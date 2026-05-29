import whisper
import sounddevice as sd
import numpy as np
import time
from scipy.io.wavfile import write
import os
import requests
import json
import re
import webbrowser
from urllib.parse import quote_plus

#PEQUEÑA NOTA
#Todos los comentarios hechos en este proyecto son para mi propio entendimiento del 
#Si, puede ser una tonteria pero tengo mala memoria y me facilitan mucho el trabajo
#Por ese motivo pueden parece obvios, inutiles o simplemente innecesarios, pero la realidad es que no comento con otro objetivo.
#Si, se que tal vez esta explicacion es innecesaria pero ya ves, no me cuesta nada

# Configuracion del audio y microfonos del dispositivo
DEVICE_ID = 1
SAMPLE_RATE = 48000
CHANNELS = 2

AUDIO_FILE = "grabacion.wav"

# Configuraciones para la grabacion del audio
SILENCE_THRESHOLD = 0.00002
SILENCE_SECONDS = 2.5
MIN_RECORD_SECONDS = 4
MAX_RECORD_SECONDS = 15
BLOCK_SECONDS = 0.2

# Configuracion de OLLAMA.
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "phi3:latest"

# Cargar modelo de Whisper.
model = whisper.load_model("medium")

# Grabar el nivel de audio para luego usarlo como referencia para decidir cuando grabar.
def get_audio_level(audio):
    volume = np.linalg.norm(audio) / len(audio)
    return volume

# Funcion que comprueba el nivel de audio y graba al detectar sonido
# Guarda el audio como un .wav que se edita sobre si mismo
def record_when_sound_detected(ui=None):

    
    print("Esperando sonido...")

    frames = []
    pre_buffer = []
    max_pre_buffer_chunks = 15

    recording = False
    start_time = None
    silence_start = None

    blocksize = int(BLOCK_SECONDS * SAMPLE_RATE)

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        device=DEVICE_ID,
        blocksize=blocksize
    ) as stream:

        while True:

            audio, overflowed = stream.read(blocksize)

            if overflowed:
                print("Aviso: overflow de audio")

            level = get_audio_level(audio)

            if not recording:
                pre_buffer.append(audio.copy())

                if len(pre_buffer) > max_pre_buffer_chunks:
                    pre_buffer.pop(0)

                print("Nivel:", level)

                if level > SILENCE_THRESHOLD:

                    print("Sonido detectado. Grabando...")
                    recording = True
                    start_time = time.time()
                    frames.extend(pre_buffer)
                    pre_buffer.clear()
                    if ui:
                        ui.set_state(ui.RECORDING)

            else:
                frames.append(audio.copy())

                elapsed = time.time() - start_time
                print("Grabando nivel:", level)

                if elapsed >= MIN_RECORD_SECONDS:
                    if level < SILENCE_THRESHOLD:
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start >= SILENCE_SECONDS:
                            print("Silencio detectado. Grabación terminada.")
                            if ui:
                                ui.set_state(ui.RESPONDING)
                            break

                    else:
                        silence_start = None

                if elapsed >= MAX_RECORD_SECONDS:
                    print("Tiempo máximo alcanzado.")
                    break

    recording_audio = np.concatenate(frames, axis=0)

    if len(recording_audio) == 0:
        print("No se grabó audio.")
        return None

    recording_int16 = np.int16(recording_audio * 32767)

    write(AUDIO_FILE, SAMPLE_RATE, recording_int16)

    print("Audio guardado en:", os.path.abspath(AUDIO_FILE))
    print("Duración aproximada:", len(recording_audio) / SAMPLE_RATE, "segundos")

    return AUDIO_FILE

# Usar el modelo de Whisper para transcribir el audio y guardarlo como texto
def transcribe_audio(audio_file):
    print("Transcribiendo audio...")

    result = model.transcribe(
        audio_file,
        language="es",
        fp16=False,
        condition_on_previous_text=False
    )

    text = result["text"].strip()

    print("Texto detectado:", text)

    return text

# Extracion a partir de la respuesta de Ollama y conversion en JSON
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No se encontró JSON en la respuesta de Ollama.")

    return match.group(0)

# Analizar la intencion de la transcripcion de Whsisper usando el modelo de Ollama.
def analyze_search_intent(text):
    print("Analizando intención con Ollama...")

    # Reglas de Ollama (Prompt dado al modelo)
    prompt = f"""
Devuelve solo un JSON válido para una búsqueda web.

Texto del usuario:
{text}

Formato obligatorio:
{{
  "intent": "search",
  "query": "",
  "engine": "google"
}}

Reglas:
- Devuelve solo JSON.
- No uses markdown.
- No expliques nada.
- El campo intent debe ser "search".
- El campo engine solo puede ser "google" o "youtube".
- El campo query nunca puede ser una explicación.
- El campo query debe contener únicamente la búsqueda final.
- Si el usuario dice "en YouTube", "youtube", "vídeo" o "videos", usa "engine": "youtube".
- Si el usuario dice "en Google", "google" o no especifica plataforma, usa "engine": "google".
- En query elimina palabras como "busca", "buscar", "abre", "abrir", "en Google", "en YouTube", "youtube", "google" o "en internet".
- Si el usuario dice "Abre YouTube en Google", devuelve query "YouTube" y engine "google".
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_predict": 80
            }
        },
        timeout=180
    )

    response.raise_for_status()

    raw_response = response.json()["response"].strip()
    print("Respuesta de Ollama:", raw_response)

    json_text = extract_json(raw_response)
    data = json.loads(json_text)

    print("JSON interpretado:", data)

    return data

# Metodo para reducir la complejidad y el tiempo de respuesta de Ollama mediantee reglas senciallas.
def quick_intent(text):
    clean = text.lower().strip()

    if ("en youtube" in clean or "youtube" in clean) and "en google" not in clean:
        engine = "youtube"
    else:
        engine = "google"

    query = clean

    words_to_remove = [
        "busca",
        "buscar",
        "abre",
        "abrir",
        "en google",
        "en youtube",
        "en internet",
        "google",
        "por favor"
    ]

    for word in words_to_remove:
        query = query.replace(word, "")

    query = query.strip(" .,;:")

    if not query and "youtube" in clean:
        query = "youtube"

    if not query:
        return None
    
    # Return de la intencion
    return {
        "intent": "search",
        "query": query,
        "engine": engine
    }

# Construir la URL a partir de la intencion lanazada por ollama y el JSON
def build_search_url(intent_data):
    query = intent_data.get("query", "").strip()
    engine = intent_data.get("engine", "google").strip().lower()

    if not query:
        return None

    if engine == "youtube":
        return "https://www.youtube.com/results?search_query=" + quote_plus(query)

    return "https://www.google.com/search?q=" + quote_plus(query)

# Abrir la URL en el navegador 
def open_search(intent_data):
    url = build_search_url(intent_data)

    if not url:
        print("No hay búsqueda válida.")
        return

    print("Abriendo búsqueda:", url)
    webbrowser.open(url)

# Bucle principal que se devuelve a app.py para lanzar el proceso completo
def run_orion(ui=None):
    audio_file = record_when_sound_detected(ui=ui)

    if not audio_file:
        return None

    if ui:
        ui.set_state(ui.RESPONDING)

    text = transcribe_audio(audio_file)

    if not text:
        return None

    intent_data = quick_intent(text)

    if not intent_data:
        intent_data = analyze_search_intent(text)

    url = build_search_url(intent_data)

    return {
        "text": text,
        "intent": intent_data,
        "url": url
    }
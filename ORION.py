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

DEVICE_ID = 1
SAMPLE_RATE = 48000
CHANNELS = 2

AUDIO_FILE = "grabacion.wav"

SILENCE_THRESHOLD = 0.00002
SILENCE_SECONDS = 2.5
MIN_RECORD_SECONDS = 4
MAX_RECORD_SECONDS = 15
BLOCK_SECONDS = 0.2

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "phi3:latest"

model = whisper.load_model("medium")


def get_audio_level(audio):
    volume = np.linalg.norm(audio) / len(audio)
    return volume


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
                        ui.request_state(ui.RECORDING)
                        ui.request_bubble("Escuchando")

            else:
                frames.append(audio.copy())

                elapsed = time.time() - start_time
                print("Grabando nivel:", level)

                if elapsed >= MIN_RECORD_SECONDS:
                    if level < SILENCE_THRESHOLD:
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start >= SILENCE_SECONDS:
                            print("Silencio detectado. Grabacion terminada.")
                            break
                    else:
                        silence_start = None

                if elapsed >= MAX_RECORD_SECONDS:
                    print("Tiempo maximo alcanzado.")
                    break

    recording_audio = np.concatenate(frames, axis=0)

    if len(recording_audio) == 0:
        print("No se grabo audio.")
        return None

    recording_int16 = np.int16(recording_audio * 32767)

    write(AUDIO_FILE, SAMPLE_RATE, recording_int16)

    print("Audio guardado en:", os.path.abspath(AUDIO_FILE))
    print("Duracion aproximada:", len(recording_audio) / SAMPLE_RATE, "segundos")

    return AUDIO_FILE


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


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No se encontro JSON en la respuesta de Ollama.")

    return match.group(0)


def analyze_search_intent(text):
    print("Analizando intencion con Ollama...")

    prompt = f"""
Devuelve solo un JSON valido para una busqueda web.

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
- El campo query nunca puede ser una explicacion.
- El campo query debe contener unicamente la busqueda final.
- Si el usuario dice "en YouTube", "youtube", "video" o "videos", usa "engine": "youtube".
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

    return {
        "intent": "search",
        "query": query,
        "engine": engine
    }


def build_search_url(intent_data):
    query = intent_data.get("query", "").strip()
    engine = intent_data.get("engine", "google").strip().lower()

    if not query:
        return None

    if engine == "youtube":
        return "https://www.youtube.com/results?search_query=" + quote_plus(query)

    return "https://www.google.com/search?q=" + quote_plus(query)


def open_search(intent_data):
    url = build_search_url(intent_data)

    if not url:
        print("No hay busqueda valida.")
        return

    print("Abriendo busqueda:", url)
    webbrowser.open(url)


def run_orion(ui=None):
    audio_file = record_when_sound_detected(ui=ui)

    if not audio_file:
        return None

    if ui:
        ui.request_state(ui.SEARCHING)
        ui.request_bubble("Transcribiendo...")

    text = transcribe_audio(audio_file)

    if not text:
        if ui:
            ui.request_bubble("No he entendiod el audio")
        return None

    if ui:
        ui.request_bubble(f'He escuchado: "{text}"')
        time.sleep(1.2)
        ui.request_bubble("Preparando busqueda...")
    intent_data = quick_intent(text)

    if not intent_data:
        if ui:
            ui.request_bubble("Consultado a Ollama...")    

        intent_data = analyze_search_intent(text)

    url = build_search_url(intent_data)

    if ui:
        query = intent_data.get("query", "")
        engine = intent_data.get("engine", "google")
        ui.request_bubble(f"Buscando: {query} en {engine}")

    return {
        "text": text,
        "intent": intent_data,
        "url": url
    }
def run_text_command(text, ui = None):
    text = text.strip()

    if not text: 
        return None
    if ui:
        ui.request_state(ui.SEARCHING)
        ui.request_bubble(f'Comando: "{text}"')
    intent_data = quick_intent(text)

    if not intent_data:
        if ui:
            ui.request_bubble("Consultado a Ollama...")
        intent_data = analyze_search_intent(text)

    url = build_search_url(intent_data)

    if ui:
        query = intent_data.get("query", "")
        engine = intent_data.get("engine", "google")
        ui.request_bubble(f"Buscando: {query} en {engine}")
    return {
        "text": text,
        "intent": intent_data,
        "url": url
    }
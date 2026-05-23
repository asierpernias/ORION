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

def record_when_sound_detected():
    print("Esperando sonido...")

    frames = []
    pre_buffer = []
    max_pre_buffer_chunks = 5

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
        raise ValueError("No se encontró JSON en la respuesta de Ollama.")

    return match.group(0)

def analyze_search_intent(text):
    print("Analizando intención con Ollama...")

    prompt = f"""
Devuelve solo un JSON válido para una búsqueda web.

Texto del usuario:
{text}

Formato obligatorio:
{{
  "intent": "search",
  "query": "solo los términos que deben buscarse",
  "engine": "google | youtube"
}}

Reglas:
- Devuelve solo JSON.
- No uses markdown.
- No expliques nada.
- Si el usuario dice "en YouTube", "youtube", "vídeo" o "videos", usa "engine": "youtube".
- Si el usuario dice "en Google", "google" o no especifica plataforma, usa "engine": "google".
- En query elimina palabras como "busca", "buscar", "abre", "en Google", "en YouTube", "youtube" o "google".
- En query deja solo lo que el usuario quiere buscar.
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
                "num_predict": 120
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
        print("No hay búsqueda válida.")
        return

    print("Abriendo búsqueda:", url)
    webbrowser.open(url)

def run_orion():
    audio_file = record_when_sound_detected()

    if not audio_file:
        return None

    text = transcribe_audio(audio_file)

    if not text:
        return None

    intent_data = analyze_search_intent(text)
    url = build_search_url(intent_data)

    return {
        "text": text,
        "intent": intent_data,
        "url": url
    }

if __name__ == "__main__":
    result = run_orion()

    if result:
        print("Resultado final:", result)
        open_search(result["intent"])
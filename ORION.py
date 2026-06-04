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
import config
from i18n import t
from logger import log

from intent_parser import parse_intent
from actions import execute

from config import(
    DEVICE_ID,
    SAMPLE_RATE,
    CHANNELS,
    AUDIO_FILE,
    SILENCE_THRESHOLD,
    SILENCE_SECONDS,
    MIN_RECORD_SECONDS,
    MAX_RECORD_SECONDS,
    BLOCK_SECONDS,
    OLLAMA_MODEL,
    OLLAMA_URL,
    WHISPER_MODEL,
    WHISPER_LANGUAGE,
    APP_LANGUAGE
)


class OrionError(Exception):
    pass
class MicrophoneError(OrionError):
    pass
class TranscriptionError(OrionError):
    pass
class IntentError(OrionError):
    pass
class BrowserSearchError(OrionError):
    pass

model = whisper.load_model(WHISPER_MODEL)


def get_audio_level(audio):
    volume = np.linalg.norm(audio) / len(audio)
    return volume


def record_when_sound_detected(ui=None):
    log("Esperando sonido...")

    frames = []
    pre_buffer = []
    max_pre_buffer_chunks = 15

    recording = False
    start_time = None
    silence_start = None

    blocksize = int(BLOCK_SECONDS * SAMPLE_RATE)

    try:
        stream_context = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        device=DEVICE_ID,
        blocksize=blocksize
    ) 
        with stream_context as stream:
            while True:
                    audio, overflowed = stream.read(blocksize)

                    if overflowed:
                        log("Aviso: overflow de audio")

                    level = get_audio_level(audio)

                    if not recording:
                        pre_buffer.append(audio.copy())

                        if len(pre_buffer) > max_pre_buffer_chunks:
                            pre_buffer.pop(0)

                        log("Nivel:", level)

                        if level > SILENCE_THRESHOLD:
                            log("Sonido detectado. Grabando...")

                            recording = True
                            start_time = time.time()
                            frames.extend(pre_buffer)
                            pre_buffer.clear()

                            if ui:
                                ui.request_state(ui.RECORDING)
                                ui.request_bubble(t("listening"))

                    else:
                        frames.append(audio.copy())

                        elapsed = time.time() - start_time
                        log("Grabando nivel:", level)

                        if elapsed >= MIN_RECORD_SECONDS:
                            if level < SILENCE_THRESHOLD:
                                if silence_start is None:
                                    silence_start = time.time()
                                elif time.time() - silence_start >= SILENCE_SECONDS:
                                    log("Silencio detectado. Grabacion terminada.")
                                    break
                            else:
                                silence_start = None

                        if elapsed >= MAX_RECORD_SECONDS:
                            log("Tiempo maximo alcanzado.")
                            break
    
    except Exception as e:
        raise MicrophoneError("No encuentro el microfono") from e
    if not frames:
        raise MicrophoneError("No he detectado audio")
    recording_audio = np.concatenate(frames, axis=0)

    if len(recording_audio) == 0:
        log("No se grabo audio.")
        return None

    recording_int16 = np.int16(recording_audio * 32767)

    write(AUDIO_FILE, SAMPLE_RATE, recording_int16)

    log("Audio guardado en:", os.path.abspath(AUDIO_FILE))
    log("Duracion aproximada:", len(recording_audio) / SAMPLE_RATE, "segundos")

    return AUDIO_FILE


def transcribe_audio(audio_file):
    log("Transcribiendo audio...")

    try:
        result = model.transcribe(
            audio_file,
            language= config.WHISPER_LANGUAGE,
            fp16=False,
            condition_on_previous_text=False
        )

    except Exception as e:
        raise TranscriptionError("No pude transcribir el audio") from e

    text = result["text"].strip()

    log("Texto detectado:", text)

    if not text:
        raise TranscriptionError("No he entendido el audio")

    return text


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No se encontro JSON en la respuesta de Ollama.")

    return match.group(0)


def analyze_search_intent(text):
    log("Analizando intencion con Ollama...")

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
    try:
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
    except requests.exceptions.RequestException as e:
        raise IntentError("Ollama no responde") from e

    raw_response = response.json()["response"].strip()
    log("Respuesta de Ollama:", raw_response)

    try:
        json_text = extract_json(raw_response)
        data = json.loads(json_text)
    except Exception as e:
        raise IntentError("Ollama devolvio una respuesta invalida") from e
    log("JSON interpretado:", data)

    return data


def quick_intent(text):
    clean = text.lower().strip()

    if ("en youtube" in clean or "youtube" in clean) and "en google" not in clean:
        engine = "youtube"
    elif ("on youtube" in clean or "in youtube" in clean) and "on google" not in clean:
        engine = "youtube"
    else:
        engine = "google"

    query = clean

    words_es = [
        "busca",
        "buscar",
        "abre",
        "abrir",
        "en google",
        "en youtube",
        "en internet",
        "google",
        "por favor",
        ""
    ]
    words_en = [
        "search",
        "look for",
        "open", 
        "in google",
        "on google",
        "in youtube",
        "on youtube",
        "in internet",
        "on internet",
        "please"
    ]

    words_common = [ 
        "youtube", "google", ""
    ]



    import config
    if config.APP_LANGUAGE == "en":
        words_to_remove = words_en + words_common
    else:
        words_to_remove = words_es + words_common
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
        raise IntentError("No hay busqueda valida")

    if engine == "youtube":
        return "https://www.youtube.com/results?search_query=" + quote_plus(query)

    return "https://www.google.com/search?q=" + quote_plus(query)


def open_search(intent_data):
    url = build_search_url(intent_data)

    if not url:
        log("No hay busqueda valida.")
        return

    log("Abriendo busqueda:", url)
    try:
        webbrowser.open(url)
    except Exception as e:
        raise BrowserSearchError("No se pudo abrir el navegador") from e


def reload_model():
    global model
    import config
    log(f"Recargando modelo whisper: {config.WHISPER_MODEL}")
    model = whisper.load_model(config.WHISPER_MODEL)



def run_orion(ui=None):
    audio_file = record_when_sound_detected(ui=ui)

    if not audio_file:
        return None

    if ui:
        ui.request_state(ui.SEARCHING)
        ui.request_bubble(t("transcribing"))

    text = transcribe_audio(audio_file)

    if not text:
        if ui:
            ui.request_bubble(t("no_audio"))
        return None

    if ui:
        ui.request_bubble(f'{t("heard") } " {text}"')
        time.sleep(1.2)
        ui.request_bubble(t("preparing"))
    
    intent_data = parse_intent(text)
    result = execute(intent_data, ui=ui)
    

    return {
        "text": text,
        "intent": intent_data,
        "result": result
    }
def run_text_command(text, ui = None):
    text = text.strip()

    if not text: 
         raise IntentError("No hay comando para procesar")
    if ui:
        ui.request_state(ui.SEARCHING)
        ui.request_bubble(f'{t("processing")} {text}')
    
    intent_data = parse_intent(text)
    
    result = execute(intent_data, ui=ui)
   

    return {
        "text": text,
        "intent": intent_data,
        "result": result
    }
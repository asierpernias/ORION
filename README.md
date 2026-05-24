# ORION

ORION es un asistente local por voz hecho en Python. Escucha el micrófono, detecta cuando el usuario habla, graba el audio, lo transcribe con Whisper, analiza la intención de búsqueda con Ollama y abre automáticamente una búsqueda en Google o YouTube.

## Flujo
Voz → Audio WAV → Whisper → Texto → Ollama → JSON → Google / YouTube

## Tecnologías

- Python
- Whisper
- Sounddevice
- Scipy
- Numpy
- Requests
- Ollama
- FastAPI
- Uvicorn

## Instalación

Instala las dependencias de Python:

```bash
pip install -r requirements.txt
```

Instala Ollama desde https://ollama.com y descarga el modelo:

```bash
ollama pull phi3
ollama list
```

## Uso en terminal

```bash
python ORION.py
```

Di una frase como:
Busca Wikipedia en Google
Busca música lofi en YouTube

## Demo web local

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8001
```

Abre en el navegador: http://127.0.0.1:8001

Pulsa **Escuchar**, habla y espera a que ORION transcriba, analice y abra la búsqueda.

## Configuración

Los valores principales están en `ORION.py`:

| Variable | Valor por defecto |
|---|---|
| `DEVICE_ID` | `1` |
| `SAMPLE_RATE` | `48000` |
| `CHANNELS` | `2` |
| `SILENCE_THRESHOLD` | `0.00002` |
| `SILENCE_SECONDS` | `2.5` |
| `MIN_RECORD_SECONDS` | `4` |
| `MAX_RECORD_SECONDS` | `15` |
| `OLLAMA_MODEL` | `phi3:latest` |

Si el micrófono no detecta bien la voz, ajusta `DEVICE_ID` o `SILENCE_THRESHOLD`.

## Troubleshooting

**Uvicorn not found**
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8001
```

**Module error** — run from inside the project folder:
```bash
cd path/to/ORION
```

**Ollama not working**
```bash
ollama list
ollama pull phi3   # if model is missing
```

**Microphone not working** — update `DEVICE_ID` in `ORION.py`.

**Browser blocks new tab** — click the result link on the page.

**App is slow** — use a lighter model in `ORION.py`:
```python
model = whisper.load_model("tiny")
```

## Demo

https://youtu.be/05UA5RDzzxI

## Nota

La demo real funciona en local porque necesita acceso al micrófono, Whisper y Ollama ejecutándose en el ordenador del usuario.

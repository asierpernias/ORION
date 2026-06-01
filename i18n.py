STRINGS = {
    "es": {
        "subtitle": "asistente local de escritorio con ia",
        "booting": "iniciando ORION",
        "checking": "comprobando configuracion local",
        "voice_engine": "motor de voz",
        "voice_language": "idioma de voz",
        "intent_engine": "motor de intencion",
        "endpoint": "ollama endpoint",
        "app_language": "idioma de app",
        "input_modes": "modods de entrada",
        "status_ready": "listo",
        "launch": "▶ Iniciar Orion",
        "config_btn": "⚙ config",
        "prompt": "> pregunta a orion...",
        "listening": "Escuchando...",
        "thinking": "Pensando...",
        "opening": "Abriendo",
        "processing": "Procesando",
        "transcribing": "Transcribiendo",
        "heard": "He escuchado...",
        "preparing": "Preparando busqueda...",
        "asking_ollama": "Consultando a OLlama...",
        "searching": "Buscando:",
        "already_running": "Ya estoy procesando algo...",
        "no_audio": "No he entendido el audio",
        "unexpected": "Ocurrio un error inesperado"
    },

    "en": {
        "subtitle": "local AI powered desktop assistant",
        "booting": "booting ORION",
        "checking": "checking local configuration",
        "voice_engine": "voice engine",
        "voice_language": "voice language",
        "intent_engine": "intent engine",
        "endpoint": "endpoint",
        "app_language": "app language",
        "input_modes": "input modes",
        "status_ready": "ready",
        "launch": "▶ Launch ORION",
        "config_btn": "⚙ config",
        "prompt": "> ask orion anything...",
        "listening": "Listening...",
        "thinking": "Thinking...",
        "opening": "Opening...",
        "processing": "Processing...",
        "transcribing": "Transcribing...",
        "heard": "I heard: ",
        "preparing": "Preparing search...",
        "asking_ollama": "Asking Ollama...",
        "searching": "Searching: ",
        "already_running": "Already processing something...",
        "no_audio": "I didn't understand the audio",
        "unexpected": "An unexpected error ocurred.",
    }
}

def t(key):
    import config
    lang = getattr(config, "APP_LANGUAGE", "es")
    return STRINGS.get(lang, STRINGS["es"].get(key, key))
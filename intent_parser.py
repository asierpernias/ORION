import config

TRIGGER_WORDS = {
    "note": {
        "es": ["anota", "guarda", "nota", "apunta", "recuerda"],
        "en": ["note", "save", "remember", "write down", "jot"]
    },
    "help": {
        "es": ["ayuda", "comandos", "qué puedes hacer", "help"],
        "en": ["help", "commands", "what can you do"]
    },
    "timer": {
        "es": ["timer", "temporizador", "pon un timer", "avisame en"],
        "en": ["timer", "set a timer", "remaind me in"]
    },
    "open_app": {
        "es": ["abre", "lanza", "ejecuta"],
        "en": ["open", "launch", "find"]
    },
    "search": {
        "es": ["busca", "buscar"],
        "en": ["search", "look for", "find"]
    }
    
}

def parse_intent(text):
    clean = text.lower().strip()
    lang = getattr(config, "APP_LANGUAGE", "es")

    for intent, langs in TRIGGER_WORDS.items():
        triggers = langs.get(lang, [])
        for trigger in triggers:
            if trigger in clean:
                payload = clean
                for t in triggers:
                    payload =  payload.replace(t, "")
                payload = payload.strip(".,;:\"'")
                return {"intent": intent, "text": payload, "raw": text}
    return {"intent": "search", "text": clean, "raw": text}

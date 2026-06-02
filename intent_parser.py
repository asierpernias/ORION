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
        "en": ["timer", "set a timer", "remind me in"]
    },
    "open_app": {
        "es": ["abre", "lanza", "ejecuta"],
        "en": ["open", "launch", "find"]
    },
    "search": {
        "es": ["busca", "buscar"],
        "en": ["search", "look for", "find"]
    },
    "note_list":{
        "es": ["lee mis notas", "mostrar notas", "muestra mis notas", "ver notas", "listar notas"],
        "en": ["read my notes", "show notes", "show my notes", "view notes", "list notes"]
    }
    
}

TRIGGER_ORDER = [
    "timer",
    "note_list",
    "note",
    "help",
    "open_app",
    "search"
]

def parse_intent(text):
    clean = text.lower().strip()
    lang = getattr(config, "APP_LANGUAGE", "es")
    for intent in TRIGGER_ORDER:
        triggers = TRIGGER_WORDS[intent].get(lang, [])

        for trigger in triggers:
            if trigger in clean:
                payload = clean
                for t in triggers:
                    payload =  payload.replace(t, "")
                payload = payload.strip(".,;:\"'")
                return {"intent": intent, "text": payload, "raw": text}
    return {"intent": "search", "text": clean, "raw": text}

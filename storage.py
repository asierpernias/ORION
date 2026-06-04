import json 
from datetime import datetime
import os
import logging

HISTORY_FILE = "history.json"
  
def save_history_entry(command_type, text, intent_data, url):
    history = load_history()

    entry = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": command_type,
        "text": text,
        "intent": intent_data.get("intent", ""),
        "query": intent_data.get("query", ""),
        "engine": intent_data.get("engine", ""),
        "url": url
    }
    
    history.append(entry)
    history = history[-50:]

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=2)
    except Exception as error:
        logging.error("No se ha podido guardar el historial: ", error)
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list):
            return data
        return []
    except Exception as error:
        logging.error("No se pudo cargar el historial: ", error)
        return []
  
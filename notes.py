import json 
import os
from datetime import datetime

NOTES_FILE = "notes.json"

def load_notes():
    if not os.path.exits(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_note(text):
    notes = load_notes()
    notes.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text
    })
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, ident=2)
    return len(notes)
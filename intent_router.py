from ORION import open_search
from actions import (
    action_note,
    action_note_list,
)

def route_intent(result, ui=None):
    intent = result.get("intent", [])
    intent_type = intent.get("intent")

    if intent_type == "search":
        open_search(intent)
        return{"handled": True, "type": "search"}
    if intent_type == "note":
        return action_note(intent, ui=ui)
    if intent_type == "note_list":
        return action_note_list(intent, ui=ui)
    return {
        "handled": False,
        "error": "unknown_intent"
    }
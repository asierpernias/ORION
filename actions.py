from i18n import t
from notes import save_note, load_notes

ACTION_REGISTRY = {}

def register(intent_name):
    def decorator(fn):
        ACTION_REGISTRY[intent_name] = fn
        return fn
    return decorator
def execute(intent_data, ui=None):
    intent = intent_data.get("intent")
    handler = ACTION_REGISTRY.get(intent)

    if handler:
        return handler(intent_data, ui=ui)
    if ui:
        ui.request_bubble(t("uknown_intent"))
        return None
    
@register("help")

def action_help(intent_data, ui=None):
    if ui:
        ui.request_bubble(t("help_text"))
    return intent_data

@register("search")
def action_search(intent_data, ui=None):
    from ORION import quick_intent, analyze_search_intent, build_search_url, open_search
    text = intent_data.get("raw", "")
    result = quick_intent(text)
    if not result:
        result = analyze_search_intent(text)
    url = build_search_url(result)
    if ui:
        query = result.get("query", "")
        engine = result.get("engine", "")
        ui.request_bubble(f'{t("searching")} {query} — {engine}')
    open_search(result)
    return {"intent": result, "url": url}

@register("timer")
def action_timer(intent_data, ui=None):
    pass

@register("open_app")
def action_oppen_app(intent_data, ui=None):
    pass

@register("note")
def action_note(intent_data, ui=None):
    text = intent_data.get("text", "")
    text = text.strip() if isinstance(text, str) else ""

    if not text: 
        if ui:
            ui.request_bubble("error")
        return None
    total = save_note(text)

    if ui:
        ui.request_bubble(f"Nota guardada ({total})")

    return {
        "saved": True,
        "count": total
    }

@register("note list")
def action_note_list(intent_data, ui=None):
    notes = load_notes()

    if not notes:
        if ui:
            ui.request_bubble("No hay notas guardadas")
        return {
            "count": 0,
            "notes": []
        }
    lines = []

    for note in notes:
        text = note.get("text", "")
        timestamp = note.get("timestamp", "")
        lines.append(f"• {text} ({timestamp}) ")

    message = "\n".join(lines)

    if ui:
        ui.request_bubble(message)

    return {
        "count": len(notes),
        "notes": notes
    }



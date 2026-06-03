from i18n import t
from notes import save_note, load_notes
import re
import winsound
import threading

from ORION import save_history_entry

import os

active_timers = []
ACTION_REGISTRY = {}


def register(intent_name):
    def decorator(fn):
        ACTION_REGISTRY[intent_name] = fn
        return fn
    return decorator
def execute(intent_data, ui=None):
    print("execute")
    intent = intent_data.get("intent")
    handler = ACTION_REGISTRY.get(intent)
    result = None
    if handler:
        return handler(intent_data, ui=ui)
    save_history_entry(        command_type="intent",
        text=intent_data.get("raw", ""),
        intent_data=intent_data,
        result=result
    )

    if not handler:
        if ui:
            ui.request_bubble(t("unknown_intent"))
    return None
    
@register("help")

def action_help(intent_data, ui=None):
    print("1")
    if ui:
        ui.request_bubble(t("help_text"))
    return intent_data

@register("search")
def action_search(intent_data, ui=None):
    print("2")
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
    print("3")
    text = intent_data.get("text", "")
    seconds = parse_duration(text)

    if not seconds:
        if ui:
            ui.request_bubble(t("timer_invalid"))
        return None
    label =  f"{seconds}s"

    if ui: 
        ui.request_bubble(f'{t("timer_set")} {label}')

    def timer_callback():
        winsound.Beep(1000, 800)
        if ui:
            ui.request_bubble(t("timer_done"))

    timer = threading.Timer(seconds, timer_callback)
    timer.daemon = True
    timer.start()
    active_timers.append(timer)

    return {"intent": "timer", "seconds": seconds}
    

@register("open_app")
def action_oppen_app(intent_data, ui=None):
    import subprocess
    import shutil
    import glob
    import platform

    app_name = intent_data.get("text", "").strip()
    if not app_name:
        if ui: 
            ui.request_bubble(t("open_app_empty"))
        return None
    query = app_name.lower()
    system = platform.system()
    found = shutil.which(app_name)
    
    if found:
        subprocess.Popen([app_name])
        if ui:
            ui.request_bubble(f'{t("open_app_opening")} {app_name}')
        return {"opened": app_name}
    if system == "Windows":
        search_dirs = [
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expanduser("~/Desktop"),
        ]
        for directory in search_dirs:
            matches = glob.glob(os.path.join(directory, "**", "*.lnk"), recursive=True)
            for match in matches:
                filename = os.path.splitext(os.path.basename(match))[0].lower()
                if query in filename:
                    os.startfile(match)
                    if ui:
                        ui.request_bubble(f'{t("open_app_opening")} {filename}')
                    return {"opened": filename}  
        program_dirs = [
            os.path.expandvars("%PROGRAMFILES%"),
            os.path.expandvars("%PROGRAMFILES(X86)%"),
            os.path.expandvars("%LOCALAPPDATA%"),
        ]
        for directory in program_dirs:
            matches = glob.glob(os.path.join(directory, "**", f"*{query}*.exe"), recursive=True)
            if matches:
                subprocess.Popen([matches[0]])
                name = os.path.basename(matches[0])
                if ui:
                    ui.request_bubble(f'{t("open_app_opening")} {name}')
                return {"opened": name}
            
    elif system == "Darwin":
        matches = glob.glob(f"/Applications/**/*{app_name}*.app", recursive=True)
        matches += glob.glob(os.path.expanduser(f"~/Applications/**/*{app_name}*.app"), recursive=True)
        if matches:
            subprocess.Popen(["open", matches[0]])
            name = os.path.splitext(os.path.basename(matches[0]))[0]
            if ui:
                ui.request_bubble(f'{t("open_app_opening")} {name}')
            return {"opened": name}
    elif system == "Linux":
        desktop_dirs = [
            "/usr/share/applications",
            "/usr/local/share/applications",
            os.path.expanduser("~/.local/share/applications"),
        ]
        for directory in desktop_dirs:
            matches = glob.glob(os.path.join(directory, "*.desktop"))
            for match in matches:
                try:
                    with open(match, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read().lower()
                    if query in content:
                        for line in content.splitlines():
                                if line.startswith("exec="):
                                    cmd = line.split("=", 1)[1].split()[0]
                                    subprocess.Popen([cmd])
                                    name = os.path.splitext(os.path.basename(match))[0]
                                    if ui:
                                        ui.request_bubble(f'{t("open_app_opening")} {name}')
                                    return {"opened": name}
                except Exception:
                    continue
    if ui:
        ui.request_bubble(f'{t("open_app_not_found")} {app_name}')
    return None

@register("note")
def action_note(intent_data, ui=None):
    text = intent_data.get("text", "")
    text = text.strip() if isinstance(text, str) else ""

    if not text: 
        if ui:
            ui.request_bubble(t("note_empty"))
        return None
    total = save_note(text)

    if ui:
        svg_msg = t("note_saved")
        ui.request_bubble(f"{svg_msg} ({total})")

    return {
        "saved": True,
        "count": total
    }

@register("note_list")
def action_note_list(intent_data, ui=None):
    notes = load_notes()

    if not notes:
        if ui:
            ui.request_bubble(t("notes_empty"))
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


def parse_duration(text):
    patterns_es = [
        (r'(\d+)\s*hora', 3600),
        (r'(\d+)\s*minuto', 60),
        (r'(\d+)\s*segundo', 1), 
    ]
    patterns_en = [
        (r'(\d+)\s*hour', 3600),
        (r'(\d+)\s*minute', 60),
        (r'(\d+)\s*second', 1), 
    ]

    import config
    patterns = patterns_en if config.APP_LANGUAGE == "en" else patterns_es

    total = 0

    for pattern, multiplier, in patterns:
        match = re.search(pattern, text.lower())
        if match:
            total += int(match.group(1)) * multiplier
    return total if total > 0 else None

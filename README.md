
# ORION

> local desktop assistant with AI

voice + text. no cloud processing. everything local.

---

## > what is it

ORION is a desktop assistant that lives in the corner of your screen. You can talk to it or type commands, and it understands and executes them.

Whisper transcribes audio locally. A machine learning model analyzes intent. Nothing leaves your computer.

---

## > features

* local voice recognition using Whisper
* voice and text interaction
* fully offline processing
* local intent detection system
* local note storage
* timer system with sound alert
* open applications from commands
* smart search (Google / YouTube)
* draggable floating desktop avatar
* lightweight desktop UI
* privacy-focused design

---

## > commands (v2)

search [query]
-> opens Google or YouTube depending on context

note [text]
-> saves notes locally

show my notes
-> lists saved notes

set a timer for [time]
-> starts a countdown timer with sound alert

open [app]
-> launches any application on your system

help
-> shows available commands

---

## > installation

### installer method

download ORION_Setup_1.0.0.exe
run the installer
launch ORION from the desktop shortcut

---

### from source

```bash
git clone https://github.com/your-username/orion
cd orion
pip install -r requirements.txt
python app.py
```

---

## > usage

double click avatar -> voice mode
click or press space -> text input mode

the avatar appears in the bottom-right corner and can be dragged anywhere on the screen

---

## > configuration

edit config.py to change settings:

WHISPER_MODEL
APP_LANGUAGE
WHISPER_LANGUAGE

---

## > requirements

minimum system requirements:

* Windows 10 / 11
* Python 3.11+
* microphone for voice mode
* 200MB+ free disk space

python dependencies:

```txt
PyQt6
openai-whisper
numpy
scikit-learn
pyaudio
```

---

## > technologies

* Python
* PyQt6
* OpenAI Whisper (local speech-to-text)
* machine learning intent classification
* SQLite / JSON local storage
* PyInstaller for packaging
* GitHub Actions for builds

---


## > roadmap

* custom wake word detection
* plugin system with a system that allows user create plugings
* App cache for faster speed response

---

## > license

MIT License

Copyright (c) 2026 Asier Pernia Soria

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.


---

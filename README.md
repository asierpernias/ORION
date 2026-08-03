# ORION

### Local Desktop Assistant with AI

A voice/text assistant that can open apps, save notes, and perform tasks such as setting timers.

# Commands (v2)

Right now these are the commands that I have been able to release:

### `search [query]`
Opens Google or YouTube depending on the context.

### `note [text]`
Saves notes locally.

### `show my notes`
Lists saved notes.

### `set a timer for [time]`
Starts a countdown timer with a sound alert.

### `open [app]`
Launches any application on your system.

### `help`
Shows the available commands.

# Installation

To install ORION, first make sure you have Ollama installed and running on your system, as it is used for intent analysis and command understanding.

Once Ollama is installed:

1. Download the model used by ORION.
2. Start the local Ollama server.
3. Download the latest ORION release.
4. Extract the ZIP file and keep all files in the same folder, including the assets and configuration files.
5. Launch `ORION.exe`.

The assistant will be ready to use.

If you prefer running the project from source:

1. Clone the repository.
2. Create a Python virtual environment.
3. Install the dependencies listed in `requirements.txt`.
4. Run `app.py`.

> ORION requires a working microphone for voice commands and stores all configuration and history locally on your machine.

# How to use it

There are two ways to interact with ORION:

- Click the avatar to use voice input.
- Click the text button (or press **Space** after selecting the avatar) to open the text input bar.

The avatar appears in the bottom-right corner of the screen. You can click and drag it anywhere on your desktop.


# Configuration

Open **Config** from the launch page to change:

- App language
- ORION language
- Whisper model

The default Whisper model is a lightweight one to make the application more accessible on lower-end computers.


# Minimum System Requirements

- Windows 10 / 11
- Linux *(experimental)*
- macOS *(experimental)*
- Python installed
- A microphone (for voice mode)
- Around **200 MB** of free disk space

> Linux and macOS have not been fully tested and may contain bugs.

## Python Dependencies

```txt
PyQt6
openai-whisper
numpy
scikit-learn
pyaudio
```


# What I Used to Create This Project

- Python (application core)
- PyQt6 (UI)
- OpenAI Whisper (local speech-to-text)
- Machine learning intent classification with a keyword-based fallback depending on the model confidence
- Local JSON storage (stores up to 50 logs)
- PyInstaller (Windows builds)
- GitHub Actions (Linux and macOS builds)

# What's Next?

Once my project gets reviewed, I plan to add:

- A plugin marketplace where users can install and publish new features.
- A web dashboard where users can view statistics and other information.

# Images

![Launch Page](<Captura de pantalla 2026-06-05 092915.png>)

![Avatar](<Captura de pantalla 2026-06-02 151750.png>)

![History](<Captura de pantalla 2026-06-02 151800.png>)

![Configuration](<Captura de pantalla 2026-06-02 150725.png>)


# License

MIT License

Copyright (c) 2026 Asier Pernia Soria

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.


---

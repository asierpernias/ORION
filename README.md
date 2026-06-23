
# ORION

### local desktop assistant with AI

 a voice / text assistant which can open apps, save notes and do things such as set timers.

---

## commands (v2)

Right now this are the commands that I have been able to release:

search [query];
opens Google or YouTube depending on context

note [text]:
saves notes locally

show my notes
lists saved notes

set a timer for [time]
starts a countdown timer with sound alert

open [app]
launches any application on your system

help
shows available commands

---

## installation

To install ORION, first make sure you have Ollama installed and running on your system, as it is used for intent analysis and command understanding. Once Ollama is installed, download the model used by ORION and start the local server. After that, download the latest ORION release, extract the ZIP file, and keep all files inside the same folder, including the assets and configuration files. Finally, launch ORION.exe and the assistant will be ready to use. If you prefer running the project from source, clone the repository, create a Python virtual environment, install the dependencies listed in requirements.txt, and execute app.py. ORION requires a working microphone for voice commands and stores all configuration and history locally on your machine

## > how to use it

The two ways to use is by clicking on the avatar (voice input) or clicking in the button/click on avatar + space to open the text bar.

The avatar will appear on the right bottom of the screen and by clicking and dragging you can move it to any place on the screen.

---

## configuration

By entering in config in the launch page you can change the app language, orion language and the whisper model, set on a light one in order to make it more accesible to all users.

---


## 

minimum system requirements:

* Windows 10 / 11 // Linux // macOs
  (Linux and mac hadnt been tried susceptible
  of errors)
* Python downloaded.
* microphone for voice mode
* Is not really accurate but more or less 200mb+ free disk space

python dependencies:

```txt
PyQt6
openai-whisper
numpy
scikit-learn
pyaudio
```

---

## what I used to create this project

* Python (all the core)
* PyQt6 (ui of the app)
* OpenAI Whisper (local speech-to-text)
* machine learning intent classification (with a backup with key words depending on the fiabilty shown by the model)
* JSON local storage that saves up to 50 logs 
* PyInstaller for packaging for windows
* GitHub Actions for builds for linux and macOs
* 

---


## what is next?

Once my project gets reviewed my plans are to add these new features
- A pluging marketplace from where users could add new features and release them
- Some web where users can see stats and those type of things

---

## imagenes

![Launch Page](<Captura de pantalla 2026-06-05 092915.png>)
![Avatar](<Captura de pantalla 2026-06-02 151750.png>)
![Historial](<Captura de pantalla 2026-06-02 151800.png>)
![Configuation](<Captura de pantalla 2026-06-02 150725.png>)

## license

MIT License

Copyright (c) 2026 Asier Pernia Soria

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.


---

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap


def start_idle_animation(window):

    window.idle_frames = [
        QPixmap("assets/idle/idle_1.png"),
        QPixmap("assets/idle/idle_2.png"),
        QPixmap("assets/idle/idle_3.png"),
        QPixmap("assets/idle/idle_4.png"),
        QPixmap("assets/idle/idle_5.png")
    ]

    window.idle_durations = [400, 250, 100, 250, 300]
    window.current_idle_frame = 0

    window.idle_timer = QTimer()
    window.idle_timer.timeout.connect(
        lambda: update_idle_frame(window)
    )

    window.idle_timer.start(window.idle_durations[0])


def update_idle_frame(window):

    window.avatar.setPixmap(
        window.idle_frames[window.current_idle_frame]
    )

    duration = window.idle_durations[window.current_idle_frame]

    window.current_idle_frame += 1

    if window.current_idle_frame >= len(window.idle_frames):
        window.current_idle_frame = 0

    window.idle_timer.start(duration)
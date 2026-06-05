from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap
from paths import resource_path

def start_idle_animation(window):

    if hasattr(window, "idle_timer"):
        window.idle_timer.stop()

    window.idle_frames = [
        QPixmap(resource_path("assets/idle/idle_1.png")),
        QPixmap(resource_path("assets/idle/idle_2.png")),
        QPixmap(resource_path("assets/idle/idle_3.png")),
        QPixmap(resource_path("assets/idle/idle_4.png")),
        QPixmap(resource_path("assets/idle/idle_5.png"))
    ]

    window.idle_durations = [400, 250, 100, 250, 300]
    window.current_idle_frame = 0

    window.idle_timer = QTimer()

    def update():
        window.avatar.setPixmap(
            window.idle_frames[window.current_idle_frame]
        )

        duration = window.idle_durations[window.current_idle_frame]

        window.current_idle_frame += 1
        if window.current_idle_frame >= len(window.idle_frames):
            window.current_idle_frame = 0

        window.idle_timer.start(duration)

    window.idle_timer.timeout.connect(update)
    window.idle_timer.start(window.idle_durations[0])


def start_searching_animation(window):

    if hasattr(window, "searching_timer"):
        window.searching_timer.stop()

    window.searching_frames = [
        QPixmap(resource_path("assets/searching/searching_1.png")),
        QPixmap(resource_path("assets/searching/searching_2.png")),
        QPixmap(resource_path("assets/searching/searching_3.png")),
        QPixmap(resource_path("assets/searching/searching_4.png"))
    ]

    window.searching_index = 0
    window.searching_timer = QTimer()

    def update():
        window.avatar.setPixmap(
            window.searching_frames[window.searching_index]
        )

        window.searching_index = (
            window.searching_index + 1
        ) % len(window.searching_frames)

    window.searching_timer.timeout.connect(update)
    window.searching_timer.start(200)


def start_recording_animation(window):

    if hasattr(window, "recording_timer"):
        window.recording_timer.stop()

    window.recording_frames = [
        QPixmap(resource_path("assets/recording/recording_1.png")),
        QPixmap(resource_path("assets/recording/recording_2.png")),
        QPixmap(resource_path("assets/recording/recording_3.png")),
        QPixmap(resource_path("assets/recording/recording_4.png")),
        QPixmap(resource_path("assets/recording/recording_5.png")),
        QPixmap(resource_path("assets/recording/recording_6.png"))
    ]

    window.recording_index = 0
    window.recording_timer = QTimer()

    def update():
        window.avatar.setPixmap(
            window.recording_frames[window.recording_index]
        )

        window.recording_index = (
            window.recording_index + 1
        ) % len(window.recording_frames)

    window.recording_timer.timeout.connect(update)
    window.recording_timer.start(200)


def start_responding_animation(window):

    if hasattr(window, "responding_timer"):
        window.responding_timer.stop()

    window.responding_frames = [
        QPixmap(resource_path("assets/responding/responding_1.png")),
        QPixmap(resource_path("assets/responding/responding_2.png")),
        QPixmap(resource_path("assets/responding/responding_3.png")),
        QPixmap(resource_path("assets/responding/responding_4.png"))
    ]

    window.responding_index = 0
    window.responding_timer = QTimer()

    def update():
        window.avatar.setPixmap(
            window.responding_frames[window.responding_index]
        )

        window.responding_index = (
            window.responding_index + 1
        ) % len(window.responding_frames)

    window.responding_timer.timeout.connect(update)
    window.responding_timer.start(200)
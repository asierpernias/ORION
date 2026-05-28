from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap
from ui import AvatarWindow


def idle_animation(self):

    self.idle_frames = [
        QPixmap("assets/idle/idle_1.png"),
        QPixmap("assets/idle/idle_2.png"),
        QPixmap("assets/idle/idle_3.png"),
        QPixmap("assets/idle/idle_4.png"),
        QPixmap("assets/idle/idle_5.png")
    ]

    self.idle_durations = [400, 250, 100, 250, 300]

    self.current_idle_frame = 0

    self.idle_timer = QTimer()

    self.idle_timer.timeout.connect(self.update_idle_frame)

    self.idle_timer.start(self.idle_durations[0])


def update_idle_frame(self):

    self.avatar.setPixmap(
        self.idle_frames[self.current_idle_frame]
    )

    duration = self.idle_durations[self.current_idle_frame]

    self.current_idle_frame += 1

    if self.current_idle_frame >= len(self.idle_frames):
        self.current_idle_frame = 0

    self.idle_timer.start(duration)
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
import threading

from controller import controller_run_orion
from bubbles import SpeechBubble

from animations import (
    start_idle_animation,
    start_recording_animation,
    start_searching_animation,
    start_responding_animation
)


class AvatarWindow(QWidget):

    state_requested = pyqtSignal(str)

    IDLE = "IDLE"
    RECORDING = "RECORDING"
    SEARCHING = "SEARCHING"
    RESPONDING = "RESPONDING"

    def __init__(self):
        super().__init__()

        self.state_requested.connect(self.set_state)

        self.drag_position = None
        self.lock = threading.Lock()

        self.setup_window()
        self.setup_avatar()
        self.setup_bubble()

        self.setWindowIcon(QIcon("assets/icon.ico"))

        self.state = None
        self.set_state(self.IDLE)

    def setup_bubble(self):
        self.bubble = SpeechBubble(self)
        self.bubble.move(260, 40)
        self.bubble.hide()
        

    def setup_window(self):
        self.setWindowTitle("ORION")
        self.resize(4096, 4096)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def setup_avatar(self):
        self.avatar = QLabel(self)
        pixmap = QPixmap("assets/idle/idle_1.png")
        self.avatar.setPixmap(pixmap)
        self.avatar.resize(pixmap.width(), pixmap.height())

    def request_state(self, new_state):
        self.state_requested.emit(new_state)

    def set_state(self, new_state):
        if self.state == new_state:
            return

        self.state = new_state

        print("New state =", new_state)

        self.stop_all_animations()
        self.update_animation()
        self.update_bubble()

    def stop_all_animations(self):
        if hasattr(self, "idle_timer"):
            self.idle_timer.stop()

        if hasattr(self, "recording_timer"):
            self.recording_timer.stop()

        if hasattr(self, "searching_timer"):
            self.searching_timer.stop()

        if hasattr(self, "responding_timer"):
            self.responding_timer.stop()

    def update_animation(self):
        if self.state == self.IDLE:
            start_idle_animation(self)

        elif self.state == self.RECORDING:
            start_recording_animation(self)

        elif self.state == self.SEARCHING:
            start_searching_animation(self)

        elif self.state == self.RESPONDING:
            start_responding_animation(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def mouseDoubleClickEvent(self, event):
        controller_run_orion(self)

    def update_bubble(self):
        if self.state == self.IDLE:
            self.bubble.hide()
        elif self.state == self.RECORDING:
            self.bubble.set_text("Escuchando...")
        elif self.state == self.SEARCHING:
            self.bubble.set_text("Pensando...")
        elif self.state == self.RESPONDING:
            self.bubble.set_text("Abriendo...")

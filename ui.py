from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QIcon, QGuiApplication
from PyQt6.QtCore import Qt, pyqtSignal

from i18n import t
from history_button import HistoryButton
from history_window import HistoryWindow

import threading

from controller import controller_run_orion, controller_run_text
from bubbles import SpeechBubble
from command_bar import CommandBar
from input_button import inputButton

from animations import (
    start_idle_animation,
    start_recording_animation,
    start_searching_animation,
    start_responding_animation
)


class AvatarWindow(QWidget):

    state_requested = pyqtSignal(str)
    bubble_requested = pyqtSignal(str)

    IDLE = "IDLE"
    RECORDING = "RECORDING"
    SEARCHING = "SEARCHING"
    RESPONDING = "RESPONDING"

    def __init__(self):
        super().__init__()

        self.state_requested.connect(self.set_state)
        self.bubble_requested.connect(self.set_bubble_text)

        self.drag_position = None
        self.lock = threading.Lock()

        self.setup_window()
        self.setup_avatar()
        self.setup_bubble()
        self.setup_command_bar()
        self.setup_input_button()
        self.setup_history_button()

        self.setWindowIcon(QIcon("assets/icon.ico"))

        self.state = None
        self.set_state(self.IDLE)

    def setup_window(self):
        self.setWindowTitle("ORION")

        self.resize(4096, 4096)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def setup_avatar(self):
        self.avatar = QLabel(self)

        pixmap = QPixmap("assets/idle/idle_1.png")

        self.avatar.setPixmap(pixmap)

        self.avatar.resize(
            pixmap.width(),
            pixmap.height()
        )

        screen = QGuiApplication.primaryScreen().availableGeometry()

        x = screen.width() - pixmap.width() - 80
        y = screen.height() - pixmap.height() - 80

        self.avatar.move(x, y)

    def setup_bubble(self):
        self.bubble = SpeechBubble(self)
        self.bubble.hide()

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

    def update_bubble(self):
        if self.state == self.IDLE:
            self.bubble.hide()
            return

        if self.state == self.RECORDING:
            self.bubble.set_text(t("listening"))

        elif self.state == self.SEARCHING:
            self.bubble.set_text(t("thinking"))

        elif self.state == self.RESPONDING:
            self.bubble.set_text(t("opening"))

        self.position_bubble()

    def position_bubble(self):
        margin = 20

        avatar_x = self.avatar.x()
        avatar_y = self.avatar.y()
        avatar_width = self.avatar.width()

        bubble_width = self.bubble.width()

        x = avatar_x - bubble_width - margin
        y = avatar_y + 20

        if x < 0:
            x = avatar_x + avatar_width + margin

        self.bubble.move(x, y)

    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.avatar.pos()
            )

            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            self.avatar.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            self.position_input_button()
            self.position_bubble()
            self.position_history_button()

            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def mouseDoubleClickEvent(self, event):
        controller_run_orion(self)

    def request_bubble(self, text):
        self.bubble_requested.emit(text)

    def set_bubble_text(self, text):
        if not text:
            self.bubble.hide()
            return
        self.bubble.set_text(text)
        self.position_bubble()

    def setup_command_bar(self):
        self.command_bar = CommandBar(self)
        self.command_bar.submitted.connect(self.handle_text_command)
        self.command_bar_position = self.calculate_command_bar_position()
        self.command_bar.move(*self.command_bar_position)
        self.command_bar.hide()
    def position_command_bar(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()

        x = (screen.width() - self.command_bar.width()) // 2
        y = screen.height() - self.command_bar.height() - 80

        self.command_bar.move(x, y)

    

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.toggle_command_bar()

    def handle_text_command(self, text):
        if self.lock.locked():
            self.request_bubble("Ya estoy procesando algo...")
            return
        controller_run_text(self, text)
    def calculate_command_bar_position(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()

        x = (screen.width() - self.command_bar.width()) // 2
        y = screen.height() - self.command_bar.height() - 80

        return x, y 
    
    def setup_input_button(self):
        self.input_button = inputButton(self)
        self.input_button.clicked.connect(self.toggle_command_bar)
        self.position_input_button()
        self.input_button.show()

    def setup_history_button(self):
        self.history_button = HistoryButton(self)
        self.history_button.clicked.connect(self.open_history_window)
        self.position_history_button()
        self.history_button.show()

    def position_history_button(self):
        margin_x = 52
        margin_y = 12

        x = self.avatar.x() + self.avatar.width() - self.history_button.width() - margin_x
        y = self.avatar.y() - self.history_button.height() + margin_y

        self.history_button.move(x, y)
        self.history_button.raise_()

    def position_input_button(self):
        magin_x = 12
        margin_y = 12

        x = self.avatar.x() + self.avatar.width() -self.input_button.width() - magin_x
        y = self.avatar.y() - self.input_button.height() + margin_y

        self.input_button.move(x, y)
        self.input_button.raise_()

    def toggle_command_bar(self):
        if self.lock.locked():
            self.request_bubble("Ya estoy procesando algo...")
            return
        self.command_bar.toggle()

    def open_history_window(self):
        if not hasattr(self, "history_window") or self.history_window is None:
            self.history_window = HistoryWindow(parent=self)
        self.history_window.refresh()
        self.history_window.show()
        self.history_window.raise_()
        self.history_window.activateWindow()
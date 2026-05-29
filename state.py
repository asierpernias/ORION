from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

from animations import start_idle_animation, start_recording_animation, start_responding_animation, start_searching_animation

class AvatarWindow(QWidget):

    IDLE = "IDLE"
    RESPONDING = "RESPONDING"
    SEARCHING = "SEARCHING"
    RECORDING = "RECORDING"

    def __init__(self):
        super().__init__()

        self.state = self.IDLE
        self.setup_window()
        self.setup_avatar()

        self.set_state(self.IDLE)

    def set_state(self, new_state):
        if self.state == new_state:
            return
        
        self.state = new_state
        self.stop_all_animations()
        print("New state =", new_state)
        self.update_animation()

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
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

from animations import start_idle_animation


class AvatarWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_window()
        self.setup_avatar()

        start_idle_animation(self)
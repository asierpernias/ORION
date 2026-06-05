import os 
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from logger import log
from paths import resource_path

class HistoryButton(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, assets_dir=resource_path("assets\history_button"), scale=2):
        super().__init__(parent)

        self.assets_dir = assets_dir
        self.scale = scale
        self.idle_pixmap = self.load_pixmap(resource_path("pixil-frame-0.png"))
        self.hover_pixmap = self.load_pixmap(resource_path("pixil-frame-2.png"))
        self.pressed_pixmap = self.load_pixmap(resource_path("pixil-frame-1.png"))

        self.setPixmap(self.idle_pixmap)
        self.resize(
            self.idle_pixmap.width(),
            self.idle_pixmap.height()

        )

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def load_pixmap(self, filename):
        path = os.path.join(self.assets_dir, filename)
        pixmap = QPixmap(path)

        if pixmap.isNull():
            log("Missing asset: ", path)
            return QPixmap()
        return pixmap.scaled(
            pixmap.width() * self.scale,
            pixmap.height() * self.scale,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.FastTransformation
        )
    def enterEvent(self, event):
        if not self.hover_pixmap.isNull():
            self.setPixmap(self.hover_pixmap)
        
    def leaveEvent(self, event):
        if not self.idle_pixmap.isNull():
            self.setPixmap(self.idle_pixmap)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.pressed_pixmap.isNull():
                self.setPixmap(self.pressed_pixmap)
            event.accept()
    def mouseReleaseEvent(self, event):
        
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.hover_pixmap.isNull():
                self.setPixmap(self.hover_pixmap)
            
            self.clicked.emit()
            event.accept()
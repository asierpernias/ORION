import os

from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QLineEdit

import logging


class CommandLineEdit(QLineEdit):
    escape_pressed = pyqtSignal()  
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.escape_pressed.emit()
            event.accept()
            return
        super().keyPressEvent(event)

class CommandBar(QWidget):

    submitted = pyqtSignal(str)

    def __init__(
        self,
        parent=None,
        assets_dir="assets/input_bar",
        scale=4,
        width=640
    ):
        super().__init__(parent)

        self.assets_dir = assets_dir
        self.scale = scale
        self.bar_width = width

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.left = self.load_part("bar_left.png")
        self.center = self.load_part("bar_center.png")
        self.right = self.load_part("bar_right.png")

        if self.center.isNull():
            self.bar_height = 32
        else:
            self.bar_height = self.center.height()

        self.setFixedSize(self.bar_width, self.bar_height)

        self.input = CommandLineEdit(self)
        self.input.setPlaceholderText("Escribe una indicacion...")
        self.input.setFont(QFont("Inter", 9))
        self.input.setFrame(False)
        self.input.setTextMargins(0, 0, 0, 0)
        self.input.setStyleSheet("""
            QLineEdit {
                color: #1b1b1b;
                background: transparent;
                border: none;
                padding: 0px;
                selection-background-color: #7aa2ff;
            }
        """)

        self.input.returnPressed.connect(self.submit)
        self.input.escape_pressed.connect(self.hide_bar)

        self.layout_input()
        self.hide()

    def load_part(self, filename):
        path = os.path.join(self.assets_dir, filename)
        pixmap = QPixmap(path)

        if pixmap.isNull():
            logging.critical("Missing command bar asset:", path)
            return QPixmap()

        return pixmap.scaled(
            pixmap.width() * self.scale,
            pixmap.height() * self.scale,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

    def layout_input(self):
        padding_x = 30

        self.input.setGeometry(
            padding_x,
            0,
            self.width() - padding_x * 2,
            self.height()
        )

    def show_bar(self):
        self.show()
        self.raise_()
        self.input.setFocus()

    def hide_bar(self):
        self.input.clear()
        self.hide()

        if self.parent():
            self.parent().setFocus()

    def toggle(self):
        if self.isVisible():
            self.hide_bar()
        else:
            self.show_bar()

    def submit(self):
        text = self.input.text().strip()

        if not text:
            return

        self.input.clear()
        self.hide()

        if self.parent():
            self.parent().setFocus()

        self.submitted.emit(text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

        if self.left.isNull() or self.center.isNull() or self.right.isNull():
            return

        left_width = self.left.width()
        right_width = self.right.width()
        center_width = self.width() - left_width - right_width

        painter.drawPixmap(0, 0, self.left)

        center_rect = QRect(
            left_width,
            0,
            center_width,
            self.height()
        )

        painter.drawTiledPixmap(center_rect, self.center)

        painter.drawPixmap(
            self.width() - right_width,
            0,
            self.right
        )

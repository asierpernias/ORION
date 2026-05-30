import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QLineEdit


class CommandBar(QWidget):

    submitted = pyqtSignal(str)

    def __init__(
        self,
        parent=None,
        assets_dir="assets/input_bar",
        scale=4,
        width=672,
        height=64
    ):
        super().__init__(parent)

        self.assets_dir = assets_dir
        self.scale = scale
        self.bar_width = width
        self.bar_height = height

        
        

        self.left = self.load_part("bar_left.png")
        self.center = self.load_part("bar_center.png")
        self.right = self.load_part("bar_right.png")

        self.setFixedSize(self.bar_width, self.bar_height)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        if not self.center.isNull():
            self.bar_height = self.center.height()
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Escribe una indicacion...")
        self.input.setFont(QFont("Inter", 12))
        self.input.setFrame(False)
        self.input.setStyleSheet("""
            QLineEdit {
                color: #1b1b1b;
                background: transparent;
                border: none;
                selection-background-color: #7aa2ff;
            }
        """)

        self.input.returnPressed.connect(self.submit)

        self.layout_input()
        self.hide()

    def load_part(self, filename):
        path = os.path.join(self.assets_dir, filename)
        pixmap = QPixmap(path)

        if pixmap.isNull():
            print("Missing command bar asset:", path)
            return QPixmap()

        return pixmap.scaled(
            pixmap.width() * self.scale,
            pixmap.height() * self.scale,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

    def layout_input(self):
        padding_x = 28
        input_height = 36
        input_y = 8


        self.input.setGeometry(
            padding_x,
            input_y,
            self.width() - padding_x * 2,
            input_height
        )

    def show_bar(self):
        self.show()
        self.raise_()
        self.input.setFocus()

    def hide_bar(self):
        self.input.clear()
        self.hide()

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

        self.submitted.emit(text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

        if self.left.isNull() or self.center.isNull() or self.right.isNull():
            return

        left_width = self.left.width()
        right_width = self.right.width()
        center_width = self.center.width()

        painter.drawPixmap(0, 0, self.left)

        x = left_width
        end_x = self.width() - right_width

        while x < end_x:
            draw_width = min(center_width, end_x - x)

            if draw_width == center_width:
                painter.drawPixmap(x, 0, self.center)
            else:
                painter.drawPixmap(
                    x,
                    0,
                    self.center.copy(0, 0, draw_width, self.center.height())
                )

            x += draw_width

        painter.drawPixmap(end_x, 0, self.right)
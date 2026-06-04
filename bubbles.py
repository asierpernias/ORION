import os

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPixmap, QFont, QFontMetrics
from PyQt6.QtWidgets import QWidget, QLabel
from logger import log

class SpeechBubble(QWidget):

    def __init__(
        self,
        parent=None,
        assets_dir="assets/bubbles",
        tile_size=8,
        scale=4,
        max_text_width=320
    ):
        super().__init__(parent)

        self.assets_dir = assets_dir
        self.tile_size = tile_size
        self.scale = scale
        self.max_text_width = max_text_width

        self.tile_px = self.tile_size * self.scale
        self.padding_x = self.tile_px
        self.padding_y = self.tile_px

        self.text = ""

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.tiles = {
            "top_left": self.load_tile("bubble_top_left.png"),
            "top": self.load_tile("bubble_top.png"),
            "top_right": self.load_tile("bubble_top_right.png"),
            "left": self.load_tile("bubble_left.png"),
            "center": self.load_tile("bubble_center.png"),
            "right": self.load_tile("bubble_right.png"),
            "bottom_left": self.load_tile("bubble_bottom_left.png"),
            "bottom": self.load_tile("bubble_bottom.png"),
            "bottom_right": self.load_tile("bubble_bottom_right.png"),
        }

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )
        self.label.setFont(QFont("Inter", 11))
        self.label.setStyleSheet("""
            QLabel {
                color: #1b1b1b;
                background: transparent;
            }
        """)

        self.hide()

    def load_tile(self, filename):
        path = os.path.join(self.assets_dir, filename)
        pixmap = QPixmap(path)

        if pixmap.isNull():
            log("Missing bubble tile:", path)
            return QPixmap()

        return pixmap.scaled(
            self.tile_px,
            self.tile_px,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

    def set_text(self, text):
        self.text = text.strip()

        if not self.text:
            self.hide()
            return

        self.label.setText(self.text)
        self.update_size()
        self.show()
        self.update()

    def update_size(self):
        font_metrics = QFontMetrics(self.label.font())

        text_rect = font_metrics.boundingRect(
            QRect(0, 0, self.max_text_width, 10000),
            Qt.TextFlag.TextWordWrap,
            self.text
        )

        text_width = min(
            max(text_rect.width(), self.tile_px * 3),
            self.max_text_width
        )

        text_height = max(text_rect.height(), self.tile_px)

        bubble_width = self.snap_to_tile(text_width + self.padding_x * 2)
        bubble_height = self.snap_to_tile(text_height + self.padding_y * 2)

        self.setFixedSize(bubble_width, bubble_height)

        self.label.setGeometry(
            self.padding_x,
            self.padding_y,
            bubble_width - self.padding_x * 2,
            bubble_height - self.padding_y * 2
        )

    def snap_to_tile(self, value):
        remainder = value % self.tile_px

        if remainder == 0:
            return value

        return value + (self.tile_px - remainder)

    def paintEvent(self, event):
        if not self.text:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

        self.draw_bubble_body(painter, self.width(), self.height())

    def draw_bubble_body(self, painter, width, height):
        tile = self.tile_px

        self.draw_tile(painter, "top_left", 0, 0)
        self.draw_tile(painter, "top_right", width - tile, 0)
        self.draw_tile(painter, "bottom_left", 0, height - tile)
        self.draw_tile(painter, "bottom_right", width - tile, height - tile)

        for x in range(tile, width - tile, tile):
            self.draw_tile(painter, "top", x, 0)
            self.draw_tile(painter, "bottom", x, height - tile)

        for y in range(tile, height - tile, tile):
            self.draw_tile(painter, "left", 0, y)
            self.draw_tile(painter, "right", width - tile, y)

        for x in range(tile, width - tile, tile):
            for y in range(tile, height - tile, tile):
                self.draw_tile(painter, "center", x, y)

    def draw_tile(self, painter, tile_name, x, y):
        pixmap = self.tiles.get(tile_name)

        if pixmap and not pixmap.isNull():
            painter.drawPixmap(x, y, pixmap)
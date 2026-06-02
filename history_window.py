import json
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase, QPixmap, QPainter
from PyQt6.QtWidgets import(
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame
)

class HistoryWindow(QWidget):
    def __init__(self, history_path="history.json", parent=None):
        super().__init__(parent)

        self.history_path = history_path
        self.entries = []

        self.window_pixmap = QPixmap("history_window/pixil-frame-0 (2).png")
        
        font_id = QFontDatabase.addApplicationFont("assets\fonts\press-start-2p.ttf")

        self.setup_window()
        self.setup_ui()
        self.load_history()
        self.render_entries()

    def setup_window(self):
        self.setWindowTitle("Orion Histoy")
        self.setFixedSize(320, 280)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setStyleSheet(
            """
              QWidget {
                background-color: #0d0d0d;
                color: #FFF9E2;
                font-family: "Courier New", monospace;
            }

            QLabel#title {
                color: #FFEFAD;
                font-size: 12px;
                font-family: "Press Start 2P", "Courier New", monospace;
            }

            QLabel#empty {
                color: #414245;
                font-size: 11px;
            }

            QFrame#item {
                background-color: #111214;
                border: 1px solid #414245;
            }

            QLabel#item_text {
                color: #FFF9E2;
                font-size: 11px;
            }

            QLabel#item_meta {
                color: #3666CB;
                font-size: 10px;
            }

            QPushButton {
                background-color: #FFEFAD;
                color: #0d0d0d;
                border: none;
                padding: 6px 10px;
                font-size: 8px;
                font-family: "Press Start 2P", "Courier New", monospace;
            }

            QPushButton:hover {
                background-color: #FFF9E2;
            }

            QPushButton:pressed {
                background-color: #e8d88a;
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: #111214;
                width: 8px;
            }

            QScrollBar::handle:vertical {
                background: #3666CB;
            }
        """)

    def setup_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(12,12,12,12)
        root.setSpacing(8)

        header = QHBoxLayout()

        title = QLabel("HISTORY")
        title.setObjectName("title")

        close_button = QPushButton("X")
        close_button.setFixedSize(28, 24)
        close_button.clicked.connect(self.close)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(close_button)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.content = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(6)
        self.content.setLayout(self.content_layout)
        self.scroll.setWidget(self.content)

        root.addLayout(header)
        root.addWidget(self.scroll)
        self.setLayout(root)

    def load_history(self):
        if not os.path.exists(self.history_path):
            self.entries = []
            return
        try:
            with open(self.history_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                self.entries = data
            else:
                self.entries = []
        except Exception as error:
            print("No se pudo leer el historial", error)
            self.entries = []

    def render_entries(self):

        self.clear_entries()

        if not self.entries:
            empty = QLabel("No hay historial todavia")
            empty.setObjectName("empty")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.addWidget(empty)
            self.content_layout.addStretch()
            return
        for entry in reversed(self.entries[-20:]):
            self.content_layout.addWidget(self.create_entry_widget(entry))
        self.content_layout.addStretch()

    def clear_entries(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def create_entry_widget(self, entry):
        frame = QFrame()
        frame.setObjectName("item")

        layout = QVBoxLayout()
        layout.setContentsMargins(8,6,8,6)
        layout.setSpacing(3)

        text = entry.get("text", "Sin texto")
        engine = entry.get("engine", "")
        created_at = entry.get("created_at", "")

        text_label = QLabel(text)
        text_label.setObjectName("item_text")
        text_label.setWordWrap(True)

        meta_label = QLabel(f"{engine}  {created_at}".strip())
        meta_label.setObjectName("item_meta")
        meta_label.setWordWrap(True)

        layout.addWidget(text_label)

        if engine or created_at:
            layout.addWidget(meta_label)

        frame.setLayout(layout)

        return frame
    
    def refresh(self):
        self.load_history()
        self.render_entries()
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)

        if not self.window_pixmap.isNull():
            painter.drawPixmap(0,0, self.window_pixmap)
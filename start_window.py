from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

from config import WHISPER_MODEL, WHISPER_LANGUAGE, OLLAMA_MODEL, OLLAMA_URL, APP_LANGUAGE

class StartWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.avatar_window = None
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        self.setWindowTitle("ORION Launcher")
        self.resize(760, 460)
        self.setWindowIcon(QIcon("assets/icon.ico"))

        self.setStyleSheet(
            """
            Qwidget{
            background-color: #101010;
            color: #f4f1de;
            font-family: Consolas;
            }

            QLabel#title{
            color: #ffd84d;
            font-size: 64px;
            font-weight: bold;
            }

            QLabel#subtitle{
            color: #d98f64;
            font-size: 15px
            }

            QLabel#terminal{
            color: #f4f1de;
            font-size: 14px;
            border: 2px solid #5b3a32;
            padding: 18px;
            background-color: #151515;
            }

            QPushButton{
            color: #101010;
            backgroun-color: #ff84d;
            border: 2px solid #8a6d1d;
            padding: 10px 18px;
            font-size: 14px;
            font-weight: bold;
            }

            QPushButton:hover{
            background-color: #ffe377;
            }

            QPushButton:hover{
            backgroun-color: #cfa2f;
            }
            """
        )
    def setup_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(18)

        header = QHBoxLayout()

        title_box = QVBoxLayout()
        title_box.setSpacing(4)
        title = QLabel("ORION")
        title.setObjectName("title")

        subtitle = QLabel("local voice + text assitant")
        subtitle.setObjectName("subtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        header.addLayout(title_box)
        header.addStretch()

        terminal = QLabel(self.build_status_text())
        terminal.setObjectName("terminal")
        terminal.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        launch_button = QPushButton("Lanunc ORION")
        launch_button.clicked.connect(self.launch_orion)

        root.addLayout(header)
        root.addWidget(terminal)
        root.addStretch()
        root.addWidget(launch_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(root)

    def build_status_text(self):
        return(
            "> booting ORION\\n"
            "> checking local configuration\\n\\n"
            f"voice engine      whisper {WHISPER_MODEL}\\n"
            f"voice language    {WHISPER_LANGUAGE}\\n"
            f"intent engine     {OLLAMA_MODEL}\\n"
            f"ollama endpoint   {OLLAMA_URL}\\n"
            f"app language      {APP_LANGUAGE}\\n"
            "input modes       voice + text\\n\\n"
            "> status: ready"
        )
    
    def launch_orion(self):
        self.avatar_window = AvatarWindow()
        self.avatar_window.show()
        self.close()
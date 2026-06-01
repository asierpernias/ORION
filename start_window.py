from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame

from ui import AvatarWindow

from config import WHISPER_MODEL, WHISPER_LANGUAGE, OLLAMA_MODEL, OLLAMA_URL, APP_LANGUAGE

class StartWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.avatar_window = None
        self._cursor_visible = True
        self.setup_window()
        self.setup_ui()
        self.start_cursor_blink()

    def setup_window(self):
        self.setWindowTitle("ORION Launcher")
        screen = QGuiApplication.primaryScreen().availableGeometry()

        width = int(screen.width() * 0.62)
        height = int(screen.height() * 0.58)

        width = max(720, min(width, 980))
        height = max(440, min(height, 640))

        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2

        self.setGeometry(x, y, width, height)
        self.setWindowIcon(QIcon("assets/icon.ico"))

        self.setStyleSheet(
            """
            Qwidget{
            background-color: #101010;
            color: #FFF9E2;
            font-family: "Courier New", Courier, monospace;
            }

            QLabel#title{
            color: #FFEFAD;
            font-size: 58px;
            font-weight: bold;
            font-family: "Courier New", Courier, monospace;
            letter-spacing:3px;
            }

            QLabel#subtitle{
            color: #FFEFAD;
            font-size: 15px
            letter-spacing: 1px;
            font-family: "Courier New", Courier, monospace;
            }

            QLabel#ascii{
            color: #3666CB;
            font-size:10px
            font-family: "Courier New", Courier, monospace;
            liner-height: 1.2;
            }

            QFrame#terminal_box{
            border: 2px solid #414245;
            background-color: #111214
            }

            QLabel#terminal{
            color: #FFF9E2;
            font-size: 13px;
            font-family: "Courier New", Courier, monospace
            border: none;
            padding: 0px;
            background-color: transparent;
            }

            QLabel#prompt{
            color: #FFEFAD;
            font-size: 13px;
            font-family: "Courier New", Courier, monospace;
            }

            QLabel#model_tag{
            color: #414245;
            font-size:11px;
            font-family: "Courier New", Courier, monospace;
            }

            QLabel#agent_tag{
            color: #0d0d0d;
            background-color: #3666CB;
            font-size: 10px;
            font-weight: bold;
            padding: 4px 8px;
            font-family: "Courier New", Courier, monospace;
            letter-spacing: 1px;
            }

            QPushButton{
            color: #0d0d0d;
            backgroun-color: #FFEFAD;
            border: none;
            padding: 12px 12px;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 2px;
            font-family: "Courier New", Courier, monospace;
            }

            QPushButton:hover{
            background-color: #FFF9E2;
            }

            QPushButton:hover{
            backgroun-color: #e8d88a;
            padding: 14px 20px 10px 24px;
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

        subtitle = QLabel("local AI powered desktop assistant")
        subtitle.setObjectName("subtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        ascii_art = QLabel(
             "     .---.  \n"
            "       [*] [*] \n"
            "       |[___]| \n"
            "  [-]  | ### |   [-] \n"
            "       |_____| \n"
            "         \n"
            
        )

        ascii_art.setObjectName("ascii")
        ascii_art.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        header.addLayout(title_box)
        header.addStretch()
        header.addWidget(ascii_art)

        terminal_frame = QFrame()
        terminal_frame.setObjectName("terminal_box")
        terminal_layout = QVBoxLayout(terminal_frame)
        terminal_layout.setContentsMargins(20, 18, 20, 18)
        terminal_layout.setSpacing(0)

        self.prompt_label = QLabel("> ask orion anything... /u2588")
        self.prompt_label.setObjectName("name")

        footer = QHBoxLayout()
        footer.setSpacing(10)

        left_footer = QVBoxLayout()
        left_footer.setSpacing(4)

        model_tag = QLabel(f"{OLLAMA_MODEL} · ollama/{OLLAMA_MODEL} ")
        model_tag.setObjectName("model_tag")

        agent_tag = QLabel("◆ agent mode")
        agent_tag.setObjectName("agent_tag")
        agent_tag.setFixedHeight(22)

        left_footer.addWidget(model_tag)
        left_footer.addWidget(agent_tag)

        launch_button = QPushButton("▶  Launch ORION")
        launch_button.setFixedHeight(42)
        launch_button.clicked.connect(self.launch_orion)

        footer.addLayout(left_footer)
        footer.addStretch()
        footer.addWidget(launch_button, alignment=Qt.AlignmentFlag.AlignBottom)


        root.addLayout(header)
        root.addWidget(terminal_frame)
        root.addWidget(self.prompt_label)
        root.addStretch()
        root.addLayout(footer)

        self.setLayout(root)

    def build_status_text(self):

        o = "#FFEFAD"
        g = "#3666CB"
        w = "#FFF9E2"

        def row(key, val):
            return(
                f'<span style="color:{w}; font-family: Courier New, monospace;>'
                f'<span style="display:inline-block; min-width:180px;">{key} </span>'
                f'<span style="color:{w}; ">{val}</span><br>'

            )
        
        return(
            f'<span style="color:{o}; font-family:Courier New,monospace;">&gt; booting ORION</span><br>'
            f'<span style="color:{o}; font-family:Courier New,monospace;">&gt; checking local configuration</span><br><br>'
            + row("voice engine", f"whisper {WHISPER_MODEL}")
            + row("voice language", WHISPER_LANGUAGE)
            + row("intent engine", OLLAMA_MODEL)
            + row("ollama endpoint", OLLAMA_URL)
            + row("app language", APP_LANGUAGE)
            + row("input modes", "voice + text")
            + f'<br><span style="color:{o}; font-family:Courier New,monospace;">&gt; status: </span>'
            + f'<span style="color:{g}; font-weight:bold; font-family:Courier New,monospace;">ready</span>'
        )
        
    def start_cursor_blink(self):
        self._cursor_timer = QTimer(self)
        self._cursor_timer.timeout.connect(self._blink_cursor)
        self._cursor_timer.start(530)

    def _blink_cursor(self):
        self._cursor_visible = not self._cursor_visible
        cursor = "\u2588" if self._cursor_visible else ""
        self.prompt_label.setText(f">ask orion anything... {cursor}")
                      


    
    
    def launch_orion(self):
        self.avatar_window = AvatarWindow()
        self.avatar_window.show()
        self.close()

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QGuiApplication, QIcon, QFontDatabase
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame

from i18n import t

from ui import AvatarWindow
from config import WHISPER_MODEL, WHISPER_LANGUAGE, OLLAMA_MODEL, OLLAMA_URL, APP_LANGUAGE


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.avatar_window = None
        self._cursor_visible = True
        QFontDatabase.addApplicationFont("assets/fonts/press-start-2p.ttf")
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

        self.setStyleSheet("""
            QWidget {
                background-color: #0d0d0d;
                color: #FFF9E2;
                font-family: "Courier New", Courier, monospace;
            }

            QLabel#title {
                color: #FFEFAD;
                font-size: 28px;
                font-weight: bold;
                font-family: "Press Start 2P", Courier, monospace;
                letter-spacing: 3px;
            }

            QLabel#subtitle {
                color: #FFEFAD;
                font-size: 15px;
                letter-spacing: 1px;
                font-family: "Courier New", Courier, monospace;
            }

            QLabel#ascii {
                color: #3666CB;
                font-size: 8px;
                font-family: "Press Start 2P", Courier, monospace;
                line-height: 1.2;
            }

            QFrame#terminal_box {
                border: 2px solid #414245;
                background-color: #111214;
            }

            QLabel#terminal {
                color: #FFF9E2;
                font-size: 13px;
                font-family: "Courier New", Courier, monospace;
                border: none;
                padding: 0px;
                background-color: transparent;
            }

            QLabel#prompt {
                color: #FFEFAD;
                font-size: 13px;
                font-family: "Courier New", Courier, monospace;
            }

            QLabel#model_tag {
                color: #414245;
                font-size: 11px;
                font-family: "Courier New", Courier, monospace;
            }

            QLabel#agent_tag {
                color: #0d0d0d;
                background-color: #3666CB;
                font-size: 10px;
                font-weight: bold;
                padding: 4px 8px;
                font-family: "Courier New", Courier, monospace;
                letter-spacing: 1px;
            }

            QPushButton {
                color: #0d0d0d;
                background-color: #FFEFAD;
                border: none;
                padding: 12px 22px;
                font-size: 8px;
                font-weight: bold;
                letter-spacing: 2px;
                font-family: "Press Start 2P", Courier, monospace;
            }

            QPushButton:hover {
                background-color: #FFF9E2;
            }

            QPushButton:pressed {
                background-color: #e8d88a;
                padding: 14px 20px 10px 24px;
            }

            QPushButton#config_btn {
                color: #FFEFAD;
                background-color: transparent;
                border: 1px solid #414245;
                padding: 4px 10px;
                font-size: 8px;
                font-family: "Press Start 2P", "Courier New", monospace;
                letter-spacing: 1px;
            }

            QPushButton#config_btn:hover {
                border-color: #FFEFAD;
            }
        """)

    def setup_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(18)

        header = QHBoxLayout()

        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        title = QLabel("ORION")
        title.setObjectName("title")

        subtitle = QLabel(t("subtitle"))
        subtitle.setObjectName("subtitle")
        self.subtitle_label = subtitle

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        ascii_art = QLabel(
            "  .---.  \n"
            " [*] [*] \n"
            " |[___]| \n"
            " | ### | \n"
            " |_____| \n"
            "  /   \  \n"
            " [_] [_] "
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

        terminal = QLabel(self.build_status_text())
        terminal.setObjectName("terminal")
        terminal.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        terminal.setTextFormat(Qt.TextFormat.RichText)
        terminal_layout.addWidget(terminal)
        self.terminal_label = terminal

        config_button = QPushButton(t("config_btn"))
        config_button.setObjectName("config_btn")
        config_button.setFixedHeight(28)
        config_button.clicked.connect(self.open_config)
        terminal_layout.addSpacing(10)
        terminal_layout.addWidget(config_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.prompt_label = QLabel(t("prompt") + "\u2588")
        self.prompt_label.setObjectName("prompt")

        footer = QHBoxLayout()
        footer.setSpacing(10)

        left_footer = QVBoxLayout()
        left_footer.setSpacing(4)

        model_tag = QLabel(f"{OLLAMA_MODEL} · ollama/{OLLAMA_MODEL}")
        model_tag.setObjectName("model_tag")

        agent_tag = QLabel("◆ agent mode")
        agent_tag.setObjectName("agent_tag")
        agent_tag.setFixedHeight(22)

        left_footer.addWidget(model_tag)
        left_footer.addWidget(agent_tag)

        launch_button = QPushButton(t("launch"))
        launch_button.setFixedHeight(42)
        launch_button.clicked.connect(self.launch_orion)
        self.launch_button = launch_button
        
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
        import config
        o = "#FFEFAD"
        g = "#3666CB"
        w = "#FFF9E2"

        def row(key, val):
            return (
                f'<span style="color:{w}; font-family:Courier New,monospace;">'
                f'<span style="display:inline-block; min-width:180px;">{key}</span>'
                f'<span style="color:{w};">{val}</span></span><br>'
            )

        return (
            f'<span style="color:{o}; font-family:Courier New,monospace;">&gt; booting ORION</span><br>'
            f'<span style="color:{o}; font-family:Courier New,monospace;">&gt; checking local configuration</span><br><br>'
            + row(t("voice engine"), f"whisper {config.WHISPER_MODEL}")
            + row(t("voice language"), config.WHISPER_LANGUAGE)
            + row(t("intent engine"), config.OLLAMA_MODEL)
            + row(t("endpoint"), config.OLLAMA_URL)
            + row(t("app language"),config. APP_LANGUAGE)
            + row(t("input modes"), "voice + text")
            + f'<br><span style="color:{o}; font-family:Courier New,monospace;">&gt; status: </span>'
            + f'<span style="color:{g}; font-weight:bold; font-family:Courier New,monospace;">ready</span>'
            )
    def _refresh_terminal(self):
        self.terminal_label.setText(self.build_status_text())
        self.subtitle_label.setText(t("subtitle"))
        self.launch_button.setText(t("launch"))
        self.prompt_label.setText(t("prompt") + "\u2588")
        
    def start_cursor_blink(self):
        self._cursor_timer = QTimer(self)
        self._cursor_timer.timeout.connect(self._blink_cursor)
        self._cursor_timer.start(530)

    def _blink_cursor(self):
        self._cursor_visible = not self._cursor_visible
        cursor = "\u2588" if self._cursor_visible else " "
        self.prompt_label.setText(f"> ask orion anything...{cursor}")

    def open_config(self):
        from PyQt6.QtWidgets import QDialog, QComboBox, QFormLayout, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("ORION config")
        dialog.setFixedWidth(360)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #0d0d0d;
                color: #FFF9E2;
                font-family: "Courier New", Courier, monospace;
            }
            QLabel {
                color: #FFEFAD;
                font-size: 8px;
                font-family: "Press Start 2P", "Courier New", monospace;
            }
            QComboBox {
                background-color: #111214;
                color: #FFF9E2;
                border: 1px solid #414245;
                padding: 6px;
                font-size: 8px;
                font-family: "Press Start 2P", "Courier New", monospace;
            }
            QComboBox:hover { border-color: #FFEFAD; }
            QComboBox QAbstractItemView {
                background-color: #111214;
                color: #FFF9E2;
                selection-background-color: #3666CB;
            }
            QPushButton {
                color: #0d0d0d;
                background-color: #FFEFAD;
                border: none;
                padding: 8px 16px;
                font-size: 8px;
                font-family: "Press Start 2P", "Courier New", monospace;
            }
            QPushButton:hover { background-color: #FFF9E2; }
        """)

        form = QFormLayout(dialog)
        form.setSpacing(14)
        form.setContentsMargins(20, 20, 20, 20)

        combo_model = QComboBox()
        combo_model.addItems(["small", "medium", "large"])
        combo_model.setCurrentText(WHISPER_MODEL)

        combo_whisper_lang = QComboBox()
        combo_whisper_lang.addItems(["es", "en"])
        combo_whisper_lang.setCurrentText(WHISPER_LANGUAGE)

        combo_app_lang = QComboBox()
        combo_app_lang.addItems(["es", "en"])
        combo_app_lang.setCurrentText(APP_LANGUAGE)

        form.addRow("whisper model", combo_model)
        form.addRow("whisper lang", combo_whisper_lang)
        form.addRow("app language", combo_app_lang)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            import config
            config.WHISPER_MODEL    = combo_model.currentText()
            config.WHISPER_LANGUAGE = combo_whisper_lang.currentText()
            config.APP_LANGUAGE     = combo_app_lang.currentText()

            self._write_config(
                config.WHISPER_MODEL,
                config.WHISPER_LANGUAGE,
                config.APP_LANGUAGE
            )
            self._refresh_terminal()

    def _write_config(self, whisper_model, whisper_language, app_language):
        import re

        path = "config.py"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(r'WHISPER_MODEL\s*=\s*".*?"',    f'WHISPER_MODEL = "{whisper_model}"',      content)
        content = re.sub(r'WHISPER_LANGUAGE\s*=\s*".*?"', f'WHISPER_LANGUAGE = "{whisper_language}"', content)
        content = re.sub(r'APP_LANGUAGE\s*=\s*".*?"',     f'APP_LANGUAGE = "{app_language}"',         content)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        import threading
        from ORION import reload_model
        t = threading.Thread(target=reload_model, daemon=True)
        t.start()

    def launch_orion(self):
        self.avatar_window = AvatarWindow()
        self.avatar_window.show()
        self.close()

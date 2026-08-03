import ctypes
import logging
import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from ..core.paths import resource_path
from .ui import StartWindow

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = PROJECT_ROOT / "data" / "orion.log"


def main():
    app_id = "orion.macondo.avatar.1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("assets\\icon.ico")))

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    window = StartWindow()
    window.setWindowIcon(QIcon(resource_path("assets\\icon.ico")))
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
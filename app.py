import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui import AvatarWindow
from start_window import StartWindow


if __name__ == "__main__":

    app_id = "orion.macondo.avatar.1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets\icon.ico"))

    window = StartWindow()
    window.setWindowIcon(QIcon("assets\icon.ico"))
    window.show()

    sys.exit(app.exec())
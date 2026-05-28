import sys
from PyQt6.QtWidgets import QApplication
from ui import AvatarWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AvatarWindow()
    window.show()

    sys.exit(app.exec())
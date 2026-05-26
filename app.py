import sys

from PyQt6.QtWidgets import QApplication

from ui import AvatarWindow


app = QApplication(sys.argv)

window = AvatarWindow()

window.show()

app.exec()
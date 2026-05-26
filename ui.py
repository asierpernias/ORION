from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from ORION import run_orion, open_search


class AvatarWindow(QWidget):

    

    def __init__(self):
        super().__init__()

        self.drag_position = None

        self.setup_window()
        self.setup_avatar()
        self.setWindowIcon(QIcon("icon.ico"))
        self.processing = False

    def setup_window(self):

        self.setWindowTitle("ORION")

        self.resize(256, 256)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    def setup_avatar(self):

        self.avatar = QLabel(self)

        pixmap = QPixmap(
            r"C:\Users\ague_\Desktop\programacion\macondo_hackclub\ORION\assets\idle.png"
        )

        self.avatar.setPixmap(pixmap)

        self.avatar.resize(pixmap.width(), pixmap.height())


    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

 
    def mouseMoveEvent(self, event):

        if self.drag_position is not None:

            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

 
    def mouseReleaseEvent(self, event):

        self.drag_position = None

    def mouseDoubleClickEvent(self, event):

        if self.processing == True:
            print("ORION is already running")
            return
        

        self.processing = True

        print("Doble click detectado → ejecutando ORION")

        result = run_orion()

        print(result)

        if result:
            open_search(result["intent"]) 
            
        self.processing = False
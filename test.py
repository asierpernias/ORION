from PyQt6.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)

w = QWidget()
w.setWindowTitle("TEST ORION")
w.resize(300, 200)
w.show()

app.exec()
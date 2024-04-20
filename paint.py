from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint, QRect
import sys


class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pixmap = QPixmap(600, 600)
        self.pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self.pixmap)
        self.setMouseTracking(True)
        self.drawing = False
        self.last_mouse_position = QPoint()


    # Mouse events
    def mouseMoveEvent(self, event):
        mouse_position = event.pos()
        if(event.buttons() and Qt.MouseButton.LeftButton) and self.drawing:
            self.draw(mouse_position)
        print(mouse_position)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_position = event.pos()
            self.drawing = True
            print("Left click at" + str(event.pos()))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
            print("Left release at" + str(event.pos()))

    # Drawing function
    def draw(self, points):
        painter = QPainter(self.pixmap)
        pen = QtGui.QPen(Qt.GlobalColor.black, 5)
        painter.setPen(pen)

        painter.drawLine(self.last_mouse_position, points)
        self.last_mouse_position = points
        self.update()

    # Paint function
    def paintEvent(self, event):
        painter = QPainter(self)
        target_rect = QRect()
        target_rect = event.rect()
        painter.drawPixmap(target_rect, self.pixmap, target_rect)
        painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(600, 600)
        self.setWindowTitle('Paint App')

        canvas = Canvas()
        self.setCentralWidget(canvas)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
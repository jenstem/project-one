from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QStatusBar, QToolBar
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
import sys


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pixmap = QPixmap(600, 600)
        self.pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self.pixmap)
        self.setMouseTracking(True)
        self.drawing = False
        self.last_mouse_position = QPoint()
        self.status_label = QLabel()


    # Mouse events
    def mouseMoveEvent(self, event):
        mouse_position = event.pos()
        status_text = f"Mouse coordinates are X: {mouse_position.x()}, Y: {mouse_position.y()}"
        self.status_label.setText(status_text)
        self.parent.statusBar.addWidget(self.status_label)
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

        # Canvas
        canvas = Canvas(self)
        self.setCentralWidget(canvas)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Toolbar
        tool_bar = QToolBar("Toolbar")
        tool_bar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, tool_bar)
        tool_bar.setMovable(False)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
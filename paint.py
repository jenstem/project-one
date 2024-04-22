from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QStatusBar, QToolBar, QColorDialog, QAction, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QIcon
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
import sys
import os


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
        self.eraser = False
        self.pen_color = Qt.GlobalColor.black
        self.pen_width = 1


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
        if self.eraser == False:
            pen = QPen(self.pen_color, self.pen_width)
            painter.setPen(pen)

            painter.drawLine(self.last_mouse_position, points)
            self.last_mouse_position = points

        elif self.eraser == True:
            eraser = QRect(points.x(), points.y(), 10, 10)
            painter.eraseRect(eraser)

        self.update()

    # Paint function
    def paintEvent(self, event):
        painter = QPainter(self)
        target_rect = QRect()
        target_rect = event.rect()
        painter.drawPixmap(target_rect, self.pixmap, target_rect)
        painter.end()


    def selectTool(self, tool):
        if tool == "pencil":
            self.pen_width = 2
            self.eraser = False
        elif tool == "marker":
            self.pen_width = 4
            self.eraser = False
        elif tool == "eraser":
            self.pen_width = 10
            self.eraser = True
        elif tool == "color":
            self.eraser = False
            color = QColorDialog.getColor()
            self.pen_color = color


    # New canvas
    def new(self):
        self.pixmap.fill(Qt.GlobalColor.white)
        self.update()


    # Save canvas
    def save(self):
        file_name = QFileDialog.getSaveFileName(self, "Save As", os.path.curdir + "image.png", "PNG File(*.png)")
        if file_name:
            self.pixmap.save(file_name, "png")


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

        # Actions
        pencil_art = QAction(QIcon("icons/pencil.png"), "Pencil", tool_bar)
        pencil_art.triggered.connect(lambda: canvas.selectTool("pencil"))
        marker_art = QAction(QIcon("icons/marker.png"), "Marker", tool_bar)
        marker_art.triggered.connect(lambda: canvas.selectTool("marker"))
        eraser_act = QAction(QIcon("icons/eraser.png"), "Eraser", tool_bar)
        eraser_act.triggered.connect(lambda: canvas.selectTool("eraser"))
        color_act = QAction(QIcon("icons/colors.png"), "Colors", tool_bar)
        color_act.triggered.connect(lambda: canvas.selectTool("color"))

        tool_bar.addAction(pencil_art)
        tool_bar.addAction(marker_art)
        tool_bar.addAction(eraser_act)
        tool_bar.addAction(color_act)


        # Menu bar
        self.new_act = QAction("New", self)
        self.new_act.triggered.connect(lambda: canvas.new())
        self.save_file_act = QAction("Save", self)
        self.save_file_act.triggered.connect(lambda: canvas.pixmap.save("image.png"))
        self.quit_act = QAction("Exit", self)
        self.quit_act.triggered.connect(self.close)

        self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_act)
        file_menu.addAction(self.save_file_act)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_act)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
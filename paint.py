from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QStatusBar, QToolBar, QColorDialog, QAction, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QIcon
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
import sys
import os


class Canvas(QLabel):
    """
    A class to represent a drawing canvas where users can draw shapes and lines.
    Inherits from QLabel to utilize its features for displaying the drawing.
    """
    def __init__(self, parent):
        """
        Initializes the Canvas with a parent widget and sets up the user interface.

        Parameters:
        parent (QWidget): The parent widget for the Canvas.
        """
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    
    def initUI(self):
        """
        Initializes the user interface components of the Canvas.
        Sets up the pixmap, mouse tracking, and default drawing settings.
        """
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


    def mouseMoveEvent(self, event):
        """
        Handles mouse movement events on the Canvas.

        Parameters:
            event (QMouseEvent): The mouse event containing position data.
        """
        mouse_position = event.pos()
        status_text = f"Mouse coordinates are X: {mouse_position.x()}, Y: {mouse_position.y()}"
        self.status_label.setText(status_text)
        self.parent.statusBar.addWidget(self.status_label)
        if(event.buttons() and Qt.MouseButton.LeftButton) and self.drawing:
            self.draw(mouse_position)
        print(mouse_position)

    
    def mousePressEvent(self, event):
        """
        Handles mouse press events on the Canvas.

        Parameters:
            event (QMouseEvent): The mouse event containing button data.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_position = event.pos()
            self.drawing = True
            print("Left click at" + str(event.pos()))

    
    def mouseReleaseEvent(self, event):
        """
        Handles mouse release events on the Canvas.

        Parameters:
            event (QMouseEvent): The mouse event containing button data.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
            print("Left release at" + str(event.pos()))


    def draw(self, points):
        """
        Draws on the Canvas based on the current tool and mouse position.

        Parameters:
            points (QPoints): The current mouse position for drawing.
        """
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

    
    def paintEvent(self, event):
        """
        Paints the current pixmap onto the Canvas.

        Parameters:
            event (QPaintEvent): The paint event containing the area to be repainted.
        """
        painter = QPainter(self)
        target_rect = QRect()
        target_rect = event.rect()
        painter.drawPixmap(target_rect, self.pixmap, target_rect)
        painter.end()


    def selectTool(self, tool):
        """
        Selects the drawing tool based on user input.

        Parameters:
            tool (str): The name of the tool to be selected (e.g. pencil, marker, eraser, color).
        """
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


    def new(self):
        """
        Clears the Canvas and fills it with a white background.
        """
        self.pixmap.fill(Qt.GlobalColor.white)
        self.update()


    def save(self):
        """
        Saves the current drawing on the Canvas to a file.
        Prompts the user to select a file location and name.
        """
        file_name = QFileDialog.getSaveFileName(self, "Save As", os.path.curdir + "image.png", "PNG File(*.png)")
        if file_name:
            self.pixmap.save(file_name, "png")


class MainWindow(QMainWindow):
    """
    A class to represent the main window of the Paint application.
    Inherits from QMainWindow to provide a framework for the application.
    """
    def __init__(self):
        """
        Initializes the MainWindow and sets up the user interface.
        """
        super().__init__()
        self.initUI()

    
    def initUI(self):
        """
        Initializes the user interface components of the MainWindow.
        Sets up the Canvas, status bar, toolbar, and menu actions.
        """
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

from PyQt5.QtWidgets import QMainWindow, QApplication
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setMinimumSize(400, 400)
        self.setWindowTitle('Paint App')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
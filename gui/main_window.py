from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys

from gui.frames.main_frame import MainFrame


class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.app = app
        self.setWindowTitle("学习认字")
        self.setFixedSize(800, 600)

        self.main_frame = MainFrame()
        self.setCentralWidget(self.main_frame)

    def start_app(self):
        self.show()
        sys.exit(self.app.exec_())

    @Slot()
    def exit_app(self):
        QApplication.quit()

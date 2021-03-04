from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys

from gui_py.top_frame import TopFrame


class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.app = app
        self.setWindowTitle("学习认字")
        self.top_frame = TopFrame()

        self.setCentralWidget(self.top_frame)
        self.setFixedSize(600, 400)

    def start_app(self):
        self.show()
        sys.exit(self.app.exec_())

    @Slot()
    def exit_app(self):
        QApplication.quit()

from PySide6.QtWidgets import *
from gui_py.main_window import MainWindow
import sys


if __name__ == "__main__":
    window = MainWindow(QApplication(sys.argv))
    window.start_app()

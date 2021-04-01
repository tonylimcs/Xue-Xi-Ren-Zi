from PySide6.QtWidgets import *
from gui.main_window import MainWindow


if __name__ == "__main__":
    window = MainWindow(QApplication())
    window.start_app()

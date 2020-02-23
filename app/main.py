# pylint: disable=C0103

"""
Starting point of the app where window displays
"""
import sys

from PySide2.QtWidgets import QApplication

from ui.app import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec_())

# This Python file uses the following encoding: utf-8

import sys
from PyQt5.QtWidgets import QApplication
from window import Window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec_())


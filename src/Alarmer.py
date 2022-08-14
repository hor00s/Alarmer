#!/bin/env python3
import sys
from mainwindow.uialarm import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Alarm = UI()
    sys.exit(app.exec_())

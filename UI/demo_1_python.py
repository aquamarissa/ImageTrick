import sys

from PyQt5.QtWidgets import QDialog, QLabel
from qtconsole.mainwindow import MainWindow

from demo_1 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import glob
import moviepy.editor as mpy
import os
import subprocess
import cv2
from MapWindow import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.image_window = MapWindow()
        self.ui.pushButton.clicked.connect(self.setDepthLength)
        self.ui.pushButton.clicked.connect(self.image_window.createWindow)

    def setDepthLength(self):
        if self.ui.lineEdit_2.text():
            depth_length = float(self.ui.lineEdit_2.text())
            self.image_window.focus = depth_length
        else:
            return 0


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    map_window = MapWindow()
    height_window = Height()
    myapp.show()
    sys.exit(app.exec_())

import sys

from PyQt5.QtWidgets import QDialog, QLabel
from qtconsole.mainwindow import MainWindow

from demo_2 import *
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
        self.ui.pushButton.clicked.connect(self.setAllOptions)
        self.ui.pushButton.clicked.connect(self.image_window.createWindow)
        self.ui.pushButton_2.clicked.connect(self.selectFile)

    def selectFile(self):
        self.image_window.map = ''.join(QFileDialog.getOpenFileName()[0])

    def setAllOptions(self):
        self.image_window.focus = float(self.ui.lineEdit_2.text())
        self.image_window.parties_h = self.image_window.parties_h / int(self.ui.lineEdit_8.text())
        self.image_window.parties_w = self.image_window.parties_w / int(self.ui.lineEdit_9.text())
        self.image_window.height_cam = float(self.ui.lineEdit_3.text())
        self.image_window.weight_cam = float(self.ui.lineEdit_6.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    map_window = MapWindow()
    height_window = Height()
    myapp.show()
    sys.exit(app.exec_())

 # Посланіє: треба перенести усі значення з камери у клас мапи, а потім для кожної точки та її висоти визначати розміри
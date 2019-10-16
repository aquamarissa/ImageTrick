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
        self.start_acces = [True] * 10
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.image_window = MapWindow()
        self.ui.pushButton.clicked.connect(self.setAllOptions)
        self.ui.pushButton_2.clicked.connect(self.selectFile)

    def selectFile(self):
        self.image_window.map = ''.join(QFileDialog.getOpenFileName()[0])

    def setAllOptions(self):
        self.image_window.acces = True
        if self.image_window.map == '':
            self.start_acces[0] = False
        else:
            self.start_acces[0] = True

        if float(self.ui.lineEdit.text()) < 0:
            self.start_acces[1] = False
        else:
            self.image_window.height_point.max_height = float(self.ui.lineEdit.text())
            self.start_acces[1] = True

        if float(self.ui.lineEdit_2.text()) < 0:
            self.start_acces[2] = False
        else:
            self.image_window.focus = float(self.ui.lineEdit_2.text())
            self.start_acces[2] = True

        if int(self.ui.lineEdit_8.text()) < 0:
            self.start_acces[3] = False
        else:
            self.image_window.parties_h = self.image_window.parties_h / int(self.ui.lineEdit_8.text())
            self.start_acces[3] = True

        if int(self.ui.lineEdit_9.text()) < 0:
            self.start_acces[4] = False
        else:
            self.image_window.parties_w = self.image_window.parties_w / int(self.ui.lineEdit_9.text())
            self.start_acces[4] = True

        if float(self.ui.lineEdit_3.text()) < 0:
            self.start_acces[5] = False
        else:
            self.image_window.height_cam = float(self.ui.lineEdit_3.text())
            self.start_acces[5] = True

        if float(self.ui.lineEdit_6.text()) < 0:
            self.start_acces[6] = False
        else:
            self.image_window.weight_cam = float(self.ui.lineEdit_6.text())
            self.start_acces[6] = True

        if float(self.ui.lineEdit_7.text()) < 0 or float(self.ui.lineEdit_7.text()) > 100:
            self.start_acces[7] = False
        else:
            self.image_window.percent_start = float(self.ui.lineEdit_7.text())
            self.start_acces[7] = True

        if float(self.ui.lineEdit_5.text()) < 0 or float(self.ui.lineEdit_5.text()) > 100:
            self.start_acces[8] = False
        else:
            self.image_window.percent_per_hundred = float(self.ui.lineEdit_5.text())
            self.start_acces[8] = True

        if float(self.ui.lineEdit_4.text()) < 0 or float(self.ui.lineEdit_4.text()) > 100:
            self.start_acces[9] = False
        else:
            self.image_window.percent_per_photo = float(self.ui.lineEdit_4.text())
            self.start_acces[9] = True

        for i in self.start_acces:
            if not i:
                self.image_window.acces = False

        self.image_window.createWindow()

    def callError(self, message):
        QMessageBox.about(self, "Помилка", message)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    map_window = MapWindow()
    height_window = Height()
    myapp.show()
    sys.exit(app.exec_())

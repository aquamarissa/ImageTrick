# Todo: Додати обмеження на рух дрона(площа зображення)

import sys
from demo_0 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.area_bool = False
        self.image_bool = True
        self.x_move = 27
        self.y_move = 75
        self.x_length = 100
        self.y_length = 100
        self.ui.pushButton_5.clicked.connect(self.move_right)
        self.ui.pushButton_2.clicked.connect(self.move_up)
        self.ui.pushButton_3.clicked.connect(self.move_down)
        self.ui.pushButton_4.clicked.connect(self.move_left)
        self.ui.pushButton.clicked.connect(self.hide_interface)
        self.ui.pushButton_6.clicked.connect(self.show_interface)

    def hide_interface(self):
        self.ui.pushButton_2.hide()
        self.ui.pushButton_3.hide()
        self.ui.pushButton_4.hide()
        self.ui.pushButton_5.hide()
        self.ui.pushButton_8.hide()
        self.ui.pushButton_9.hide()
        self.ui.label.hide()
        self.ui.label_2.hide()
        self.ui.tabWidget.setGeometry(QtCore.QRect(20, 555, 751, 201))

    def show_interface(self):
        self.ui.pushButton_2.show()
        self.ui.pushButton_3.show()
        self.ui.pushButton_4.show()
        self.ui.pushButton_5.show()
        self.ui.pushButton_8.show()
        self.ui.pushButton_9.show()
        self.ui.label.show()
        self.ui.label_2.show()
        self.ui.tabWidget.setGeometry(QtCore.QRect(20, 355, 751, 201))

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image_bool:
            pixmap = QtGui.QPixmap()
            pixmap.load('images/2016_0101_000725_002.JPG')
            painter.drawPixmap(27, 75, 741, 451, pixmap)
            painter.setPen(QPen(Qt.green, 8, Qt.SolidLine))
            painter.drawRect(self.x_move, self.y_move, self.x_length, self.y_length)
            self.update()

    def move_right(self):
        self.x_move = self.x_move + 10

    def move_left(self):
        self.x_move = self.x_move - 10

    def move_up(self):
        self.y_move = self.y_move - 10

    def move_down(self):
        self.y_move = self.y_move + 10


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

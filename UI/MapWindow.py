# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from demo_1 import *
from demo_1_python import *
import math
import numpy as np


class Height(QDialog):
    def __init__(self, parent=None):
        super(Height, self).__init__(parent)
        self.enterHeight = QPushButton("Підтвердити")
        self.enterHeight.setGeometry(QtCore.QRect(240, 80, 250, 100))
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setGeometry(QtCore.QRect(20, 60, 150, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.height = 0
        layout = QHBoxLayout()
        layout.addWidget(self.enterHeight)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)
        self.enterHeight.clicked.connect(self.takeHeight)

    def takeHeight(self):
        if self.lineEdit.text():
            self.height = float(self.lineEdit.text())
        else:
            self.height = 0
        self.close()

    def createWindow(self):
        self.setGeometry(250, 100, 250, 100)
        self.setWindowTitle("Висота")
        self.show()


class MapWindow(QDialog):
    def __init__(self, parent=None):
        super(MapWindow, self).__init__(parent)
        self.points = []
        self.ways = [0]
        self.angels = []
        self.rects = []
        self.heights = []
        self.count = -1
        self.focus = 0.00
        self.height_point = Height()

    def createWindow(self):
        self.setGeometry(250, 250, 741, 451)
        self.setWindowTitle("Мапа")
        self.show()

    def mousePressEvent(self, event):
        print(self.focus)
        self.count += 1
        self.points.append(np.array([event.pos().x(), event.pos().y(), 0]))
        self.rects.append(self.focusArea(self.count))
        if self.count > 0:
            self.ways[0] = int((np.linalg.norm(self.points[self.count] - self.points[0]) + self.focus) /
                               self.focus)
            self.ways.append(int((np.linalg.norm(self.points[self.count - 1] - self.points[self.count]) + self.focus) /
                                 self.focus))
        self.height_point.createWindow()
        if self.count > 0:
            self.heights.append(self.height_point.height)
        else:
            self.heights.append(0)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pixmap = QtGui.QPixmap()
        pixmap.load('images/mapa.jpeg')
        painter.drawPixmap(0, 0, 741, 451, pixmap)
        painter.setPen(QPen(Qt.gray, 5, Qt.SolidLine))
        for i in range(len(self.points)):
            painter.drawEllipse(self.points[i][0], self.points[i][1], 8, 8)
            if len(self.points) > 1:
                line = QtCore.QLine(QtCore.QPoint(self.points[i - 1][0], self.points[i - 1][1]),
                                    QtCore.QPoint(self.points[i][0], self.points[i][1]))
                painter.drawLine(line)
            if i > 0:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(55, 60, 61, 100)))
                for j in range(self.ways[i]):
                    temp_point = self.findStepLine(self.points[i - 1], self.points[i], j)
                    painter.drawPolygon(
                        self.createPolygon(4, (math.sqrt(2 * self.focus ** 2) / 2),  # радіус рівний половині діагоналі
                                           self.angels[i], temp_point[0], temp_point[1]))

        painter.end()
        self.update()

    def focusArea(self, i):
        if len(self.points) > 2:
            a = self.points[i - 2]
            b = self.points[i - 1]
            c = self.points[i]
            vector_ba = b - a
            vector_bc = b - c
            mod_ba = np.linalg.norm(a - b)
            mod_bc = np.linalg.norm(c - b)
            scalar_ba_bc = np.dot(vector_ba, vector_bc)
            cos_b = scalar_ba_bc / (mod_ba * mod_bc)
            print(self.angels[len(self.angels)-1])
            print(math.degrees(math.acos(cos_b)) + self.angels[len(self.angels)-1])
            self.angels.append(-math.degrees(math.acos(cos_b)) + self.angels[len(self.angels)-1])
            #return self.findPolygonPoints(i)
        elif i == 0:
            self.angels.append(0)
        elif 3 > len(self.points) > 0:
            b = self.points[i - 1]
            c = self.points[i]
            a = np.array([c[0], b[1], 0])
            vector_ba = b - a
            vector_bc = b - c
            mod_ba = np.linalg.norm(a - b)
            mod_bc = np.linalg.norm(c - b)
            scalar_ba_bc = np.dot(vector_ba, vector_bc)
            cos_b = scalar_ba_bc / (mod_ba * mod_bc)
            print(self.angels[len(self.angels) - 1])
            print(math.degrees(math.acos(cos_b)) + self.angels[len(self.angels) - 1])
            self.angels.append(-math.degrees(math.acos(cos_b)) + self.angels[len(self.angels) - 1])

    def findPolygonPoints(self, i):
        f = self.focus
        polygon = QRect(self.points[i][1] - f / 2, self.points[i][2] - f / 2, f, f)
        return polygon

    def findStepLine(self, point1, point2, step): # points[i - 1], points[i]
        len = np.linalg.norm(point1 - point2)
        point3 = point1 + (point2 - point1) * ((step * self.focus) / len)
        return point3

    def createPolygon(self, n, r, s, x_coord, y_coord):
        polygon = QtGui.QPolygonF()
        w = 360 / n
        for i in range(n):
            t = w * i + s+45
            x = r * math.cos(math.radians(t))
            y = r * math.sin(math.radians(t))
            polygon.append(QtCore.QPointF(x_coord + x, y_coord + y))

        return polygon

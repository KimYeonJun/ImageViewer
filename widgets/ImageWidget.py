from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ImageWidget(QWidget):
    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName
        self.resize(1300, 1300)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        image = QImage(self.fileName)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        print(self.imageLabel.width(),self.imageLabel.height())
        grid.addWidget(self.imageLabel)


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ImageTab(QWidget):
    def __init__(self, fileName):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.editor = QLineEdit()

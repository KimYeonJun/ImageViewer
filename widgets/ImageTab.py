from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ImageTab(QWidget):
    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName
        self.scaleFactor = 1.0
        self.setActions()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # 툴바
        self.toolbar = QToolBar()
        self.toolbar.addAction(self.zoomInAction)
        self.toolbar.addAction(self.zoomOutAction)
        grid.addWidget(self.toolbar)
        # 이미지

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.scrollArea = QScrollArea()
        self.scrollArea.setVisible(False)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)


        image = QImage(self.fileName)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.imageLabel.setScaledContents(True)
        self.scrollArea.setVisible(True)
        self.imageLabel.adjustSize()

        grid.addWidget(self.scrollArea)

    def setActions(self):
        self.zoomInAction = QAction(QIcon('images/plus.png'),'Zoom In (ctrl+numpad+)',self,shortcut="Ctrl++",triggered=self.zoomIn)
        self.zoomOutAction = QAction(QIcon('images/minus3.png'),'Zoom Out (ctrl+numpad-)',self,shortcut="Ctrl+-",triggered=self.zoomOut)

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
        # print('스크롤바 : '+str(self.scrollArea.horizontalScrollBar().value()))
        # print(self.scrollArea.horizontalScrollBar().pageStep())
        # self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value()+self.scrollArea.horizontalScrollBar().pageStep())
        self.setScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.setScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAction.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAction.setEnabled(self.scaleFactor > 0.333)

    def setScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value() + ((factor-1) * scrollBar.pageStep()/2 )))



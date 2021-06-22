from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ImageTab(QWidget):
    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName
        self.scaleFactor = 1.0
        self.lastDragPosX = 0
        self.setActions()
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)


        # 툴바
        self.toolbar = QToolBar()
        self.toolbar.addAction(self.zoomInAction)
        self.toolbar.addAction(self.zoomOutAction)
        self.toolbar.addAction(self.expandAction)
        self.toolbar.addAction(self.collapseAction)
        self.grid.addWidget(self.toolbar)
        # 이미지

        self.imageLabel = QLabel()
        print(self.imageLabel.width(),self.imageLabel.height())
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.scrollArea = QScrollArea()
        self.scrollArea.setVisible(True)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)

        self.qPixmapOrigin = QPixmap()
        self.qPixmapOrigin.load(self.fileName)

        #image = QImage(self.fileName)
        #self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.imageLabel.setPixmap(self.qPixmapOrigin)
        self.imageLabel.setScaledContents(True)
        self.scrollArea.setVisible(True)
        self.imageLabel.adjustSize()

        self.grid.addWidget(self.scrollArea)

    def setActions(self):
        self.zoomInAction = QAction(QIcon('images/plus.png'),'Zoom In (ctrl+numpad+)',self,shortcut="Ctrl++",triggered=self.zoomIn)
        self.zoomOutAction = QAction(QIcon('images/minus3.png'),'Zoom Out (ctrl+numpad-)',self,shortcut="Ctrl+-",triggered=self.zoomOut)
        self.expandAction = QAction(QIcon('images/expand.jpg'),'Expand',self, triggered=self.expandImg)
        self.collapseAction = QAction(QIcon('images/collapse.png'), 'Collapse', self,shortcut="Ctrl++",triggered=self.collapseImg)

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def expandImg(self):
        self.scrollArea.setWidgetResizable(True)
        #self.imageLabel.adjustSize()
        #self.scaleFactor = 1.0
        #self.scrollArea.hide()
       # self.imageLabel.adjustSize()

        #print('expand')
        #self.imageLabel.setPixmap(self.qPixmapOrigin.scaled(self.imageLabel.width(),self.imageLabel.height(),Qt.KeepAspectRatio))
        #self.imageLabel.setPixmap(qPixmapOrigin.scaled(self.label.width() - 3, self.label.height() - 3, Qt.KeepAspectRatio))

    def collapseImg(self):
        self.scrollArea.setWidgetResizable(False)
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
        #self.imageLabel.adjustSize(True)
        #print('collapse')


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

    def wheelEvent(self, event):
        zoom = False
        if event.modifiers() == Qt.ControlModifier:
            zoom = True
        if event.angleDelta().y()>0:
            event.accept()
            if zoom:
                self.zoomIn()
        else:
            event.accept()
            if zoom:
                self.zoomOut()
        # if event.modifiers() == Qt.ControlModifier:
        #     if event.angleDelta().y()>0:
        #         self.zoomIn()
        #     else:
        #         self.zoomOut()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            print(event.pos().y())

        return QWidget.eventFilter(self, source, event)

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.lastDragPosX = event.pos().x()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            distanceX = self.lastDragPosX - event.pos().x()
            self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value()+distanceX)
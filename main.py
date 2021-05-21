import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from widgets.ImageTab import ImageTab

form_class = uic.loadUiType("UI/image_viewer.ui")[0]


class TabButtonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create button's
        self.button_remove = QPushButton("x")
        # Set button size
        self.button_remove.setFixedSize(16, 16)

        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Add button's to layout
        self.layout.addWidget(self.button_remove)

        # Use layout in widget
        self.setLayout(self.layout)

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadCustomMenu()
        self.setEvent()

    def loadCustomMenu(self):
        self.action_delete_list = QAction(self)
        self.action_delete_list.setText('Delete')
        self.customMenu = QMenu('Menu', self.image_list_widget)
        self.customMenu.addAction(self.action_delete_list)

    def setEvent(self):
        # MenuBar 버튼 이벤트
        self.action_open_image.triggered.connect(self.actionOpenImage)
        self.action_open_images.triggered.connect(self.actionOpenImages)
        self.action_open_folder.triggered.connect(self.actionOpenFolder)
        self.action_clear_list.triggered.connect(self.actionClearList)
        self.image_list_widget.currentItemChanged.connect(self.chkCurrentItemChanged)
        self.image_list_widget.itemDoubleClicked.connect(self.listItemDoubleClicked)
        self.image_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.image_list_widget.customContextMenuRequested.connect(self.listItemRightClicked)

        # TabWidget 이벤트
        self.image_viewer_tab.setTabsClosable(True)
        self.image_viewer_tab.tabCloseRequested.connect(self.closeTab)


    def closeTab(self, index):
        if index == 0:
            return
        tab = self.image_viewer_tab.widget(index)
        tab.deleteLater() # 메모리에서 위젯의 참조를 즉시 삭제한다.
        self.image_viewer_tab.removeTab(index)

    def listItemRightClicked(self, event):
        index = self.image_list_widget.indexAt(event)
        if not index.isValid():
            return
        self.customMenu.popup(QCursor.pos())

    def actionClearList(self):
        self.image_list_widget.clear()

    def listItemDoubleClicked(self):
        if self.image_list_widget.currentItem():
            fileName = self.image_list_widget.currentItem().text()
            tabName = fileName.split('/')[-1]
            index = self.image_viewer_tab.addTab(ImageTab(fileName), tabName)
            self.image_viewer_tab.setCurrentIndex(index)
            # self.right = self.image_viewer_tab.tabBar().RightSide
            # # self.image_viewer_tab.tabBar().setTabButton(self.image_viewer_tab.count()-1, self.right,TabButtonWidget(self.image_viewer_tab))
            # tabButtonWidget = TabButtonWidget()
            # tabButtonWidget.button_remove.clicked.connect(self.btnRun_clicked)
            # self.image_viewer_tab.tabBar().setTabButton(self.image_viewer_tab.count() - 1, self.right,
            #                                             tabButtonWidget)


    # def listItemDoubleClicked(self):
    #     if self.image_list_widget.currentItem():
    #         newTab = QWidget()
    #         gg = QGridLayout()
    #         newTab.setLayout(gg)
    #         qPixmapVar = QPixmap()
    #         qPixmapVar.load(self.image_list_widget.currentItem().text())
    #         label = QLabel()
    #         label.setPixmap(qPixmapVar)
    #         label.resize(qPixmapVar.width(), qPixmapVar.height())
    #         gg.addItem(label)
    #         fileName = self.image_list_widget.currentItem().text()
    #         tabName = fileName.split('/')[-1]
    #         self.image_viewer_tab.addTab(newTab, tabName)
    #         print(self.image_list_widget.currentItem().text())

    # def chkCurrentItemChanged(self):
    #     if self.image_list_widget.currentItem():
    #         qPixmapVar = QPixmap()
    #         qPixmapVar.load(self.image_list_widget.currentItem().text())
    #         self.label.setPixmap(qPixmapVar)
    #         self.label.setAlignment(Qt.AlignCenter)
    #         print('label : '+str(self.label.width())+" "+str(self.label.height()))
    #         #self.label.resize(qPixmapVar.width(), qPixmapVar.height())
    #         print(str(qPixmapVar.width()) + " " + str(qPixmapVar.height()))
    #     else:
    #         self.label.setPixmap(QPixmap()) # 선택된 아이템이 없는 경우 이미지 안보이기.

    def chkCurrentItemChanged(self):
        if self.image_list_widget.currentItem():
            qPixmapVar = QPixmap()
            qPixmapVar.load(self.image_list_widget.currentItem().text())
            if qPixmapVar.width()>= self.label.width() or qPixmapVar.height()>=self.label.height():
                self.label.setPixmap(qPixmapVar.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))
            else:
                self.label.setPixmap(qPixmapVar)
            # self.label.setPixmap(qPixmapVar.scaled(self.label.width(),self.label.height(),Qt.KeepAspectRatio))
            self.label.setAlignment(Qt.AlignCenter)
            print('label : '+str(self.label.width())+" "+str(self.label.height()))
            #self.label.resize(qPixmapVar.width(), qPixmapVar.height())
            print(str(qPixmapVar.width()) + " " + str(qPixmapVar.height()))
        else:
            self.label.setPixmap(QPixmap()) # 선택된 아이템이 없는 경우 이미지 안보이기.


    def actionOpenImage(self):
        fileNameTuple = QFileDialog.getOpenFileName(self, 'OpenImage', "","Images (*.png *.xpm *.jpg)")
        fileName = fileNameTuple[0]
        if fileName:
            self.image_list_widget.addItem(fileName)


    def actionOpenImages(self):
        fileNameTuple = QFileDialog.getOpenFileNames(self, 'OpenImage', "", "Images (*.png *.xpm *.jpg)")
        print(fileNameTuple)
        fileNameList = fileNameTuple[0]
        for fileName in fileNameList:
            self.image_list_widget.addItem(fileName)

    def actionOpenFolder(self):
        #fileNameTuple = QFileDialog.getOpenFileNames(self, 'OpenImage', "", "Images (*.png *.xpm *.jpg)")
        dirName = QFileDialog.getExistingDirectory(self, 'Find Folder')
        fileList = os.listdir(dirName)
        arr = []
        for file in fileList:
            full_filename = os.path.join(dirName, file)
            ext = os.path.splitext(full_filename)[-1]
            if ext.lower() == '.png' or ext.lower() == '.jpg':
                full_filename = full_filename.replace("\\", "/")
                self.image_list_widget.addItem(full_filename)
                arr.append(full_filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()


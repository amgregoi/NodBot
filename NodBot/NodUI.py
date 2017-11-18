import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl 
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QPlainTextEdit, QDockWidget, QMenuBar, QMenu, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
import NodBot as Nodiatis

"""
" 
"
" Parent: None
"""  
class Browser(QWebEngineView):

    """
    " 
    "
    " Parent: Browser Class
    """
    def __init__(self):
        self.view = QWebEngineView.__init__(self)
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)

    
    """
    " 
    "
    " Parent: Browser Class
    """
    def load(self,url):  
        self.setUrl(QUrl(url)) 
 
    """
    " 
    "
    " Parent: Browser Class
    """
    def adjustTitle(self):
        self.setWindowTitle(self.title())
 
    """
    " 
    "
    " Parent: Browser Class
    """
    def disableJS(self):
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)

"""
" 
"
" Parent: None
""" 
class MenuPane(QWidget):

    lKillCount = 0
    layout = QGridLayout()

    mPlayStatus = "Play"
    
    """
    " 
    "
    " Parent: MenuPane Class
    """
    def __init__(self):
        super(MenuPane, self).__init__()
        self.initPane()

    """
    " 
    "
    " Parent: MenuPane Class
    """
    def initPane(self):

        button1 = QPushButton(self.mPlayStatus)
        button1.clicked.connect(self.toggleStatus)

        button2 = QPushButton("Setup SS")
        button2.clicked.connect(self.takeSetupScreenShot)

        label1 = QLabel("Kill Count: %d" %self.lKillCount)

        self.layout.addWidget(button1, 1, 0, Qt.AlignTop)
        self.layout.addWidget(button2, 2, 0,Qt.AlignTop)
        self.layout.addWidget(label1, 5, 0, Qt.AlignTop)
        
        self.setLayout(self.layout)

    """
    " 
    "
    " Parent: MenuPane Class
    """
    def incrementKillCount(self):
        print("MADE IT HERE!!!!!!!!!!!!!!!!!")
        self.lKillCount += 1
        self.updateLayout(self.layout)

    """
    " 
    "
    " Parent: MenuPane Class
    """
    def updateLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtWidgets.QWidgetItem):
                item.widget().close()
            else:
                self.clearLayout(item.layout())

        layout.removeItem(item)
        self.initPane()
 
    """
    " 
    "
    " Parent: MenuPane Class
    """
    def toggleStatus(self, two):
        if(self.mPlayStatus == "Play"): 
            self.mPlayStatus = "Pause"
        else: 
            self.mPlayStatus = "Play"
        self.updateLayout(self.layout)
        Nodiatis.toggleGameStatus()
   
    """
    " 
    "
    " Parent: MenuPane Class
    """
    def takeSetupScreenShot(one, two):
        Nodiatis.takeSetupSS()

"""
" 
"
" Parent None
"""
class OutputPane(QPlainTextEdit):
    
    """
    " 
    "
    " Parent: OutputPane Class
    """   
    def __init__(self):
        super(OutputPane, self).__init__()
        self.initPane()

    """
    " 
    "
    " Parent: OutputPane Class
    """
    def initPane(self):
        self.setReadOnly(True)

    """
    " 
    "
    " Parent: OutputPane Class
    """
    def addMessage(self, aMessage):
        self.appendPlainText(aMessage)

"""
" 
"
"
"""
class NodGUI(QMainWindow):

    mOutput = None
    mMenu = None

    """
    " 
    "
    " Parent: NodGUI Class
    """
    def __init__(self):
        super(NodGUI, self).__init__()
        self.title = 'NodBot'
        self.left = 5
        self.top = 5
        self.width = 800
        self.height = 800
        self.initUI()
 
    """
    " 
    "
    " Parent: NodGUI Class
    """
    def initUI(self):
        print("#################")
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 

        lBrowser = self.createBrowserWidget()
        lDock = self.createOutputPaneDock()
        

        self.mMenu = MenuPane()
        lDock2 = QDockWidget()
        lDock2.setFeatures(QDockWidget.NoDockWidgetFeatures)
        lDock2.setWidget(self.mMenu)


        self.setCentralWidget(lBrowser)
        self.addDockWidget(Qt.BottomDockWidgetArea, lDock)
        self.addDockWidget(Qt.RightDockWidgetArea, lDock2)
        self.show()

    """
    " 
    "
    " Parent: NodGUI Class
    """
    def createBrowserWidget(self):
        browser = Browser()
        browser.setFixedSize(800,650)
        browser.show()
        browser.load("https://nodiatis.com")

        return browser

    """
    " 
    "
    " Parent: NodGUI Class
    """
    def createOutputPaneDock(self):
        self.mOutput = OutputPane()
        dock = QDockWidget()
        dock.setWidget(self.mOutput)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)

        return dock;

    """
    " 
    "
    " Parent: NodGUI Class
    """
    def addOutputMessage(self, aMessage):
        self.mOutput.addMessage(aMessage)

    """
    " 
    "
    " Parent: NodGUI Class
    """
    def incrementKillCount(self):
        self.mMenu.incrementKillCount()




















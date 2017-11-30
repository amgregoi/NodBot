import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl 
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QPlainTextEdit, QDockWidget, QMenuBar, QMenu, QVBoxLayout, QGridLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

"""
" 
"
" Parent: None
"""  
class Browser(QWebEngineView):

    """
    " This function initializes the browser class
    "
    " Parent: Browser 
    """
    def __init__(self):
        self.view = QWebEngineView.__init__(self)
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)
    
    """
    " This function loads the provided url
    "
    " Parent: Browser 
    """
    def load(self, url):  
        self.setUrl(QUrl(url)) 
 
    """
    " This function changes the title of the browser window
    "
    " Parent: Browser 
    """
    def adjustTitle(self):
        self.setWindowTitle(self.title())
 
    """
    " This function disables javascript in the browser
    "
    " Parent: Browser 
    """
    def disableJS(self):
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)

"""
" This class holds relevant buttons, and counters for the user to interact with
"
" Parent: None
""" 
class MenuPane(QWidget):

    kill_count = 0
    chest_count = 0
    layout = QGridLayout()

    play_status = "Start"

    special_button_text = "Special (F)"
    special_move_button = True # True = 'f', False = 'd'

    
    """
    " This function intializes the MenuPane class
    "
    " Parent: MenuPane 
    """
    def __init__(self, game):
        super(MenuPane, self).__init__()
        self.game_comm = game
        self.initPane()

    """
    " 
    "
    " Parent: MenuPane 
    """
    def initPane(self):

        # init status button
        status_button = QPushButton(self.play_status)
        status_button.clicked.connect(self.toggleStatus)

        # init setup button
        setup_button = QPushButton("Setup SS")
        setup_button.clicked.connect(self.takeSetupScreenShot)

        # init debug button
        debug_button = QPushButton("DEBUG")
        debug_button.clicked.connect(self.toggleDebug)

        # init class ability button
        special_button = QPushButton(self.special_button_text)
        special_button.clicked.connect(self.toggleSpecialMoveButton)

        # init kill count label
        kill_count_label = QLabel("Kill Count: %d" %self.kill_count)
        
        # init chest count label
        chest_count_label = QLabel("Chest Count: %d" %self.chest_count)

        # Add all widgets to menu layout
        self.layout.addWidget(status_button, 1, 0, Qt.AlignTop)
        self.layout.addWidget(special_button, 2, 0, Qt.AlignTop)
        self.layout.addWidget(debug_button, 3, 0, Qt.AlignTop)
        self.layout.addWidget(setup_button, 4, 0, Qt.AlignTop)
        self.layout.addWidget(kill_count_label, 15, 0, Qt.AlignBottom)
        self.layout.addWidget(chest_count_label, 16, 0, Qt.AlignBottom)
        
        self.setLayout(self.layout)

    """
    " This function increments the kill counter
    "
    " Parent: MenuPane 
    """
    def incrementKillCount(self):
        self.kill_count += 1
        self.updateLayout(self.layout)

    """
    " This function increments the chest counter
    "
    " Parent: MenuPane 
    """
    def incrementChestCount(self):
        self.chest_count += 1
        self.updateLayout(self.layout)

    """
    " This function refreshes the menu pane layout
    "
    " Parent: MenuPane 
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
    " This function toggles the run status of the bot
    "
    " Parent: MenuPane 
    """
    def toggleStatus(self, two):
        if(self.play_status == "Resume" or self.play_status == "Start"): 
            self.play_status = "Pause"
        else: 
            self.play_status = "Resume"

        self.updateLayout(self.layout)
        self.game_comm.toggleGameStatus()

 
    """
    " This function toggles the debug status for output messages
    "
    " Parent: MenuPane 
    """
    def toggleDebug(self, two):
        self.game_comm.toggleDebug()
        

    """
    " This function toggles the class ability between "D" and "F"
    "
    " Parent: MenuPane 
    """
    def toggleSpecialMoveButton(self, two):
        #Toggle the special flag
        self.special_move_button = not self.special_move_button
        #update the combat button
        
        if(self.special_move_button):
            self.special_button_text = "Special (F)"
            self.game_comm.toggleSpecialMoveButton('f')
        else: 
            self.special_button_text = "Special (D)"
            self.game_comm.toggleSpecialMoveButton('d')

        self.updateLayout(self.layout)


   
    """
    " This function takes the setup screenshot 
    "
    " Parent: MenuPane 
    """
    def takeSetupScreenShot(self, two):
        self.game_comm.takeSetupSS()

"""
" 
"
" Parent None
"""
class OutputPane(QPlainTextEdit):
    
    """
    " This function intiailizes the OutputPanel widget
    "
    " Parent: OutputPane 
    """   
    def __init__(self):
        super(OutputPane, self).__init__()
        self.setReadOnly(True)

    """
    " This function adds a message to the output panel 
    "
    " Parent: OutputPane 
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
    " This function initializes the NodGUI class
    "
    " Parent: NodGUI 
    """
    def __init__(self, game):
        super(NodGUI, self).__init__()
        self.title = 'NodBot'
        self.left = 5
        self.top = 5
        self.width = 800
        self.height = 800
        self.game_comm = game
        self.initUI()
 
    """
    " This function builds the relevant widgets for the nod gui
    "
    " Parent: NodGUI 
    """
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 

        lBrowser = self.createBrowserWidget()
        lDock = self.createOutputPaneDock()
        

        self.mMenu = MenuPane(self.game_comm)
        lDock2 = QDockWidget()
        lDock2.setFeatures(QDockWidget.NoDockWidgetFeatures)
        lDock2.setWidget(self.mMenu)


        self.setCentralWidget(lBrowser)
        self.addDockWidget(Qt.BottomDockWidgetArea, lDock)
        self.addDockWidget(Qt.RightDockWidgetArea, lDock2)
        self.show()

    """
    " This function creates the browser widget
    "
    " Parent: NodGUI 
    """
    def createBrowserWidget(self):
        browser = Browser()
        browser.setFixedSize(800,650)
        browser.show()
        browser.load("https://nodiatis.com")

        return browser

    """
    " This function creates the output panel widget
    "
    " Parent: NodGUI 
    """
    def createOutputPaneDock(self):
        self.mOutput = OutputPane()
        dock = QDockWidget()
        dock.setWidget(self.mOutput)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)

        return dock;

    """
    " This function adds a message to the output panel widget
    "
    " Parent: NodGUI 
    """
    def addOutputMessage(self, aMessage):
        self.mOutput.addMessage(aMessage)

    """
    " This function increments the kill counter in the menu pane widget
    "
    " Parent: NodGUI 
    """
    def incrementKillCount(self):
        self.mMenu.incrementKillCount()

    """
    " This function increments the chest counter in the menu pane widget
    "
    " Parent: NodGUI 
    """
    def incrementChestCount(self):
        self.mMenu.incrementChestCount()




















import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject

from Nodcv import NodiatisCV
from Output import Logger
from Game import Game
from NodUI import NodGUI

"""
"
"
" Parent: None
"""
class GameController():

    #
    running = False

    """
    " This function initializes the GameController class
    "
    " Parent: GameController
    """
    def __init__(self, logger, game):
        self.logger = logger
        self.nod_cv = NodiatisCV(logger)
        self.game = game

    """
    " This function starts the game loop thread
    "
    " Parent: GameController
    """
    def startBot (self):
        if not self.running:
            self.running = True #set the playing flag so multiple play instances cannot start
            thread = Thread(target = self.game.GameLoop)
            thread.daemon = True
            thread.start()

    """
    " This function takes the setup screen shot of the map
    "
    " Parent: GameController
    """
    def takeSetupSS(self):
        self.nod_cv.takeSetupSS(self.nod_cv.SSQueries.get("ooc"))
        nod_log.logOutput("Take Screenshot of map")

    """
    " This function toggles the game loop status 
    "
    " Parent: GameController
    """
    def toggleGameStatus(self):
        if self.running:
            self.game.toggleGameStatus()
        else:
            self.startBot()

    """
    " This function toggles which class ability is used (F or D)
    "
    " Parent: GameController
    """
    def toggleSpecialMoveButton(self, aVal):
        self.game.toggleSpecialMoveButton(aVal)

    """
    " This function toggles whether DEBUG messages are to be shown
    "
    " Parent: GameController
    """
    def toggleDebug(self):
        self.logger.toggleDebug()

"""
"
"
" Parent: None
"""
class Application(QObject):
    app = QApplication(sys.argv)
    nod_gui = None

    """
    " This function forwards an output message to the gui output pane
    "
    " Parent: Application
    """
    def showMessage(self, aMessage):
        if(self.nod_gui is not None):
            self.nod_gui.addOutputMessage(aMessage)

    """
    " This function forwards an increment messages to the menu pane kill counter
    "
    " Parent: Application
    """
    def incrementKillCount(self):        
        if(self.nod_gui is not None):
            self.nod_gui.incrementKillCount()

    """
    " This function forwards an increment messages to the menu pane chest counter
    "
    " Parent: Application
    """
    def incrementChestCount(self):        
        if(self.nod_gui is not None):
            self.nod_gui.incrementChestCount()

    """
    " This function initializes the application by creating the GUI and waiting for exit
    "
    " Parent: Application
    """
    def init(self, game):
        self.nod_gui = NodGUI(game)
        sys.exit(self.app.exec_())

"""
" 
" 
" 
"""
if __name__ == '__main__':
    #Init classes
    nod_log = Logger()
    nod_application = Game(nod_log)
    game_controller = GameController(nod_log, nod_application)
    q_app = Application()

    #Connect to GUI triggers
    nod_log.output_trigger.connect(q_app.showMessage)
    nod_log.kill_trigger.connect(q_app.incrementKillCount)
    nod_log.chest_trigger.connect(q_app.incrementChestCount)
    
    #Start application interface
    q_app.init(game_controller)























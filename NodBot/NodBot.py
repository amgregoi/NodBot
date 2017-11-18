import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *

import Nodcv as NodCV
import Combat as CMB
import Output
from Game import Game
from NodUI import NodGUI

#
IS_PLAYING = False


"""
"
"
"
"""
def doPlay ():
    global IS_PLAYING
    if not IS_PLAYING:
        IS_PLAYING = True #set the playing flag so multiple play instances cannot start
        thread = Thread(target = nod_application.GameLoop)
        thread.daemon = True
        thread.start()

"""
"
"
"
"""
def takeSetupSS():
    NodCV.takeSetupSS(NodCV.SSQueries.get("ooc"))
    Output.logOutput("Take Screenshot of map")

"""
"
"
"
"""
def toggleGameStatus():
    if IS_PLAYING:
        nod_application.toggleGameStatus()
    else:
        doPlay()

"""
"
"
"
"""
class Application(QObject):
    q_app = QApplication(sys.argv)
    nod_gui = None

    def makeConnection(self, obj):
        obj.GUI_KillCount.connect(self.incrementKillCount)
        obj.GUI_ShowMessage.connect(self.showMessage)
        print "connection made ################"

    """
    "
    "
    "
    """
    @pyqtSlot(str)
    def showMessage(self, aMessage):
        if(self.nod_gui is not None):
            self.nod_gui.addOutputMessage(aMessage)

    """
    "
    "
    "
    """
    #QObject::setParent: Cannot set parent, new parent is in a different thread
    @pyqtSlot(int)
    def incrementKillCount(self, val):
        print "incrementing kill count"
        if(nod_gui is not None):
            nod_gui.incrementKillCount()

    """
    "
    "
    "
    """
    def init(self):
        nod_gui = NodGUI()
        sys.exit(self.q_app.exec_())

"""
" 
" 
" 
"""
q_app = Application()
nod_application = Game()

if __name__ == '__main__':
    # q_app.makeConnection(nod_application)
    q_app.init()























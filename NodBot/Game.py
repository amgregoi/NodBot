import Combat as CMB
import Nodcv as NodCV
import time as Clock
import random, gc
import Output as NodLog

from PyQt5.QtCore import pyqtSignal, QThread

from guppy import hpy


#
COUNT_DOWN = 5

#
GAME_PAUSE = False

#
TOTAL_KILLS = 0

#
CURRENT_KILLS = 0

"""
"
"
"
"""
class Game (QThread):
    
    GUI_KillCount = pyqtSignal(int)
    GUI_ShowMessage = pyqtSignal(str)

    """
    "
    "
    " Parent: Game Class
    """
    def __init__(self):
        super(Game, self).__init__()
        self.hp = hpy()
        self.hp.setrelheap()



    """
    " This function automates nodiatis combat
    " 
    " Parent: Game Class
    """
    def GameLoop(self):    
        #Kill Counter
        global TOTAL_KILLS
        global CURRENT_KILLS
        
        self.startCountDown()
        
        while 1:
            # Test - Remove / fix later
            # self.GUI_KillCount.emit(1)
            # self.GUI_ShowMessage.emit("This is a test")

            while not GAME_PAUSE:
                self.GUI_KillCount.emit(1)

                try:
                    if NodCV.doScreenMatch(NodCV.SSQueries.get("ooc")) is not None: 
                        CMB.start()

                    elif NodCV.doScreenMatch(NodCV.SSQueries.get("exit")) is not None:
                        CMB.end()
                        CURRENT_KILLS += 1
                    else:
                        CMB.inProcess()

                    #Random Break / Pause.. maybe
                    rand_kills = random.randint(15, 40)
                    rand_sleep = random.randint(10, 25)

                    if CURRENT_KILLS > rand_kills:
                        NodLog.logOutput("Taking break for %ds" %rand_sleep)
                        Clock.sleep(rand_sleep)
                        TOTAL_KILLS += CURRENT_KILLS
                        CURRENT_KILLS = 0;

                except Exception as e:
                    NodLog.logDebug("Exception occurred: ")
                    NodLog.logDebug(e)
                    # print e

                gc.collect() # initiate garbage collector > prevents fragmentation

            h = self.hp.heap()
            print h
            Clock.sleep(2) # wait for game to resume


    """
    "
    "
    " Parent: Game Class
    """
    def getKillCount(self):
        return TOTAL_KILLS + CURRENT_KILLS

    """
    "
    "
    " Parent: Game Class
    """
    def startCountDown(self):
        lCount = COUNT_DOWN
        while(lCount > 0):
            NodLog.logOutput("Starting in %d seconds" %lCount)
            Clock.sleep(1)
            lCount -= 1

    """
    "
    "
    " Parent: Game Class
    """
    def toggleGameStatus(self):
        global GAME_PAUSE

        if GAME_PAUSE:
            NodLog.logOutput("Resuming game")
            GAME_PAUSE = False
        else:
            NodLog.logOutput("Pausing game")
            GAME_PAUSE = True

















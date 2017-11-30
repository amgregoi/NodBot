from Combat import Combat
from Nodcv import NodiatisCV
import time as Clock
import random, gc

from PyQt5.QtCore import pyqtSignal, QThread


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
" Parent: None
"""
class Game (QThread):
        
    """
    " This function initializes the Game class
    "
    " Parent: Game 
    """
    def __init__(self, logger):
        super(Game, self).__init__()
        self.CMB = Combat(logger)
        self.nod_cv = NodiatisCV(logger)
        self.nod_log = logger



    """
    " This function automates nodiatis combat
    " 
    " Parent: Game 
    """
    def GameLoop(self):
        global CURRENT_KILLS

        self.startCountDown()
        
        while 1:
            while not GAME_PAUSE:                
                try:
                    if self.nod_cv.doScreenMatch(self.nod_cv.SSQueries.get("ooc")) is not None: 
                        self.CMB.start()
                    else:
                        exit = self.nod_cv.doScreenMatch(self.nod_cv.SSQueries.get("exit")) 
                        if exit is not None:
                            self.randomBreak()
                            self.CMB.end(exit)
                            CURRENT_KILLS += 1
                        else:
                            self.CMB.inProcess()

                except Exception as e:
                    self.nod_log.logDebug("Exception occurred: ")
                    self.nod_log.logDebug(e)
                    # print e

                gc.collect() # initiate garbage collector > prevents fragmentation

            Clock.sleep(2) # wait for game to resume

    """
    " This function takes a random length break after a random number of kills
    "
    " Parent: Game 
    """
    def randomBreak(self):
        global TOTAL_KILLS
        global CURRENT_KILLS

        #Random Break / Pause.. maybe
        rand_kills = random.randint(15, 40)
        rand_sleep = random.randint(10, 25)

        if CURRENT_KILLS > rand_kills:
            self.nod_log.logOutput("Taking break for %ds" %rand_sleep)
            Clock.sleep(rand_sleep)
            TOTAL_KILLS += CURRENT_KILLS
            CURRENT_KILLS = 0;

    """
    " This function prints the count down timer when the script will start
    "
    " Parent: Game 
    """
    def startCountDown(self):
        lCount = COUNT_DOWN
        while(lCount > 0):
            self.nod_log.logOutput("Starting in %d seconds" %lCount)
            Clock.sleep(1)
            lCount -= 1

    """
    " This function toggles game loop status
    "
    " Parent: Game 
    """
    def toggleGameStatus(self):
        global GAME_PAUSE

        if GAME_PAUSE:
            self.nod_log.logOutput("Resuming game")
            GAME_PAUSE = False
        else:
            self.nod_log.logOutput("Pausing game")
            GAME_PAUSE = True

    """
    " This function toggles which class ability is used in combat
    "
    " Parent: Game 
    """
    def toggleSpecialMoveButton(self, aVal):
        self.CMB.special_move_button = aVal
        self.nod_log.logOutput("Class Ability changed to (%s)" %aVal)

















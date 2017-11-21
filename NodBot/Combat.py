import Input
from Nodcv import NodiatisCV
import time as Clock
import random as Rand


#
SKIP_TROPHIES = True

"""
" This class acts as an enumerator for the fighting status in the combat class
"
"""
class FightStatus():
    START = 1
    END = 2
    WAITING = 3
    INIT = 99


"""
"
"
"
"""
class Combat():

    special_move_button = 'f'  #Initial Value always 'F'

    """
    " This function initializes the Combat class
    "
    " Parent: Combat 
    """
    def __init__(self, logger):
        self.nod_log = logger
        self.NodCV = NodiatisCV(logger)
        self.status = FightStatus.INIT


    """
    " This function will initialize combat from the base map
    "
    " Parent: Combat 
    """
    def start(self):
        self.nod_log.logOutput("Starting Combat")
        self.status = FightStatus.START

        #Start Combat
        Input.doKeyPress('f')

        #Start AutoAttack
        Input.doKeyPress('a')

        #Use Special
        Clock.sleep(1)
        Input.doKeyPress(self.special_move_button) #Special skill (D or F)

        Input.moveTo(Rand.randint(20, 110), Rand.randint(100, 300))

    """
    " This function will loot trophies, look for chests, and exit combat
    "
    " Parent: Combat 
    """
    def end(self):
        self.nod_log.logOutput("Finished Combat")
        self.status = FightStatus.END

        #Click loot button
        coord = self.NodCV.doScreenMatch(self.NodCV.SSQueries.get("exit"))

        Input.doLeftClick(coord[0]-Rand.randint(190, 215), coord[1]-Rand.randint(60, 69))
        Input.moveTo(Rand.randint(20, 110), Rand.randint(100, 300)) # Move off of loot location to get rid of tooltip
        
        #Look for chests
        self.scanForChests()

        #Exit
        Clock.sleep(2)
        Input.doKeyPress('e')

        if SKIP_TROPHIES:
            location = self.NodCV.doScreenMatch(self.NodCV.SSQueries.get("confirm"))
            try:
                Input.doLeftClick(location[0] - Rand.randint(5,20), location[1] - Rand.randint(2, 5))
            except Exception as e:
                self.nod_log.logDebug("Skip Trophy Exception: ")
                self.nod_log.logDebug(e)


    """
    " This function scans the screen for the three types of chests
    "
    " Parent: Combat 
    """
    def scanForChests(self):
        try:     
            Clock.sleep(3)

            xOffset = Rand.randint(-5, 5)
            yOffset = Rand.randint(0, 10)

            self.nod_log.logOutput("Scanning for chest 1 (brown)")
            location = self.NodCV.chestMatch(self.NodCV.SSQueries.get("chest1"))
            if(location is not None):
                Input.doLeftClick(location[0] + xOffset, location[1] + yOffset)
                self.nod_log.logFoundChest()
                return

            self.nod_log.logOutput("Scanning for chest 2 (gray)")
            location = self.NodCV.chestMatch(self.NodCV.SSQueries.get("chest2"))
            if(location is not None):
                Input.doLeftClick(location[0] + xOffset, location[1] + yOffset)
                self.nod_log.logFoundChest()
                return

            self.nod_log.logOutput("Scanning for chest 3 (green)")
            location = self.NodCV.chestMatch(self.NodCV.SSQueries.get("chest3"))
            if(location is not None):
                Input.doLeftClick(location[0] + xOffset, location[1] + yOffset)
                self.nod_log.logFoundChest()

        except Exception as e:
            self.nod_log.logDebug("Known OpenCV issue with minimum threshold: ")
            self.nod_log.logDebug(e)


    """
    " This function waits for combat to end, stacks trophies, movies full stacks to stash
    "
    " Parent: Combat 
    """
    def inProcess(self):
        if(self.status != FightStatus.WAITING):
            self.nod_log.logOutput("Combat in Progress")
            self.status = FightStatus.WAITING

        Clock.sleep(3)














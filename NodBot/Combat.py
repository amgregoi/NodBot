import Input
import Nodcv as NodCV
import Output as NodLog

import time as Clock
import random as Rand


#
DEBUG = False

#
SKIP_TROPHIES = True


"""
" This function will initialize combat from the base map
"
" Parent: None
"""
def start():
    NodLog.logDebug("Initializing Combat")
    
    #Start Combat
    Input.doKeyPress('f')

    #Start AutoAttack
    Input.doKeyPress('a')

    #Use Special
    Clock.sleep(1)
    Input.doKeyPress('f') #Special skill (D or F)

    Input.moveTo(100, 150)

"""
" This function will loot trophies, look for chests, and exit combat
"
" Parent: None
"""
def end():
    NodLog.logDebug("Finished Combat")

    #Click loot button
    coord = NodCV.doScreenMatch(NodCV.SSQueries.get("exit"))

    Input.doLeftClick(coord[0]-Rand.randint(190, 215), coord[1]-Rand.randint(60, 69))
    # Input.moveTo(10, 900) # Move off of loot location to get rid of tooltip
    
    #Look for chests
    scanForChests()

    #Exit
    Clock.sleep(2)
    Input.doKeyPress('e')

    if SKIP_TROPHIES:
        location = NodCV.doScreenMatch(NodCV.SSQueries.get("confirm"))
        try:
            Input.doLeftClick(location[0] - Rand.randint(40,100), location[1] - Rand.randint(80, 97))
        except Exception as e:
            return


"""
" This function scans the screen for the three types of chests
"
" Parent: None
"""
def scanForChests():
    try:     
        Clock.sleep(3)

        xOffset = Rand.randint(-5, 5)
        yOffset = Rand.randint(0, 10)

        NodLog.logOutput("Scanning for chest 1 (brown)")
        location = NodCV.chestMatch(NodCV.SSQueries.get("chest1"))
        if(location is not None):
            Input.doLeftClick(location[0] + xOffset, location[1] + yOffset)

        NodLog.logOutput("Scanning for chest 2 (gray)")
        location = NodCV.chestMatch(NodCV.SSQueries.get("chest2"))
        if(location is not None):
            Input.doLeftClick(location[0] + xOffset, location[1] + yOffset)

        NodLog.logOutput("Scanning for chest 3 (green)")
        location = NodCV.chestMatch(NodCV.SSQueries.get("chest3"))
        if(location is not None):
            Input.doLeftClick(location[0] + xOffset, location[1] + yOffset)

    except Exception as e:
        NodLog.logDebug("Known OpenCV issue with minimum threshold: ")
        NodLog.logDebug(e)


"""
" This function waits for combat to end, stacks trophies, movies full stacks to stash
"
" Parent: None
"""
def inProcess():
    NodLog.logDebug("Combat in Progress")
    Clock.sleep(3)


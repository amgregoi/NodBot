from pykeyboard import PyKeyboard
import pyautogui as PyMouse
import time as Clock



"""
"
" MOUSE
"
"""	

#
py_keyboard = PyKeyboard()

"""
"
"
"
"""	
def doKeyPress(aChar):
    py_keyboard.press_key(aChar)
    Clock.sleep(1)
    py_keyboard.release_key(aChar)



"""
"
" KEYBOARD
"
"""	

"""
"
"
"
"""	
def doLeftClick(aX, aY):
	PyMouse.click(aX, aY, button='left')
	# NodLog.logDebug("Mouse Click: (%d, %d)" %(aX, aY))

"""
"
"
"
"""	
def moveTo(aX, aY):
	PyMouse.moveTo(aX, aY)

"""
"
"
"
"""	
def getMousePosition():
	return PyMouse.position()
from NodBot import q_app as App

#
DEBUG = True

"""
" This function prints debug output to the log
"
" Parent: None
"""
def logDebug(message, level=0):
	if DEBUG:
		lMessage = "D ::" + ("\t" * level) + " %s" %message
		App.showMessage(lMessage)
		print lMessage

"""
" This function prints normal output to the log
" 
" Parent: None
"""
def logOutput(message, level=0):
	lMessage = "O :: " + ("\t" * level) + " %s" %message
	App.showMessage(lMessage)
	print lMessage


"""
" This function is used to set the global debug variable
"
" Parent: None
"""
def setDebug(aVal):
	global DEBUG
	DEBUG = aVal
# from NodBot import q_app as App
from PyQt5 import QtCore



class Logger(QtCore.QObject):
	#
	DEBUG = False

	#
	output_trigger = QtCore.pyqtSignal(str)
	kill_trigger = QtCore.pyqtSignal()
	chest_trigger = QtCore.pyqtSignal()

	"""
	" This function initializes the Logger class
	"
	" Parent: Logger
	"""
	def __init__(self):
		super(Logger, self).__init__()


	"""
	" This function prints debug output to the log
	"
	" Parent: Logger
	"""
	def logDebug(self, message, level=0):		
		if self.DEBUG:
			lMessage = "D :: " + ("\t" * level) + " %s" %message
			self.output_trigger.emit(lMessage)

	"""
	" This function prints normal output to the log
	" 
	" Parent: Logger
	"""
	def logOutput(self, message, level=0):
		lMessage = "O :: " + ("\t" * level) + " %s" %message
		self.output_trigger.emit(lMessage)


	"""
	" This function logs a new kill for the GUI to update
	"
	" Parent: Logger
	"""
	def logNewKill(self):
		self.kill_trigger.emit()

	"""
	" This function logs a new kill for the GUI to update
	"
	" Parent: Logger
	"""
	def logFoundChest(self):
		self.chest_trigger.emit()

	"""
	" This function is used to set the class debug variable
	"
	" Parent: Logger
	"""
	def setDebug(self, aVal):
		self.DEBUG = aVal
		if(aVal): self.logOutput("DEBUG set to TRUE", 0)
		else: self.logOutput("DEBUG set to FALSE", 0)


	"""
	" This function is used to toggle the class debug variable
	"
	" Parent: Logger
	"""	
	def toggleDebug(self):
		self.DEBUG = not self.DEBUG
		if(self.DEBUG): self.logOutput("DEBUG set to TRUE", 0)
		else: self.logOutput("DEBUG set to FALSE", 0)






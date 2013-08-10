from PyQt4 import QtGui,QtCore

class codeArena(QtGui.QTextEdit):
	def __init__(self,parent):
		super(codeArena,self).__init__()
		self.parent=parent
		
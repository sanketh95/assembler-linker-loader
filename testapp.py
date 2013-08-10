'''
Whats up bro ! \m/
'''

import sys
from PyQt4 import QtGui,QtCore
from codeArena import *
import assembler

class Example(QtGui.QMainWindow):
	def __init__(self):
		super(Example,self).__init__()
		self.loadedFromFile=False
		self.openFilePath=''
		self.savedToFile=True
		self.initUI()
	'''
	Initialize the GUI for the program
	'''
	def initUI(self):
		
		#The main gridlayout
		self.maingrid=QtGui.QGridLayout()
		
		#The widgets
		self.input=codeArena(self)
		self.input.setUndoRedoEnabled(True)
		self.input.textChanged.connect(self.setTextChangedStatus)
		
		self.output=QtGui.QTextEdit()
		self.output.setReadOnly(True)
		#The labels
		self.inpl=QtGui.QLabel('Enter file names each in one line')
		self.outl=QtGui.QLabel('Output here!')
		
		#Adding the widgets to the gridlayout
		self.maingrid.addWidget(self.inpl,0,0)
		self.maingrid.addWidget(self.outl,0,1)
		self.maingrid.addWidget(self.input,1,0,5,1)
		self.maingrid.addWidget(self.output,1,1,5,1)
		
		#The footer
		self.footer=QtGui.QHBoxLayout()
		
		#The footer widgets
		#The assemble button
		self.assembleBtn=QtGui.QPushButton('Assemble')
		self.assembleBtn.resize(self.assembleBtn.sizeHint())
		self.assembleBtn.setStatusTip('Assemble Code')
		self.assembleBtn.clicked.connect(self.assemble)
		
		#The exit button
		self.exitBtn=QtGui.QPushButton('Exit Application')
		self.exitBtn.resize(self.exitBtn.sizeHint())
		self.exitBtn.setStatusTip('Exit Application')
		self.exitBtn.clicked.connect(self.close)
		
		#Adding footer widgets to the footer
		self.footer.addWidget(self.assembleBtn)
		self.footer.addWidget(self.exitBtn)
		
		#The main vertical layout
		self.mainvl=QtGui.QVBoxLayout()
		self.mainvl.addLayout(self.maingrid)
		self.mainvl.addLayout(self.footer)
		
		#The QWidget properties
		self.mainwid=QtGui.QWidget()
		self.mainwid.setLayout(self.mainvl)
		self.mainwid.setWindowTitle('Easy Assembly')
		
		#statusBar of the qmainwindow
		self.statusBar()
		
		#Menubar
		menubar=self.menuBar()
		
		#Menus
		
		#Add any menus to the menubar here
		
		fileMenu=menubar.addMenu('&File')
		
		#Filemenu actions
		'''
		The exitaction - Exits the software
		The saveAction - save the text in the input box to a file
		The OpenAction - The open action opens the files and loads the data into input qtextedit 
		'''
		#The exitAction
		exitAction=QtGui.QAction(QtGui.QIcon('exit.png'),'&Exit',self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit Application')
		exitAction.triggered.connect(self.close)
		#The save action
		saveAction=QtGui.QAction(QtGui.QIcon('save.jpg'),'&Save',self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.setStatusTip('Save')
		saveAction.triggered.connect(self.saveToFile)
		#The save as action
		saveAsAction=QtGui.QAction(QtGui.QIcon('saveas.jpg'),'&Save As',self)
		saveAsAction.setShortcut('Ctrl+Shift+S')
		saveAsAction.setStatusTip('Save As')
		saveAsAction.triggered.connect(self.showSaveDialog)
		#Open action
		openAction=QtGui.QAction(QtGui.QIcon('open.jpg'),'&Open',self)
		openAction.setStatusTip('Open')
		openAction.setShortcut('Ctrl+O')
		openAction.triggered.connect(self.openFromFile)
		#The New Action
		newAction=QtGui.QAction(QtGui.QIcon('new.jpg'),'&New',self)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip('New')
		newAction.triggered.connect(self.newTrigger)
		#Adding actions to fileMenu
		fileMenu.addAction(newAction)
		fileMenu.addAction(openAction)
		fileMenu.addAction(saveAction)
	#	fileMenu.addAction(saveAsAction)
		fileMenu.addAction(exitAction)
		
		#The window properties
		self.setGeometry(300,300,600,400)
		self.setCentralWidget(self.mainwid)
		self.setWindowTitle('Easy Assembly')
		self.show()
		
	def assemble(self):
		text=self.input.toPlainText()
		ass=assembler.syntaxCheck(text,self)
		self.setOutputText('Assembled and output saved to output.txt file')
		f = open('output.txt','r')
		s = f.read()
		print s
		self.output.setText(s)
		
	def showOpenDialog(self):
		fileName=QtGui.QFileDialog.getOpenFileName(self,'Open File')
		#If invalid filename return false
		if fileName==self.openFilePath:
			return False
		if not self.validFileName(fileName):
			return False
		self.openFilePath=fileName
		return True	
		
	#shows save dialog	
	def showSaveDialog(self):
		fileName=QtGui.QFileDialog.getSaveFileName(self,'Save File')
		return fileName
	
	#gets called if saveAction triggered
	def saveToFile(self):
		if self.loadedFromFile:
			if self.validFileName(self.openFilePath):
				if not self.savedToFile:
					self.saveCode(self.openFilePath)
					self.setOutputText('Saving to '+self.openFilePath+' ....')
					self.savedToFile=True
					return True
				else:
					self.setOutputText('Already saved....')
					return True
		else:
			if self.textValid():
				fileName=self.showSaveDialog()
				if self.validFileName(fileName):
					self.saveCode(fileName)
					self.setOutputText('Saving to '+fileName)
					self.savedToFile=True
					return True
				else:
					return False
			else:
				self.setOutputText('Input box empty....')
				return True

	#Gets called if saveAsAction triggered
	def saveAs(self):
		fileName=self.showSaveDialog()
		if self.validFileName(fileName):
			pass
		else:
			pass
	
	#gets called if openAction triggered
	def openFromFile(self):
		if self.savedToFile:
			if not self.loadedFromFile:
				if self.showOpenDialog():
					self.openCode(self.openFilePath)
					self.loadedFromFile=True
					self.savedToFile=True
					self.setOutputText('Opened from '+self.openFilePath+' ....')
					return True
				else:
					'''
					Invalid filename
					'''
					self.setOutputText('Invalid filename...')
					return False
			else:
				'''
				show popup Are you sure ?
				if yes open new file
				else dont open
				'''
				self.setOutputText('Are you sure?')
				
		else:
			'''
			popup message
			'Do you want to save the file ?'
			IF yes save, set savedToFile to True and call openCode()
			else just call openCode()
			'''
			resultTrue=self.showPromptMessage('Do you want to save the file?')
			if resultTrue==1:
				if self.saveToFile():
					self.openFromFile()
				else:
					pass
			elif resultTrue==0:
				self.savedToFile=True
				if not self.openFromFile():
					self.savedToFile=False
			else:
				pass
			
	
	#Validate the filename
	def validFileName(self,name):
		if name=="":
			return False
		return True
		
	#Actually writes to the file
	def saveCode(self,name):
		f=open(name,'w')
		f.write(str(self.input.toPlainText()))
		f.close()
	
	#Open code from the file path name
	def openCode(self,name):
		f=open(name,'r')
		textFromFile=f.read()
		self.input.setText(str(textFromFile))
		f.close()
	
	
	#Displaying output
	def setOutputText(self,text):
		self.output.append(text)
	
	#If newAction is triggered
	def newTrigger(self):
		self.input.setText('')
		self.output.setText('')
		self.loadedFromFile=False
		self.openFilePath=''
		self.savedToFile=''
	
	#If the text in the input textedit is changed
	def setTextChangedStatus(self):
		if self.savedToFile:
			self.savedToFile=False
			
	#To check if the text in the input qtextedit is valid 
	def textValid(self):
		if self.input.toPlainText() == "":
			return False
		else:
			return True
			
	#Escape key pressed then close the window		
	def keyPressEvent(self,e):
		if e.key() == QtCore.Qt.Key_Escape:
			self.close()
	
	#Show yes or no message
	'''
	Displays a yes or no message whose value must be passed as parameter to the method
	'''
	def showPromptMessage(self,message):
		reply=QtGui.QMessageBox.question(self,'Message',message,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
		if reply == QtGui.QMessageBox.No:
			return 0
		elif reply == QtGui.QMessageBox.Yes:
			return 1
		elif reply == QtGui.QMessageBox.Cancel:
			return 2
			
	def closeEvent(self,e):
		if self.savedToFile:
			e.accept()
		else:
			resultTrue = self.showPromptMessage('Do you want to save before quitting?')
			if resultTrue==1:
				self.saveToFile()
				e.accept()
			elif resultTrue==0:
				e.accept()
			else:
				e.ignore()
	
def main():
	app=QtGui.QApplication(sys.argv)
	ex=Example()
	sys.exit(app.exec_())
	
	
	
if __name__=='__main__':
	main()
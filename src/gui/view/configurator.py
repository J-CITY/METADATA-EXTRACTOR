import os, sys
parentPath = os.path.abspath("../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
print(parentPath)

import config.strings_en as strings
from gui.view.card.nameCard import NameCard
from gui.view.card.keywordCard import KeywordCard
from gui.view.card.locationCard import LocationCard
from gui.view.card.referenceCard import ReferenceCard
from gui.view.card.contactCard import ContactCard
from gui.view.card.infoCard import InfoCard

from gui.view.dialog.aboutDialog import AboutDialog
from gui.view.dialog.settingsDialog import SettingsDialog

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QCheckBox
from PyQt5.QtWidgets import (QGroupBox, QFileDialog, QComboBox, QProgressBar, 
	QFormLayout, QScrollArea, QLineEdit, QLabel, QGridLayout, QListWidget,QListWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl
from PyQt5 import QtWebEngineWidgets
from gui.view.tabs.tabWidget import TabWidget

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = strings.TITLE
		self.left = 100
		self.top = 100
		self.width = 500
		self.height = 300

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.mainWidget = TabWidget(self)
		self.setCentralWidget(self.mainWidget)

		self.initActions()
		#self.show()
	def setProgress(self, p):
		self.mainWidget.tabControl.setProgress(p)
	def isVisibleProgress(self, isV):
		self.mainWidget.tabControl.isVisibleProgress(isV)
	def _extractOcClick(self):
		self.presenter.extractOcClick()
	def _loadOcClick(self):
		self.presenter.loadOcClick()
	def _loadFileOcClick(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			print(fileName)
			self.presenter.loadFileOcClick(fileName)
	def _saveFileOcClick(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
		if fileName:
			print(fileName)
			self.presenter.saveFileOnClick(fileName)
	def _openFileOnClick(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			print(fileName)
			self.presenter.openFileOnClick(fileName)
	def _aboutOcClick(self):
		self.aboutDialog = AboutDialog()
	def _helpOcClick(self):
		self.view = QtWebEngineWidgets.QWebEngineView()

		pth = os.path.split(os.path.abspath(__file__))[0]
		pth = os.path.dirname(os.path.dirname(pth))

		self.view.load(QUrl().fromLocalFile(pth + '/doc/index.html'))
		self.view.show()
	def _settingsOcClick(self):
		self.settingsDialog = SettingsDialog(self.presenter)
	def initActions(self):
		self.exitAction = QAction(QIcon(strings.ICON_CLOSE), strings.MENU_EXIT, self)
		self.exitAction.setShortcut('Ctrl+Q')
		self.exitAction.setStatusTip(strings.MENU_TOOLTIP_EXIT)
		self.exitAction.triggered.connect(self.close)

		self.openAction = QAction(QIcon(strings.ICON_OPEN), strings.MENU_OPEN, self)
		self.openAction.setShortcut('Ctrl+O')
		self.openAction.setStatusTip(strings.MENU_TOOLTIP_OPEN_PDF)
		self.openAction.triggered.connect(self._openFileOnClick)

		self.saveAction = QAction(QIcon(strings.ICON_SAVE), strings.MENU_SAVE, self)
		self.saveAction.setShortcut('Ctrl+S')
		self.saveAction.setStatusTip(strings.MENU_TOOLTIP_SAVE_METADATA)
		self.saveAction.triggered.connect(self._saveFileOcClick)

		self.extractAction = QAction(QIcon(strings.ICON_PROCESS), strings.MENU_EXTRACT, self)
		self.extractAction.setShortcut('Ctrl+E')
		self.extractAction.setStatusTip(strings.MENU_TOOLTIP_EXTRACT_METADATA)
		self.extractAction.triggered.connect(self._extractOcClick)

		self.loadAction = QAction(QIcon(strings.ICON_LOAD), strings.MENU_LOAD, self)
		self.loadAction.setShortcut('Ctrl+L')
		self.loadAction.setStatusTip(strings.MENU_TOOLTIP_LOAD_METADATA)
		self.loadAction.triggered.connect(self._loadOcClick)

		self.loadFileAction = QAction(QIcon(strings.ICON_LOAD), strings.MENU_FILE_LOAD, self)
		self.loadFileAction.setShortcut('Ctrl+F')
		self.loadFileAction.setStatusTip(strings.MENU_TOOLTIP_LOAD_FILE_METADATA)
		self.loadFileAction.triggered.connect(self._loadFileOcClick)

		self.aboutAction = QAction(QIcon(''), strings.MENU_ABOUT, self)
		self.aboutAction.setShortcut('F2')
		self.aboutAction.setStatusTip(strings.MENU_TOOLTIP_ABOUT)
		self.aboutAction.triggered.connect(self._aboutOcClick)

		self.helpAction = QAction(QIcon(''), strings.MENU_HELP, self)
		self.helpAction.setShortcut('F1')
		self.helpAction.setStatusTip(strings.MENU_TOOLTIP_HELP)
		self.helpAction.triggered.connect(self._helpOcClick)

		self.settingsAction = QAction(QIcon(''), strings.MENU_SETTINGS, self)
		self.settingsAction.setShortcut('F3')
		self.settingsAction.setStatusTip(strings.MENU_TOOLTIP_SETTINGS)
		self.settingsAction.triggered.connect(self._settingsOcClick)

		self.statusBar()

		self.menubar = self.menuBar()
		mb = self.menubar.addMenu(strings.MENU_FILE)
		mb.addAction(self.exitAction)
		mb.addAction(self.openAction)
		mb.addAction(self.saveAction)
		mb.addAction(self.extractAction)
		mb.addAction(self.loadAction)
		mb.addAction(self.loadFileAction)

		helps = self.menubar.addMenu(strings.MENU_QUESTION)
		helps.addAction(self.helpAction)
		helps.addAction(self.settingsAction)
		helps.addAction(self.aboutAction)

		self.toolbar = self.addToolBar(strings.MENU_EXIT)
		self.toolbar.addAction(self.exitAction)
		self.toolbar.addAction(self.openAction)
		self.toolbar.addAction(self.saveAction)
		self.toolbar.addAction(self.extractAction)
		self.toolbar.addAction(self.loadAction)
	def statusErr(self, err):
		self.statusBar().showMessage(err, 2000)
	def setPresenter(self, p):
		self.presenter = p
		self.mainWidget.setPresenter(p)

	def setNamesData(self, names):
		for n in self.mainWidget.tabControlPerson.names:
			n.clearLayout(n.grid)
			n.deleteLater()
			n = None
		self.mainWidget.tabControlPerson.listWidget.clear()
		self.mainWidget.tabControlPerson.names = []

		for i in range(len(names)):
			self.mainWidget.tabControlPerson.addNameWithData(names[i])
			print(i)

	def setKeywordsData(self, kw, loc):
		for n in self.mainWidget.tabControlKeyword.keywords:
			n.clearLayout(n.grid)
			n.deleteLater()
			n = None
		self.mainWidget.tabControlKeyword.listKWWidget.clear()
		self.mainWidget.tabControlKeyword.keywords = []

		for n in self.mainWidget.tabControlKeyword.locations:
			n.clearLayout(n.grid)
			n.deleteLater()
			n = None
		self.mainWidget.tabControlKeyword.listLOCWidget.clear()
		self.mainWidget.tabControlKeyword.locations = []

		for i in range(len(kw)):
			self.mainWidget.tabControlKeyword.addKeywordWithData(kw[i])
			print(i)
		for i in range(len(loc)):
			self.mainWidget.tabControlKeyword.addKeywordLocWithData(loc[i])
			print(i)

	def setLocationsData(self, loc):
		for n in self.mainWidget.tabControlLocation.locations:
			n.clearLayout(n.grid)
			n.deleteLater()
			n = None
		self.mainWidget.tabControlLocation.listWidget.clear()
		self.mainWidget.tabControlLocation.locations = []

		for i in range(len(loc)):
			self.mainWidget.tabControlLocation.addLocationWithData(loc[i])
			print(i)
	
	def setReferencesData(self, ref):
		for n in self.mainWidget.tabControlReference.references:
			n.clearLayout(n.grid)
			n.deleteLater()
			n = None
		self.mainWidget.tabControlReference.listWidget.clear()
		self.mainWidget.tabControlReference.references = []

		for i in range(len(ref)):
			self.mainWidget.tabControlReference.addReferenceWithData(ref[i])
			print(i)

	def setInfoData(self, t, db, de):
		self.mainWidget.tabControlInfo.addData(t, db, de)
	def setUUID(self, uuid):
		self.mainWidget.tabControlInfo.eUUID.setText(uuid)


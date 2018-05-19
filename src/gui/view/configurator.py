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

class TabWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.layout = QVBoxLayout(self)

		# Initialize tab screen
		self.tabs = QTabWidget()
		self.tabControl = ControlTabWidget(self)
		self.tabControlPerson = ControlPersonWidget(self)
		self.tabControlKeyword = ControlKeywordWidget(self)
		self.tabControlLocation = ControlLocationWidget(self)
		self.tabControlReference = ControlReferenceWidget(self)
		self.tabControlContact = ContactCard(self)
		self.tabControlInfo = InfoCard(self)
		self.tabs.resize(300,200)

		# Add tabs
		self.tabs.addTab(self.tabControl, strings.TAB_CONTROL)
		self.tabs.addTab(self.tabControlInfo, strings.TAB_INFO)
		self.tabs.addTab(self.tabControlContact, strings.TAB_CONTACT)
		self.tabs.addTab(self.tabControlPerson, strings.TAB_PERSON)
		self.tabs.addTab(self.tabControlKeyword, strings.TAB_KEYWORD)
		self.tabs.addTab(self.tabControlLocation, strings.TAB_LOCATION)
		self.tabs.addTab(self.tabControlReference, strings.TAB_REFERENCE)

		# Add tabs to widget
		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)

	def setPresenter(self, p):
		#self.presenter = p
		self.tabControl.setPresenter(p)
		self.tabControlPerson.setPresenter(p)
		self.tabControlKeyword.setPresenter(p)
		self.tabControlLocation.setPresenter(p)
		self.tabControlReference.setPresenter(p)
		self.tabControlContact.setPresenter(p)
		self.tabControlInfo.setPresenter(p)

class ControlTabWidget(QWidget):
	#openFileOnClick = pyqtSignal([str])

	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.fileName = ""

		# Create first tab
		self.layout = QFormLayout(self)
		
		self.btnLoad = QPushButton(strings.LOAD)
		self.btnLoad.setToolTip(strings.TOOLTIP_LOAD_PDF)
		self.btnLoad.clicked.connect(self._openFileOnClick)

		self.cbMetaTitle = QCheckBox(strings.META_TITLE, self)
		self.cbMetaTitle.toggle()
		self.cbMetaTitle.stateChanged.connect(self._checkTitleOnClick)
		self.cbMetaContent = QCheckBox(strings.META_CONTENT, self)
		self.cbMetaContent.toggle()
		self.cbMetaContent.stateChanged.connect(self._checkContentOnClick)
		self.cbMetaName = QCheckBox(strings.META_NAMES, self)
		self.cbMetaName.toggle()
		self.cbMetaName.stateChanged.connect(self._checkNameOnClick)
		self.cbMetaLocation = QCheckBox(strings.META_LOCATIONS, self)
		self.cbMetaLocation.toggle()
		self.cbMetaLocation.stateChanged.connect(self._checkLocationOnClick)
		self.cbMetaKeyword = QCheckBox(strings.META_KEYWORD, self)
		self.cbMetaKeyword.toggle()
		self.cbMetaKeyword.stateChanged.connect(self._checkKeywordOnClick)
		self.cbMetaRef = QCheckBox(strings.META_REF, self)
		self.cbMetaRef.toggle()
		self.cbMetaRef.stateChanged.connect(self._checkRefOnClick)
		
		self.combo = QComboBox(self)
		self.combo.addItems([strings.TYPE_TXT, strings.TYPE_ISO19115v2, strings.TYPE_FGDC])
		self.combo.activated[str].connect(self._setTypeOnClick)

		self.btnSave = QPushButton(strings.SAVE)
		self.btnSave.setToolTip(strings.TOOLTIP_SAVE_METADATA)
		self.btnSave.clicked.connect(self._saveFileOcClick)

		self.btnExtract = QPushButton(strings.EXTRACT)
		self.btnExtract.setToolTip(strings.TOOLTIP_EXTRACT_METADATA)
		self.btnExtract.clicked.connect(self._extractOcClick)

		self.layout.addRow(self.btnLoad)
		self.layout.addRow(self.cbMetaTitle)
		self.layout.addRow(self.cbMetaContent)
		self.layout.addRow(self.cbMetaName)
		self.layout.addRow(self.cbMetaLocation)
		self.layout.addRow(self.cbMetaKeyword)
		self.layout.addRow(self.cbMetaRef)
		self.layout.addRow(self.combo)
		self.layout.addRow(self.btnExtract)
		self.layout.addRow(self.btnSave)

		self.bar = QProgressBar()
		self.bar.setValue(0)
		self.bar.setVisible(False)
		self.layout.addRow(self.bar)
		#self.setLayout(self.tab1.layout)

	def setProgress(self, p):
		self.bar.setValue(p)
	def isVisibleProgress(self, isV):
		self.bar.setVisible(isV)

	def _setTypeOnClick(self, state):
		self.presenter.setTypeOnClick(state)

	def _checkTitleOnClick(self, state):
		self.presenter.checkTitleOnClick(state)
	def _checkContentOnClick(self, state):
		self.presenter.checkContentOnClick(state)
	def _checkNameOnClick(self, state):
		self.presenter.checkNameOnClick(state)
	def _checkLocationOnClick(self, state):
		self.presenter.checkLocationOnClick(state)
	def _checkKeywordOnClick(self, state):
		self.presenter.checkKeywordOnClick(state)
	def _checkRefOnClick(self, state):
		self.presenter.checkRefOnClick(state)

	def setPresenter(self, p):
		self.presenter = p

	def _extractOcClick(self):
		self.presenter.extractOcClick()

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


class ControlPersonWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.names = []
		#self.listItems = []

		# Create first tab
		self.layout = QVBoxLayout(self)
		
		self.btnAdd = QPushButton(strings.BTN_ADD)
		self.btnAdd.setToolTip(strings.TOOLTIP_ADD_PERSON)
		self.btnAdd.clicked.connect(self._addName)
		self.layout.addWidget(self.btnAdd)

		self.listWidget = QListWidget()

		self.layout.addWidget(self.listWidget)
		#self.setLayout(self.tab1.layout)

	def _addName(self):
		n = NameCard(self)
		self.names.append(n)
		n.setId(len(self.names))
		n.setPresenter(self.presenter)

		widgetItem = QListWidgetItem(self.listWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listWidget.addItem(widgetItem)
		self.listWidget.setItemWidget(widgetItem, n)
		#self.listItems.append(widgetItem)

		self.presenter.addName()

	def addNameWithData(self, name):
		n = NameCard(self)
		self.names.append(n)
		n.setId(len(self.names))
		n.setPresenter(self.presenter)
		n.eName.setText(name.name)
		n.eOrganisation.setText(name.organisation)
		n.ePhone.setText(name.phone)
		n.eFacs.setText(name.facs)
		n.eDeliveryPoint.setText(name.deliveryPoint)
		n.eCity.setText(name.city)
		n.eArea.setText(name.area)
		n.ePostalCode.setText(name.postalCode)
		n.eCountry.setText(name.country)
		n.eEmail.setText(name.email)

		widgetItem = QListWidgetItem(self.listWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listWidget.addItem(widgetItem)
		self.listWidget.setItemWidget(widgetItem, n)
		#self.listItems.append(widgetItem)

		#self.presenter.addName()

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def delName(self, id):
		self.names[id-1].deleteLater()
		self.names[id-1:id] = []

		items = self.listWidget.count()
		selectedItems=[]
		itemsText=[]
		rangedList = list(range(items))
		rangedList.reverse()
		#for i in rangedList:
		#	if i == id-1:
		self.listWidget.takeItem(id-1)
		#update id
		id = 1
		for n in self.names:
			n.setId(id)
			id += 1
	def setPresenter(self, p):
		self.presenter = p

class ControlKeywordWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.keywords = []
		self.locations = []
		#self.listItems = []

		# Create first tab
		self.layout = QVBoxLayout(self)
		
		self.btnAddkw = QPushButton(strings.BTN_ADD)
		self.btnAddkw.setToolTip(strings.TOOLTIP_ADD_KEYWORD)
		self.btnAddkw.clicked.connect(self._addKeyword)
		self.layout.addWidget(self.btnAddkw)
		self.listKWWidget = QListWidget()
		self.layout.addWidget(self.listKWWidget)

		self.btnAddloc = QPushButton(strings.BTN_ADD)
		self.btnAddloc.setToolTip(strings.TOOLTIP_ADD_LOCATION)
		self.btnAddloc.clicked.connect(self._addLocation)
		self.layout.addWidget(self.btnAddloc)
		self.listLOCWidget = QListWidget()
		self.layout.addWidget(self.listLOCWidget)
		#self.setLayout(self.tab1.layout)

	def _addKeyword(self):
		n = KeywordCard(self, "keyword")
		self.keywords.append(n)
		n.setId(len(self.keywords))
		n.setPresenter(self.presenter)

		widgetItem = QListWidgetItem(self.listKWWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listKWWidget.addItem(widgetItem)
		self.listKWWidget.setItemWidget(widgetItem, n)

		self.presenter.addKeyword()

	def _addLocation(self):
		n = KeywordCard(self, "location")
		self.locations.append(n)
		n.setId(len(self.locations))
		n.setPresenter(self.presenter)

		widgetItem = QListWidgetItem(self.listLOCWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listLOCWidget.addItem(widgetItem)
		self.listLOCWidget.setItemWidget(widgetItem, n)

		self.presenter.addKeywordLocation()

	def addKeywordWithData(self, kw):
		n = KeywordCard(self, "keyword")
		self.keywords.append(n)
		n.setId(len(self.keywords))
		n.setPresenter(self.presenter)
		
		n.eName.setText(kw.keyword)
		n.eType.setText(kw.type)
		
		widgetItem = QListWidgetItem(self.listKWWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listKWWidget.addItem(widgetItem)
		self.listKWWidget.setItemWidget(widgetItem, n)

		#self.presenter.addKeyword()

	def addKeywordLocWithData(self, kw):
		n = KeywordCard(self, "location")
		self.locations.append(n)
		n.setId(len(self.locations))
		n.setPresenter(self.presenter)
		
		n.eName.setText(kw.keyword)
		n.eType.setText(kw.type)
		
		widgetItem = QListWidgetItem(self.listLOCWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listLOCWidget.addItem(widgetItem)
		self.listLOCWidget.setItemWidget(widgetItem, n)

		#self.presenter.addKeyword()

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def delKeyword(self, id):
		self.keywords[id-1].deleteLater()
		self.keywords[id-1:id] = []

		items = self.listKWWidget.count()
		selectedItems=[]
		itemsText=[]
		rangedList = list(range(items))
		rangedList.reverse()
		self.listKWWidget.takeItem(id-1)
		#update id
		id = 1
		for n in self.keywords:
			n.setId(id)
			id += 1
	def delKeywordLoc(self, id):
		self.locations[id-1].deleteLater()
		self.locations[id-1:id] = []

		items = self.listLOCWidget.count()
		selectedItems=[]
		itemsText=[]
		rangedList = list(range(items))
		rangedList.reverse()
		self.listLOCWidget.takeItem(id-1)
		#update id
		id = 1
		for n in self.locations:
			n.setId(id)
			id += 1
	def setPresenter(self, p):
		self.presenter = p

class ControlLocationWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.locations = []
		#self.listItems = []

		# Create first tab
		self.layout = QVBoxLayout(self)
		
		self.btnAdd = QPushButton(strings.BTN_ADD)
		self.btnAdd.setToolTip(strings.TOOLTIP_ADD_LOCATION)
		self.btnAdd.clicked.connect(self._addLocation)
		self.layout.addWidget(self.btnAdd)
		self.listWidget = QListWidget()
		self.layout.addWidget(self.listWidget)


	def _addLocation(self):
		n = LocationCard(self)
		self.locations.append(n)
		n.setId(len(self.locations))
		n.setPresenter(self.presenter)

		widgetItem = QListWidgetItem(self.listWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listWidget.addItem(widgetItem)
		self.listWidget.setItemWidget(widgetItem, n)

		self.presenter.addLocation()

	def addLocationWithData(self, loc):
		n = LocationCard(self)
		self.locations.append(n)
		n.setId(len(self.locations))
		n.setPresenter(self.presenter)
		
		n.eName.setText(loc.name)
		n.eWest.setText(loc.west)
		n.eEast.setText(loc.east)
		n.eNorth.setText(loc.north)
		n.eSouth.setText(loc.south)


		widgetItem = QListWidgetItem(self.listWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listWidget.addItem(widgetItem)
		self.listWidget.setItemWidget(widgetItem, n)

		#self.presenter.addLocation()

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def delLocation(self, id):
		self.locations[id-1].deleteLater()
		self.locations[id-1:id] = []

		items = self.listWidget.count()
		selectedItems=[]
		itemsText=[]
		rangedList = list(range(items))
		rangedList.reverse()
		self.listWidget.takeItem(id-1)
		#update id
		id = 1
		for n in self.locations:
			n.setId(id)
			id += 1

	def setPresenter(self, p):
		self.presenter = p

class ControlReferenceWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.references = []

		# Create first tab
		self.layout = QVBoxLayout(self)
		
		self.btnAdd = QPushButton(strings.BTN_ADD)
		self.btnAdd.setToolTip(strings.TOOLTIP_ADD_REFERENCE)
		self.btnAdd.clicked.connect(self._addReference)
		self.layout.addWidget(self.btnAdd)
		self.listWidget = QListWidget()
		self.layout.addWidget(self.listWidget)

	def _addReference(self):
		n = ReferenceCard(self)
		self.references.append(n)
		n.setId(len(self.references))
		n.setPresenter(self.presenter)

		widgetItem = QListWidgetItem(self.listWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listWidget.addItem(widgetItem)
		self.listWidget.setItemWidget(widgetItem, n)

		self.presenter.addReference()

	def addReferenceWithData(self, ref):
		n = ReferenceCard(self)
		self.references.append(n)
		n.setId(len(self.references))
		n.setPresenter(self.presenter)
		
		n.eOrigin.setText(ref.origin)
		n.eDate.setText(ref.date)
		n.eTitle.setText(ref.title)
		n.eLink.setText(ref.link)

		widgetItem = QListWidgetItem(self.listWidget)
		widgetItem.setSizeHint(n.sizeHint())
		self.listWidget.addItem(widgetItem)
		self.listWidget.setItemWidget(widgetItem, n)

		#self.presenter.addLocation()

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def delReference(self, id):
		self.references[id-1].deleteLater()
		self.references[id-1:id] = []

		items = self.listWidget.count()
		selectedItems=[]
		itemsText=[]
		rangedList = list(range(items))
		rangedList.reverse()
		self.listWidget.takeItem(id-1)
		#update id
		id = 1
		for n in self.references:
			n.setId(id)
			id += 1

	def setPresenter(self, p):
		self.presenter = p

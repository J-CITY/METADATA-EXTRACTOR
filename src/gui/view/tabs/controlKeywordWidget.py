import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

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

class ControlKeywordWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.keywords = []
		self.locations = []
		#self.listItems = []

		# Create first tab
		self.layout = QVBoxLayout(self)
		
		self.lKw     = QLabel(strings.LABLE_KEY_WORD)
		self.btnAddkw = QPushButton(strings.BTN_ADD)
		self.btnAddkw.setToolTip(strings.TOOLTIP_ADD_KEYWORD)
		self.btnAddkw.clicked.connect(self._addKeyword)
		self.layout.addWidget(self.lKw)
		self.layout.addWidget(self.btnAddkw)
		self.listKWWidget = QListWidget()
		self.layout.addWidget(self.listKWWidget)

		self.lLoc     = QLabel(strings.LABLE_LOCATION)
		self.btnAddloc = QPushButton(strings.BTN_ADD)
		self.btnAddloc.setToolTip(strings.TOOLTIP_ADD_LOCATION)
		self.btnAddloc.clicked.connect(self._addLocation)
		self.layout.addWidget(self.lLoc)
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

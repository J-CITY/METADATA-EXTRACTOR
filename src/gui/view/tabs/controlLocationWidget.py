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

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

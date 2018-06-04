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

from gui.view.tabs.controlReferenceWidget import ControlReferenceWidget
from gui.view.tabs.controlLocationWidget import ControlLocationWidget
from gui.view.tabs.controlKeywordWidget import ControlKeywordWidget
from gui.view.tabs.controlPersonWidget import ControlPersonWidget
from gui.view.tabs.controlTabWidget import ControlTabWidget

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

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

class ControlTabWidget(QWidget):
	#openFileOnClick = pyqtSignal([str])

	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.fileName = ""

		# Create first tab
		self.layout = QFormLayout(self)
		
		self.btnLoad = QPushButton(strings.OPEN)
		self.btnLoad.setToolTip(strings.TOOLTIP_OPEN_PDF)
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

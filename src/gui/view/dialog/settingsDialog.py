import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
import config.strings_en as strings

from converter.preferences import Preferences

from PyQt5.QtWidgets import (QWidget, QDialog, QGroupBox, QGridLayout,
	QLineEdit, QPushButton, QFormLayout, QLabel, QTabWidget, QComboBox)

class SettingsDialog(QDialog):
	def __init__(self, p):
		super().__init__()
		self.presenter = p
		self.initUI()

	def initUI(self):
		
		# Initialize tab screen
		self.tabs = QTabWidget()
		self.genGroupLogin() 
		self.genGroupExtract() 
		
		# Add tabs
		self.tabs.addTab(self.groupBoxLogin, "Login")
		self.tabs.addTab(self.groupBoxExtract, "Extract")

		self.grid = QGridLayout(self)
		self.grid.addWidget(self.tabs, 0, 0)
		self.setLayout(self.grid)

		self.setWindowTitle(strings.DIALOG_TITLE_SETTINGS)
		self.setPreferences()
		#self.setFixedSize(200, 120)
		self.exec_()

	def _listChanged(self,i):
		#self.grid = QGridLayout()
		#self.grid.addWidget(self.list, 0, 0)
		if i == 0:
			self.grid.addWidget(self.groupBoxLogin, 0, 1)
		elif i == 1:
			self.grid.addWidget(self.groupBoxExtract, 0, 1)
		#self.setLayout(self.grid)
		
	def genGroupLogin(self):
		self.groupBoxLogin = QGroupBox("Login")

		self.lProtocol = QLabel("Protolol")
		self.protocol = QComboBox(self)
		self.protocol.addItems(["http", "https"])
		self.protocol.currentIndexChanged.connect(self._changeProtocol)
		self.lUrl = QLabel("URL")
		self.url = QLineEdit(self)
		self.url.textChanged.connect(self._changeUrl)
		self.lLogin = QLabel("Login")
		self.login = QLineEdit(self)
		self.login.textChanged.connect(self._changeLogin)
		self.lPassword = QLabel("Password")
		self.password = QLineEdit(self)
		self.password.textChanged.connect(self._changePassword)

		self.vboxl = QFormLayout()
		self.vboxl.addRow(self.lProtocol, self.protocol)
		self.vboxl.addRow(self.lUrl, self.url)
		self.vboxl.addRow(self.lLogin, self.login)
		self.vboxl.addRow(self.lPassword, self.password)
		
		self.groupBoxLogin.setLayout(self.vboxl)

	def _changeProtocol(self, i):
		self.presenter.updateSettings("LOGIN", "protocol", self.protocol.currentText())
	def _changeUrl(self, text):
		self.presenter.updateSettings("LOGIN", "url", text)
	def _changeLogin(self, text):
		self.presenter.updateSettings("LOGIN", "user", text)
	def _changePassword(self, text):
		self.presenter.updateSettings("LOGIN", "passwd", text)

	def genGroupExtract(self):
		self.groupBoxExtract = QGroupBox("Extract")

		self.lFileCodec = QLabel("Codec")
		self.fileCodec = QLineEdit(self)
		self.fileCodec.textChanged.connect(self._changeFileCodec)
		self.lOutPDFFormat = QLabel("PDF extractor")
		self.outPDFFormat = QComboBox(self)
		self.outPDFFormat.addItems(["filter", "text"])
		self.outPDFFormat.currentIndexChanged.connect(self._changeOutPDFFormat)

		self.lSentencesSplitterModel = QLabel("Split model")
		self.sentencesSplitterModel = QLineEdit(self)
		self.sentencesSplitterModel.textChanged.connect(self._changeSentencesSplitterModel)
		self.lTanimoto = QLabel("Tanimoto")
		self.tanimoto = QLineEdit(self)
		self.tanimoto.textChanged.connect(self._changeTanimoto)
		
		self.lStopWords = QLabel("Stop words")
		self.stopWords = QLineEdit(self)
		self.stopWords.textChanged.connect(self._changeStopWords)
		self.lPunctuations = QLabel("Punctuations")
		self.punctuations = QLineEdit(self)
		self.punctuations.textChanged.connect(self._changePunctuations)

		self.lMaxKeyPhraseLength = QLabel("Max lengs of key phrase")
		self.maxKeyPhraseLength = QLineEdit(self)
		self.maxKeyPhraseLength.textChanged.connect(self._changeMaxKeyPhraseLength)
		self.lCountKeyPhrases = QLabel("Count key phrases")
		self.countKeyPhrases = QLineEdit(self)
		self.countKeyPhrases.textChanged.connect(self._changeCountKeyPhrases)
		#outPDFFormat = 'filter'


		self.vboxe = QFormLayout()
		self.vboxe.addRow(self.lFileCodec, self.fileCodec)
		self.vboxe.addRow(self.lOutPDFFormat, self.outPDFFormat)
		self.vboxe.addRow(self.lSentencesSplitterModel, self.sentencesSplitterModel)
		self.vboxe.addRow(self.lTanimoto, self.tanimoto)
		self.vboxe.addRow(self.lStopWords, self.stopWords)
		self.vboxe.addRow(self.lPunctuations, self.punctuations)
		self.vboxe.addRow(self.lMaxKeyPhraseLength, self.maxKeyPhraseLength)
		self.vboxe.addRow(self.lCountKeyPhrases, self.countKeyPhrases)
		
		self.groupBoxExtract.setLayout(self.vboxe)

	def _changeOutPDFFormat(self, i):
		self.presenter.updateSettings("EXTRACT", "outPDFFormat", self.outPDFFormat.currentText())
	def _changeFileCodec(self, text):
		self.presenter.updateSettings("EXTRACT", "fileCodec", text)
	def _changeSentencesSplitterModel(self, text):
		self.presenter.updateSettings("EXTRACT", "sentencesSplitterModel", text)
	def _changeTanimoto(self, text):
		self.presenter.updateSettings("EXTRACT", "minTanimoto", text)
	def _changeStopWords(self, text):
		self.presenter.updateSettings("EXTRACT", "stopWords", text)
	def _changePunctuations(self, text):
		self.presenter.updateSettings("EXTRACT", "punctuations", text)
	def _changeMaxKeyPhraseLength(self, text):
		self.presenter.updateSettings("EXTRACT", "maxKeyPhraseLength", text)
	def _changeCountKeyPhrases(self, text):
		self.presenter.updateSettings("EXTRACT", "countKeyPhrases", text)

	def setPreferences(self):
		prefs = self.presenter.getPrefs()

		pr = prefs.getPref("LOGIN", "protocol")
		if pr == 'http':
			self.protocol.setCurrentIndex(0)
		elif pr == 'https':
			self.protocol.setCurrentIndex(1)
		self.url.setText(prefs.getPref("LOGIN", "url"))
		self.login.setText(prefs.getPref("LOGIN", "user"))
		self.password.setText(prefs.getPref("LOGIN", "passwd"))

		self.fileCodec.setText(prefs.getPref("EXTRACT", "fileCodec"))

		pr = prefs.getPref("EXTRACT", "outPDFFormat")
		if pr == 'filter':
			self.outPDFFormat.setCurrentIndex(0)
		elif pr == 'text':
			self.outPDFFormat.setCurrentIndex(1)
		
		self.sentencesSplitterModel.setText(prefs.getPref("EXTRACT", "sentencesSplitterModel"))
		self.tanimoto.setText(prefs.getPref("EXTRACT", "minTanimoto"))
		self.stopWords.setText(prefs.getPref("EXTRACT", "stopWords"))
		self.punctuations.setText(prefs.getPref("EXTRACT", "punctuations"))
		self.maxKeyPhraseLength.setText(prefs.getPref("EXTRACT", "maxKeyPhraseLength"))
		self.countKeyPhrases.setText(prefs.getPref("EXTRACT", "countKeyPhrases"))


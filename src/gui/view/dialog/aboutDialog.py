import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
import config.strings_en as strings

from PyQt5.QtWidgets import (QWidget, QDialog, QPushButton, QFormLayout, QLabel)

class AboutDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.lName     = QLabel(strings.LABLE_ABOUT_NAME+": Metadata Extractor")
		self.lVersion  = QLabel(strings.LABLE_ABOUT_VERSION + ": 0.8.5")
		self.lAuthor   = QLabel(strings.LABLE_ABOUT_AUTHOR + ": Glushchenko D. A.")
		#self.lHomePage = QLabel(strings.LABLE_ABOUT_HOME_PAGE)

		self.btnOk = QPushButton(strings.DIALOG_BTN_OK, self)
		self.btnOk.clicked.connect(self.close)

		self.grid = QFormLayout()
		self.grid.setSpacing(10)
		self.grid.addRow(self.lName)
		self.grid.addRow(self.lVersion)
		self.grid.addRow(self.lAuthor)
		self.grid.addRow(self.btnOk)
		self.setLayout(self.grid)

		self.setWindowTitle(strings.DIALOG_TITLE_ABOUT)
		self.setFixedSize(200, 120)
		self.exec_()


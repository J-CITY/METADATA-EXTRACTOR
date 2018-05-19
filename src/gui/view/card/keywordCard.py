import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

import config.strings_en as strings

from PyQt5.QtWidgets import (QLineEdit, QLabel, QGridLayout, 
	QListWidget,QListWidgetItem, QWidget, QPushButton)

class KeywordCard(QWidget):
	def __init__(self, parent, _type):
		super(QWidget, self).__init__(parent)

		self.type = _type

		self.id = 0
		self.fileName = ""

		# Create first tab
		self.lId    = QLabel(str(self.id))
		self.lName  = QLabel(strings.LABLE_NAME)
		self.lType  = QLabel(strings.LABLE_TYPE)

		self.btnDel = QPushButton(strings.DELETE)
		self.btnDel.setToolTip(strings.TOOLTIP_DELETE_ELEMENT)
		self.btnDel.clicked.connect(self._deleteOnClick)

		self.eName          = QLineEdit()
		self.eName.textChanged[str].connect(self._onKeywordNameChanged)
		self.eType  = QLineEdit()
		self.eType.textChanged[str].connect(self._onKeywordTypeChanged)

		self.grid = QGridLayout()
		self.grid.setSpacing(10)

		self.grid.addWidget(self.lId, 1, 0)
		self.grid.addWidget(self.btnDel, 1, 1)

		self.grid.addWidget(self.lName, 2, 0)
		self.grid.addWidget(self.eName, 2, 1)
		self.grid.addWidget(self.lType, 3, 0)
		self.grid.addWidget(self.eType, 3, 1)

		self.setLayout(self.grid)

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def _deleteOnClick(self):
		if self.type == "keyword":
			self.presenter.delKeywordFromList(self.id)
		elif self.type == "location":
			self.presenter.delKeywordLocFromList(self.id)

	def setPresenter(self, p):
		self.presenter = p
	
	def setId(self, id):
		self.id = id
		self.lId.setText(str(id))
	
	def _onKeywordNameChanged(self, text):
		if self.type == "keyword":
			self.presenter.onKeywordNameChanged(self.id-1, text, "keyword")
		elif self.type == "location":
			self.presenter.onKeywordNameChanged(self.id-1, text, "location")
	def _onKeywordTypeChanged(self, text):
		if self.type == "keyword":
			self.presenter.onKeywordTypeChanged(self.id-1, text, "keyword")
		elif self.type == "location":
			self.presenter.onKeywordTypeChanged(self.id-1, text, "location")


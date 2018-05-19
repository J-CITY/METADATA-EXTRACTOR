import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

import config.strings_en as strings

from PyQt5.QtWidgets import (QLineEdit, QLabel, QGridLayout, 
	QListWidget,QListWidgetItem, QWidget, QPushButton)

class ReferenceCard(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.id = 0

		# Create first tab
		self.lId    = QLabel(str(self.id))
		self.lOrigin  = QLabel(strings.LABLE_ORIGIN) # Authorth
		self.lDate  = QLabel(strings.LABLE_DATE)
		self.lTitle  = QLabel(strings.LABLE_TITLE)
		self.lLink = QLabel(strings.LABLE_LINK)

		self.btnDel = QPushButton(strings.DELETE)
		self.btnDel.setToolTip(strings.TOOLTIP_DELETE_ELEMENT)
		self.btnDel.clicked.connect(self._deleteOnClick)

		self.eOrigin = QLineEdit()
		self.eOrigin.textChanged[str].connect(self._onReferenceOriginChanged)
		self.eDate = QLineEdit()
		self.eDate.textChanged[str].connect(self._onReferenceDateChanged)
		self.eTitle = QLineEdit()
		self.eTitle.textChanged[str].connect(self._onReferenceTitleChanged)
		self.eLink = QLineEdit()
		self.eLink.textChanged[str].connect(self._onReferenceLinkChanged)

		self.grid = QGridLayout()
		self.grid.setSpacing(10)

		self.grid.addWidget(self.lId, 1, 0)
		self.grid.addWidget(self.btnDel, 1, 1)

		self.grid.addWidget(self.lOrigin, 2, 0)
		self.grid.addWidget(self.eOrigin, 2, 1)
		self.grid.addWidget(self.lDate, 3, 0)
		self.grid.addWidget(self.eDate, 3, 1)
		self.grid.addWidget(self.lTitle,  4, 0)
		self.grid.addWidget(self.eTitle,  4, 1)
		self.grid.addWidget(self.lLink, 5, 0)
		self.grid.addWidget(self.eLink, 5, 1)

		self.setLayout(self.grid)

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def _deleteOnClick(self):
		self.presenter.delReferenceFromList(self.id)

	def setPresenter(self, p):
		self.presenter = p
	
	def setId(self, id):
		self.id = id
		self.lId.setText(str(id))
	
	def _onReferenceOriginChanged(self, text):
		self.presenter.onReferenceOriginChanged(self.id-1, text)
	def _onReferenceDateChanged(self, text):
		self.presenter.onReferenceDateChanged(self.id-1, text)
	def _onReferenceTitleChanged(self, text):
		self.presenter.onReferenceTitleChanged(self.id-1, text)
	def _onReferenceLinkChanged(self, text):
		self.presenter.onReferenceLinkChanged(self.id-1, text)





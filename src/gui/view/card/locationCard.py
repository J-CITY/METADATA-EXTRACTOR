import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

import config.strings_en as strings

from PyQt5.QtWidgets import (QLineEdit, QLabel, QGridLayout, 
	QListWidget,QListWidgetItem, QWidget, QPushButton)

class LocationCard(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.id = 0

		# Create first tab
		self.lId    = QLabel(str(self.id))
		self.lName  = QLabel(strings.LABLE_NAME)
		self.lWest  = QLabel(strings.LABLE_WEST)
		self.lEast  = QLabel(strings.LABLE_EAST)
		self.lNorth = QLabel(strings.LABLE_NORTH)
		self.lSouth = QLabel(strings.LABLE_SOUTH)

		self.btnDel = QPushButton(strings.DELETE)
		self.btnDel.setToolTip(strings.TOOLTIP_DELETE_ELEMENT)
		self.btnDel.clicked.connect(self._deleteOnClick)

		self.eName = QLineEdit()
		self.eName.textChanged[str].connect(self._onLocationNameChanged)
		self.eWest = QLineEdit()
		self.eWest.textChanged[str].connect(self._onLoactionWestChanged)
		self.eEast = QLineEdit()
		self.eEast.textChanged[str].connect(self._onLoactionEastChanged)
		self.eNorth = QLineEdit()
		self.eNorth.textChanged[str].connect(self._onLoactionNorthChanged)
		self.eSouth = QLineEdit()
		self.eSouth.textChanged[str].connect(self._onLoactionSouthChanged)

		self.grid = QGridLayout()
		self.grid.setSpacing(10)

		self.grid.addWidget(self.lId, 1, 0)
		self.grid.addWidget(self.btnDel, 1, 1)

		self.grid.addWidget(self.lName, 2, 0)
		self.grid.addWidget(self.eName, 2, 1)
		self.grid.addWidget(self.lWest, 3, 0)
		self.grid.addWidget(self.eWest, 3, 1)
		self.grid.addWidget(self.lEast,  4, 0)
		self.grid.addWidget(self.eEast,  4, 1)
		self.grid.addWidget(self.lNorth, 5, 0)
		self.grid.addWidget(self.eNorth, 5, 1)
		self.grid.addWidget(self.lSouth, 6, 0)
		self.grid.addWidget(self.eSouth, 6, 1)

		self.setLayout(self.grid)

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def _deleteOnClick(self):
		self.presenter.delLocationFromList(self.id)

	def setPresenter(self, p):
		self.presenter = p
	
	def setId(self, id):
		self.id = id
		self.lId.setText(str(id))
	
	def _onLocationNameChanged(self, text):
		self.presenter.onLocationNameChanged(self.id-1, text)
	def _onLoactionWestChanged(self, text):
		self.presenter.onLocationWestChanged(self.id-1, text)
	def _onLoactionEastChanged(self, text):
		self.presenter.onLocationEastChanged(self.id-1, text)
	def _onLoactionNorthChanged(self, text):
		self.presenter.onLocationNorthChanged(self.id-1, text)
	def _onLoactionSouthChanged(self, text):
		self.presenter.onLocationSouthChanged(self.id-1, text)




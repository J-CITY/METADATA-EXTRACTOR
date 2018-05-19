import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

import config.strings_en as strings

from PyQt5.QtWidgets import (QLineEdit, QLabel, QGridLayout, 
	QListWidget,QListWidgetItem, QWidget, QPushButton)

class NameCard(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.id = 0
		self.fileName = ""

		# Create first tab
		self.lId            = QLabel(str(self.id))
		self.lName          = QLabel(strings.LABLE_NAME)
		self.lOrganisation  = QLabel(strings.LABLE_ORGANISATION)
		self.lPhone         = QLabel(strings.LABLE_PHONE)
		self.lFacs          = QLabel(strings.LABLE_FACS)
		self.lDeliveryPoint = QLabel(strings.LABLE_DELIVERY_POINT)
		self.lCity          = QLabel(strings.LABLE_CITY)
		self.lArea          = QLabel(strings.LABLE_AREA)
		self.lPostalCode    = QLabel(strings.LABLE_POSTAL_CODE)
		self.lCountry       = QLabel(strings.LABLE_COUNTRY)
		self.lEmail         = QLabel(strings.LABLE_EMAIL)

		self.btnDel = QPushButton(strings.DELETE)
		self.btnDel.setToolTip(strings.TOOLTIP_DELETE_ELEMENT)
		self.btnDel.clicked.connect(self._deleteOnClick)

		self.eName          = QLineEdit()
		self.eName.textChanged[str].connect(self._onNameChanged)
		self.eOrganisation  = QLineEdit()
		self.eOrganisation.textChanged[str].connect(self._onOrganisationChanged)
		self.ePhone         = QLineEdit()
		self.ePhone.textChanged[str].connect(self._onPhoneChanged)
		self.eFacs          = QLineEdit()
		self.eFacs.textChanged[str].connect(self._onFacsChanged)
		self.eDeliveryPoint = QLineEdit()
		self.eDeliveryPoint.textChanged[str].connect(self._onDeliveryPointChanged)
		self.eCity          = QLineEdit()
		self.eCity.textChanged[str].connect(self._onCityChanged)
		self.eArea          = QLineEdit()
		self.eArea.textChanged[str].connect(self._onAreaChanged)
		self.ePostalCode    = QLineEdit()
		self.ePostalCode.textChanged[str].connect(self._onPostalCodeChanged)
		self.eCountry       = QLineEdit()
		self.eCountry.textChanged[str].connect(self._onCountryChanged)
		self.eEmail         = QLineEdit()
		self.eEmail.textChanged[str].connect(self._onEmailChanged)

		self.grid = QGridLayout()
		self.grid.setSpacing(10)

		self.grid.addWidget(self.lId, 1, 0)
		self.grid.addWidget(self.btnDel, 1, 1)

		self.grid.addWidget(self.lName, 2, 0)
		self.grid.addWidget(self.eName, 2, 1)
		self.grid.addWidget(self.lOrganisation, 3, 0)
		self.grid.addWidget(self.eOrganisation, 3, 1)

		self.grid.addWidget(self.lPhone, 4, 0)
		self.grid.addWidget(self.ePhone, 4, 1)
		self.grid.addWidget(self.lFacs, 5, 0)
		self.grid.addWidget(self.eFacs, 5, 1)
		self.grid.addWidget(self.lDeliveryPoint, 6, 0)
		self.grid.addWidget(self.eDeliveryPoint, 6, 1)
		self.grid.addWidget(self.lCity, 7, 0)
		self.grid.addWidget(self.eCity, 7, 1)
		self.grid.addWidget(self.lArea, 8, 0)
		self.grid.addWidget(self.eArea, 8, 1)
		self.grid.addWidget(self.lPostalCode, 9, 0)
		self.grid.addWidget(self.ePostalCode, 9, 1)
		self.grid.addWidget(self.lCountry, 10, 0)
		self.grid.addWidget(self.eCountry, 10, 1)
		self.grid.addWidget(self.lEmail, 11, 0)
		self.grid.addWidget(self.eEmail, 11, 1)

		self.setLayout(self.grid)

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def _deleteOnClick(self):
		#self.deleteLater()
		self.presenter.delNameFromList(self.id)

	def setPresenter(self, p):
		self.presenter = p
	
	def setId(self, id):
		self.id = id
		self.lId.setText(str(id))
	
	def _onNameChanged(self, text):
		self.presenter.onNameChanged(self.id-1, text)
	def _onOrganisationChanged(self, text):
		self.presenter.onOrganisationChanged(self.id-1, text)
	def _onPhoneChanged(self, text):
		self.presenter.onPhoneChanged(self.id-1, text)
	def _onFacsChanged(self, text):
		self.presenter.onFacsChanged(self.id-1, text)
	def _onDeliveryPointChanged(self, text):
		self.presenter.onDeliveryPointChanged(self.id-1, text)
	def _onCityChanged(self, text):
		self.presenter.onCityChanged(self.id-1, text)
	def _onAreaChanged(self, text):
		self.presenter.onAreaChanged(self.id-1, text)
	def _onPostalCodeChanged(self, text):
		self.presenter.onPostalCodeChanged(self.id-1, text)
	def _onCountryChanged(self, text):
		self.presenter.onCountryChanged(self.id-1, text)
	def _onEmailChanged(self, text):
		self.presenter.onEmailChanged(self.id-1, text)

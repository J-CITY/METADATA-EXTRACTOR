import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

import config.strings_en as strings

from PyQt5.QtWidgets import (QLineEdit, QLabel, QGridLayout, 
	QListWidget,QListWidgetItem, QWidget, QPushButton, QFormLayout)

class ContactCard(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.fileName = ""

		# Create first tab
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

		self.grid = QFormLayout()
		self.grid.setSpacing(10)

		self.grid.addRow(self.lName, self.eName)
		self.grid.addRow(self.lOrganisation, self.eOrganisation)
		self.grid.addRow(self.lPhone, self.ePhone)
		self.grid.addRow(self.lFacs, self.eFacs)
		self.grid.addRow(self.lDeliveryPoint, self.eDeliveryPoint)
		self.grid.addRow(self.lCity, self.eCity)
		self.grid.addRow(self.lArea, self.eArea)
		self.grid.addRow(self.lPostalCode, self.ePostalCode)
		self.grid.addRow(self.lCountry, self.eCountry)
		self.grid.addRow(self.lEmail, self.eEmail)

		#self.grid.addWidget(self.lName, 2, 0)
		#self.grid.addWidget(self.eName, 2, 1)
		#self.grid.addWidget(self.lOrganisation, 3, 0)
		#self.grid.addWidget(self.eOrganisation, 3, 1)
		#self.grid.addWidget(self.lPhone, 4, 0)
		#self.grid.addWidget(self.ePhone, 4, 1)
		#self.grid.addWidget(self.lFacs, 5, 0)
		#self.grid.addWidget(self.eFacs, 5, 1)
		#self.grid.addWidget(self.lDeliveryPoint, 6, 0)
		#self.grid.addWidget(self.eDeliveryPoint, 6, 1)
		#self.grid.addWidget(self.lCity, 7, 0)
		#self.grid.addWidget(self.eCity, 7, 1)
		#self.grid.addWidget(self.lArea, 8, 0)
		#self.grid.addWidget(self.eArea, 8, 1)
		#self.grid.addWidget(self.lPostalCode, 9, 0)
		#self.grid.addWidget(self.ePostalCode, 9, 1)
		#self.grid.addWidget(self.lCountry, 10, 0)
		#self.grid.addWidget(self.eCountry, 10, 1)
		#self.grid.addWidget(self.lEmail, 11, 0)
		#self.grid.addWidget(self.eEmail, 11, 1)

		self.setLayout(self.grid)

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())

	def setPresenter(self, p):
		self.presenter = p
	
	def _onNameChanged(self, text):
		self.presenter.onContactNameChanged(text)
	def _onOrganisationChanged(self, text):
		self.presenter.onContactOrganisationChanged(text)
	def _onPhoneChanged(self, text):
		self.presenter.onContactPhoneChanged(text)
	def _onFacsChanged(self, text):
		self.presenter.onContactFacsChanged(text)
	def _onDeliveryPointChanged(self, text):
		self.presenter.onContactDeliveryPointChanged(text)
	def _onCityChanged(self, text):
		self.presenter.onContactCityChanged(text)
	def _onAreaChanged(self, text):
		self.presenter.onContactAreaChanged(text)
	def _onPostalCodeChanged(self, text):
		self.presenter.onContactPostalCodeChanged(text)
	def _onCountryChanged(self, text):
		self.presenter.onContactCountryChanged(text)
	def _onEmailChanged(self, text):
		self.presenter.onContactEmailChanged(text)

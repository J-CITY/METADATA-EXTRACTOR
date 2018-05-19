import os, sys
parentPath = os.path.abspath("../../../")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

import config.strings_en as strings

from PyQt5.QtWidgets import (QLineEdit, QLabel, QGridLayout, 
	QListWidget,QListWidgetItem, QWidget, QPushButton, QFormLayout)

class InfoCard(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		# Create first tab
		self.lTitle          = QLabel(strings.LABLE_TITLE)
		self.lOrigin          = QLabel(strings.LABLE_ORIGIN)
		self.lDateBegin  = QLabel(strings.LABLE_DATE_BEGIN)
		self.lDateEnd         = QLabel(strings.LABLE_DATE_END)
		self.lDescriptAbstract          = QLabel(strings.LABLE_DESCRIPT_ABSTRACT)
		self.lDescriptPurpose = QLabel(strings.LABLE_DESCRIPT_PURPOSE)
		self.lDescriptSupplemental          = QLabel(strings.LABLE_DESCRIPT_SUPPLEMENTAL)
		self.lStatusProgress          = QLabel(strings.LABLE_STATUS_PROGRESS)
		self.lStatusUpdate    = QLabel(strings.LABLE_POSTAL_STATUS_UPDATE)
		self.lAccess       = QLabel(strings.LABLE_ACCESS)


		self.eOrigin          = QLineEdit()
		self.eOrigin.textChanged[str].connect(self._onOriginChanged)
		self.eTitle          = QLineEdit()
		self.eTitle.textChanged[str].connect(self._onTitleChanged)
		self.eDateBegin  = QLineEdit()
		self.eDateBegin.textChanged[str].connect(self._onDateBeginChanged)
		self.eDateEnd         = QLineEdit()
		self.eDateEnd.textChanged[str].connect(self._onDateEndChanged)
		self.eDescriptAbstract          = QLineEdit()
		self.eDescriptAbstract.textChanged[str].connect(self._onDescriptAbstractChanged)
		self.eDescriptPurpose = QLineEdit()
		self.eDescriptPurpose.textChanged[str].connect(self._onDescriptPurposeChanged)
		self.eDescriptSupplemental          = QLineEdit()
		self.eDescriptSupplemental.textChanged[str].connect(self._onDescriptSupplementalChanged)
		self.eStatusProgress          = QLineEdit()
		self.eStatusProgress.textChanged[str].connect(self._onStatusProgressChanged)
		self.eStatusUpdate    = QLineEdit()
		self.eStatusUpdate.textChanged[str].connect(self._onStatusUpdateChanged)
		self.eAccess       = QLineEdit()
		self.eAccess.textChanged[str].connect(self._onAccessChanged)

		self.grid = QFormLayout()
		self.grid.setSpacing(10)

		self.grid.addRow(self.lOrigin, self.eOrigin)
		self.grid.addRow(self.lTitle, self.eTitle)
		self.grid.addRow(self.lDateBegin, self.eDateBegin)
		self.grid.addRow(self.lDateEnd, self.eDateEnd)
		self.grid.addRow(self.lDescriptAbstract, self.eDescriptAbstract)
		self.grid.addRow(self.lDescriptSupplemental, self.eDescriptSupplemental)
		self.grid.addRow(self.lDescriptPurpose, self.eDescriptPurpose)
		self.grid.addRow(self.lAccess, self.eAccess)

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
	
	def _onOriginChanged(self, text):
		self.presenter.onInfoOriginChanged(text)
	def _onTitleChanged(self, text):
		self.presenter.onInfoTitleChanged(text)
	def _onDateBeginChanged(self, text):
		self.presenter.onInfoDateBeginChanged(text)
	def _onDateEndChanged(self, text):
		self.presenter.onInfoDateEndChanged(text)
	def _onDescriptAbstractChanged(self, text):
		self.presenter.onInfoDescriptAbstractChanged(text)
	def _onDescriptPurposeChanged(self, text):
		self.presenter.onInfoDescriptPurposeChanged(text)
	def _onDescriptSupplementalChanged(self, text):
		self.presenter.onInfoDescriptSupplementalChanged(text)
	def _onStatusProgressChanged(self, text):
		self.presenter.onInfoStatusProgressChanged(text)
	def _onStatusUpdateChanged(self, text):
		self.presenter.onTitleStatusUpdateChanged(text)
	def _onAccessChanged(self, text):
		self.presenter.onInfoAccessChanged(text)

	def addData(self, title, dBegin, dEnd):
		self.eTitle.setText(title)	
		self.eDateBegin.setText(dBegin)	
		self.eDateEnd.setText(dEnd)	

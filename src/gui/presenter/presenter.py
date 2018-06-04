from PyQt5.QtCore import Qt, QThread,pyqtSignal, QObject
import threading
import os

class Worker(QObject):
	setProgress = pyqtSignal([int])
	finished = pyqtSignal()
	finishedErr = pyqtSignal([str])

	def __init__(self, model):
		super(Worker, self).__init__()
		self.model = model

	def run(self):
		if self.model.INFilename != "":
			from converter.pdfextractor import PDFContainer
			import nltk.data
			from model.title import extractTitle
			from converter.pdfextractor import PDFContainer
			from model.location import Location
			from config.dictionary import refWords, Coves, Seas, Bays, Islands
			from model.keywords import KeywordExtractor
			from model.reference import ExtracrReference
			from model.ner import NERExtractor
			from converter.dataContainer import DataPerson, DataLocation, DataKeyword, DataRef
			from converter.load import insertData
			#self.model.extract()

			self.setProgress.emit(0)
			#view.isVisibleProgress(True)
			filename, file_extension = os.path.splitext(self.model.INFilename)
			if file_extension.lower() != '.pdf':
				self.finishedErr.emit("File is not PDF")
				return
			self.model.pdf = PDFContainer(format=self.model.config.outPDFFormat, codec=self.model.config.fileCodec)
			if self.model.pdf.format == "filter":
				testExist = self.model.pdf.convertPDFFilter(self.model.INFilename)
			else:
				testExist = self.model.pdf.convertPDFAlternative(self.model.INFilename)
			if not testExist:
				self.finishedErr.emit("No such file")
				return
			
			self.setProgress.emit(10)
			self.model.tokenizer = nltk.data.load(self.model.config.sentencesSplitterModel)
			self.setProgress.emit(20)
			self.model.extractorNer = NERExtractor(self.model.config)
			self.setProgress.emit(30)
			self.model.extractorLoc = Location(self.model.config.minTanimoto)
			self.setProgress.emit(40)
			# extract title
			txt = self.model.pdf.getPages(0, 3)
			self.model.extractTitle(txt)
			self.setProgress.emit(50)
			# extract names
			txt = self.model.pdf.getPages(0, 10)
			sents = txt.split('\n') # tokenizer.tokenize(txt)
			self.model.extractName(sents)
			self.setProgress.emit(60)
			# extract locations with coords	
			txt = self.model.pdf.getAllPages()
			sents = self.model.tokenizer.tokenize(txt)
			self.model.extractLocation(sents)
			self.setProgress.emit(70)
			# extract key words
			self.model.extractKeyWords(txt)
			self.setProgress.emit(80)
			# extract refs
			self.model.extractRefs(txt)
			self.setProgress.emit(100)
			
			self.finished.emit()

class Presenter:
	def __init__(self, view, model):
		self.view = view
		self.model = model
		self.model.typeOut = "txt"
		self.model.metaTitle = True
		self.model.metaContent = True
		self.model.metaName = True
		self.model.metaLocation = True
		self.model.metaKeyWord = True
		self.model.metaRef = True
		self.model.metaAll = True

	def extractOcClick(self):
		self.view.isVisibleProgress(True)
		self.workerThread = QThread()
		self.workerObject = Worker(self.model)
		self.workerObject.moveToThread(self.workerThread)
		self.workerThread.started.connect(self.workerObject.run)
		self.workerObject.setProgress.connect(self.setProgress)
		self.workerObject.finished.connect(self.updateGUI)
		self.workerObject.finishedErr.connect(self.updateErr)
		self.workerThread.start()

	def extract(self):
		if self.model.INFilename != "":
			from converter.pdfextractor import PDFContainer
			import nltk.data
			from model.title import extractTitle
			from converter.pdfextractor import PDFContainer
			from model.location import Location
			from config.dictionary import refWords, Coves, Seas, Bays, Islands
			from model.keywords import KeywordExtractor
			from model.reference import ExtracrReference
			from model.ner import NERExtractor
			from converter.dataContainer import DataPerson, DataLocation, DataKeyword, DataRef
			from converter.load import insertData
			#self.model.extract()

			self.view.setProgress(0)
			self.view.isVisibleProgress(True)

			self.model.pdf = PDFContainer(format=self.model.config.outPDFFormat, codec=self.model.config.fileCodec)
			if self.model.pdf.format == "filter":
				self.model.pdf.convertPDFFilter(self.model.INFilename)
			else:
				self.model.pdf.convertPDFAlternative(self.model.INFilename)
			self.view.setProgress(10)
			self.model.tokenizer = nltk.data.load(self.model.config.sentencesSplitterModel)
			self.view.setProgress(20)
			self.model.extractorNer = NERExtractor(self.model.config)
			self.view.setProgress(30)
			self.model.extractorLoc = Location(self.model.config.minTanimoto)
			self.view.setProgress(40)
			# extract title
			txt = self.model.pdf.getPages(0, 3)
			self.model.extractTitle(txt)
			self.view.setProgress(50)
			# extract names
			txt = self.model.pdf.getPages(0, 10)
			sents = txt.split('\n') # tokenizer.tokenize(txt)
			self.model.extractName(sents)
			self.view.setProgress(60)
			# extract locations with coords	
			txt = self.model.pdf.getAllPages()
			sents = self.model.tokenizer.tokenize(txt)
			self.model.extractLocation(sents)
			self.view.setProgress(70)
			# extract key words
			self.model.extractKeyWords(txt)
			self.view.setProgress(80)
			# extract refs
			self.model.extractRefs(txt)
			self.view.setProgress(90)
			#############################
			self.view.setProgress(100)
			#self.view.isVisibleProgress(False)
	
	def updateGUI(self):
		self.view.setUUID(self.model.uuid)
		self.view.setNamesData(self.model.namesData)
		self.view.setKeywordsData(self.model.keywordsData, self.model.keywordsLocData)
		self.view.setLocationsData(self.model.locationsData)
		self.view.setReferencesData(self.model.refs)
		self.view.setInfoData(self.model.title, self.model.dateBegin, self.model.dateEnd)
		self.view.isVisibleProgress(False)
		self.workerThread.quit()
	
	def updateErr(self, err):
		self.view.isVisibleProgress(False)
		self.workerThread.quit()
		self.view.statusErr(err)

	def setProgress(self, p):
		self.view.setProgress(p)
	def isVisibleProgress(self, isV):
		self.view.isVisibleProgress(isV)

	def openFileOnClick(self, fileName):
		self.model.INFilename = fileName
		print("Model IN file "+self.model.INFilename)

	def saveFileOnClick(self, fileName):
		self.model.OUTFilename = fileName
		print("Model OUT file "+self.model.OUTFilename)
		self.model.save()

	def loadOcClick(self):
		code = self.model.load()
		self.view.statusErr("Load: " + str(code))
	
	def loadFileOcClick(self, infile):
		code = self.model.loadFromFile(infile)
		self.view.statusErr("Load: " + str(code))

	def checkTitleOnClick(self, state):
		if state == Qt.Checked:
			self.model.metaTitle = True
		else:
			self.model.metaTitle = False
	def checkContentOnClick(self, state):
		if state == Qt.Checked:
			self.model.metaContent = True
		else:
			self.model.metaContent = False
	def checkNameOnClick(self, state):
		if state == Qt.Checked:
			self.model.metaName = True
		else:
			self.model.metaName = False
	def checkLocationOnClick(self, state):
		if state == Qt.Checked:
			self.model.metaLocation = True
		else:
			self.model.metaLocation = False
	def checkKeywordOnClick(self, state):
		if state == Qt.Checked:
			self.model.metaKeyword = True
		else:
			self.model.metaKeyword = False
	def checkRefOnClick(self, state):
		if state == Qt.Checked:
			self.model.metaRef = True
		else:
			self.model.metaRef = False
	def setTypeOnClick(self, state):
		self.model.typeOut = state
	#if args.output_file != "":
	#	extractor.OUTFilename = args.output_file
	#extractor.typeOut = args.type
	def delNameFromList(self, id):
		self.view.mainWidget.tabControlPerson.delName(id)
		self.model.delName(id)

	def addName(self):
		self.model.addName()
	# name card
	def onNameChanged(self, id, text):
		self.model.namesData[id].name = text
	def onOrganisationChanged(self, id, text):
		self.model.namesData[id].organisation = text
	def onPhoneChanged(self, id, text):
		self.model.namesData[id].phone = text
	def onFacsChanged(self, id, text):
		self.model.namesData[id].facs = text
	def onDeliveryPointChanged(self, id, text):
		self.model.namesData[id].deliveryPoint = text
	def onCityChanged(self, id, text):
		self.model.namesData[id].city = text
	def onAreaChanged(self, id, text):
		self.model.namesData[id].area = text
	def onPostalCodeChanged(self, id, text):
		self.model.namesData[id].postalCode = text
	def onCountryChanged(self, id, text):
		self.model.namesData[id].country = text
	def onEmailChanged(self, id, text):
		self.model.namesData[id].email = text

	# keyword card
	def onKeywordNameChanged(self, id, text, _type):
		if _type == "keyword":
			self.model.keywordsData[id].keyword = text
		elif _type == "location":
			self.model.keywordsLocData[id].keyword = text
	def onKeywordTypeChanged(self, id, text, _type):
		if _type == "keyword":
			self.model.keywordsData[id].type = text
		elif _type == "location":
			self.model.keywordsLocData[id].type = text

	# keyword tab
	def addKeyword(self):
		self.model.addKeyword()
	def addKeywordLocation(self):
		self.model.addKeywordLoc()
	
	def delKeywordFromList(self, id):
		self.view.mainWidget.tabControlKeyword.delKeyword(id)
		self.model.delKeyword(id)
	def delKeywordLocFromList(self, id):
		self.view.mainWidget.tabControlKeyword.delKeywordLoc(id)
		self.model.delKeywordLoc(id)

	# location card
	def onLocationNameChanged(self, id, text):
		self.model.locationsData[id].name = text

	def onLocationWestChanged(self, id, text):
		self.model.locationsData[id].west = text
	def onLocationEastChanged(self, id, text):
		self.model.locationsData[id].east = text
	def onLocationNorthChanged(self, id, text):
		self.model.locationsData[id].north = text
	def onLocationSouthChanged(self, id, text):
		self.model.locationsData[id].south = text

	# location tab
	def addLocation(self):
		self.model.addLocation()
	
	def delLocationFromList(self, id):
		self.view.mainWidget.tabControlLocation.delLocation(id)
		self.model.delLocation(id)


	# reference card
	def onReferenceOriginChanged(self, id, text):
		self.model.refs[id].origin = text
	def onReferenceDateChanged(self, id, text):
		self.model.refs[id].date = text
	def onReferenceTitleChanged(self, id, text):
		self.model.refs[id].title = text
	def onReferenceLinkChanged(self, id, text):
		self.model.refs[id].link = text

	# reference tab
	def addReference(self):
		self.model.addReference()
	
	def delReferenceFromList(self, id):
		self.view.mainWidget.tabControlReference.delReference(id)
		self.model.delReference(id)

	# contact card
	def onContactNameChanged(self, text):
		self.model.contact.name = text
	def onContactOrganisationChanged(self, text):
		self.model.contact.organisation = text
	def onContactPhoneChanged(self, text):
		self.model.contact.phone = text
	def onContactFacsChanged(self, text):
		self.model.contact.facs = text
	def onContactDeliveryPointChanged(self, text):
		self.model.contact.deliveryPoint = text
	def onContactCityChanged(self, text):
		self.model.contact.city = text
	def onContactAreaChanged(self, text):
		self.model.contact.area = text
	def onContactPostalCodeChanged(self, text):
		self.model.contact.postalCode = text
	def onContactCountryChanged(self, text):
		self.model.contact.country = text
	def onContactEmailChanged(self, text):
		self.model.contact.email = text

	# info card
	def onInfoOriginChanged(self, text):
		self.model.origin = text
	def onInfoTitleChanged(self, text):
		self.model.title = text
	def onInfoDateBeginChanged(self, text):
		self.model.dateBegin = text
	def onInfoDateEndChanged(self, text):
		self.model.deteEnd = text
	def onInfoDescriptAbstractChanged(self, text):
		self.model.descriptAbstract = text
	def onInfoDescriptPurposeChanged(self, text):
		self.model.descriptPurpose = text
	def onInfoDescriptSupplementalChanged(self, text):
		self.model.descriptSupplemental = text
	def onInfoStatusProgressChanged(self, text):
		self.model.statusBegin = text
	def onTitleStatusUpdateChanged(self, text):
		self.model.statusEnd = text
	def onInfoAccessChanged(self, text):
		self.model.access = text
	def onInfoUUIDChanged(self, text):
		self.model.uuid = text
	def _checkUUIDOnClick(self, state):
		if state == Qt.Checked:
			self.model.genUUID = True
		else:
			self.model.genUUID  = False

	# settings
	def getPrefs(self):
		return self.model.config.getPreferences()
	
	def updateSettings(self, section, par, val):
		#print(section.encode(), par.encode(), val.encode())
		self.model.config.updatePreferences(section, par, val)



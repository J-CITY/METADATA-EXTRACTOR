import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

from model.title import extractTitle
from converter.pdfextractor import PDFContainer
from model.location import Location
from config.dictionary import refWords, Coves, Seas, Bays, Islands
from model.keywords import KeywordExtractor
from model.reference import ExtracrReference
from model.ner import NERExtractor
from converter.dataContainer import DataPerson, DataLocation, DataKeyword, DataRef
from converter.load import insertData

import datetime
import string
import random
import nltk.data
import codecs
import re

class Extractor:
	def __init__(self, config):
		self.metaTitle = False
		self.metaContent = False
		self.metaName = False
		self.metaLocation = False
		self.metaKeyWord = False
		self.metaRef = False
		self.metaAll = False
		self.config = config
		self.INFilename = 'in.pdf'
		self.OUTFilename = 'out.txt'

		self.title = ''
		
		self.origin = ''

		self.descriptAbstract = ''
		self.descriptPurpose = ''
		self.descriptSupplemental = ''

		self.dateBegin = ''
		self.dateEnd = ''

		self.statusProgress = ''
		self.statusUpdate = ''

		self.access = ''
		
		#self.names = set()
		#self.locations = set()
		#self.keys = []
		self.typeOut = "txt"
		self.refs = []

		self.contact = DataPerson("")
		self.namesData = []
		self.keywordsData = []
		self.keywordsLocData = []
		self.locationsData = []

		self.contact = DataPerson('')
	
	def reinit():
		self.namesData = []
		self.keywordsData = []
		self.locationsData = []

	def addName(self):
		self.namesData.append(DataPerson(''))
	def addKeyword(self):
		self.keywordsData.append(DataKeyword(''))
	def addKeywordLoc(self):
		self.keywordsLocData.append(DataKeyword(''))
	def addLocation(self):
		self.locationsData.append(DataLocation(''))
	def addReference(self):
		self.refs.append(DataRef(''))

	def delName(self, id):
		self.namesData[id-1:id] = []
	def delKeyword(self, id):
		self.keywordsData[id-1:id] = []
	def delKeywordLoc(self, id):
		self.keywordsLocData[id-1:id] = []
	def delLocation(self, id):
		self.locationsData[id-1:id] = []
	def delReference(self, id):
		self.locationsData[id-1:id] = []

	def extract(self):
		self.pdf = PDFContainer(format=self.config.outPDFFormat, codec=self.config.fileCodec)
		if self.pdf.format == "filter":
			self.pdf.convertPDFFilter(self.INFilename)
		else:
			self.pdf.convertPDFAlternative(self.INFilename)

		self.tokenizer = nltk.data.load(self.config.sentencesSplitterModel)
		
		self.extractorNer = NERExtractor(self.config)
		
		self.extractorLoc = Location(self.config.minTanimoto)

		# extract title
		txt = self.pdf.getPages(0, 3)
		self.extractTitle(txt)

		# extract names
		txt = self.pdf.getPages(0, 10)
		sents = txt.split('\n') # tokenizer.tokenize(txt)
		self.extractName(sents)

		# extract locations with coords	
		txt = self.pdf.getAllPages()
		sents = self.tokenizer.tokenize(txt)
		self.extractLocation(sents)

		# extract key words
		self.extractKeyWords(txt)

		# extract refs
		self.extractRefs(txt)

	def save(self):
		print(self.typeOut)
		if self.typeOut == 'txt':
			text = self.saveToTXT()
			self.saveFile(self.OUTFilename, text)
		elif self.typeOut == 'iso19115v2':
			text = self.saveToISO19115v2()
			self.saveFile(self.OUTFilename, text)
		elif self.typeOut == 'fgdc':
			text = self.saveToFGDC()
			self.saveFile(self.OUTFilename, text)
		elif self.typeOut == 'dublin':
			self.saveToDublin()
		
	def load(self):
		print(self.typeOut)
		if self.typeOut == 'iso19115v2':
			text = self.saveToISO19115v2()
			insertData(self.config.protocol, self.config.url, self.config.user, self.config.passwd, text)
		elif self.typeOut == 'fgdc':
			text = self.saveToFGDC()
			insertData(self.config.protocol, self.config.url, self.config.user, self.config.passwd, text)

	def extractRefs(self, txt):
		extr = ExtracrReference(txt)
		_refs = extr.extract()
		for r in _refs:
			self.refs.append(DataRef(r))

	def extractTitle(self, txt):
		self.title = extractTitle(txt)
		_d = re.search(r'[0-9]{4}', self.title)
		if _d is None:
			_date = ""
		else:
			_date = _d.group(0)
		self.dateBegin = _date
		self.dateEnd = "present"

	def extractName(self, sentences):
		#STXTfile = codecs.open("namesOUTNAME.txt", "w", "utf-8")
		names = set()
		for sentence in sentences:
			wordsRaw, preds = self.extractorNer.extractFromSentence(sentence)
			test = False
			res = ''
			for i, w in enumerate(wordsRaw):
				#STXTfile.write(w + ' - ' + preds[i] + '\n')
				if preds[i] == "I-PER":
					#if i > 0 and (preds[i-1] == "I-LOC" or preds[i-1] == "B-LOC" or preds[i-1] == "I-ORG" or preds[i-1] == "B-ORG"):
					#	res += wordsRaw[i-1] + ' '
					res += w + ' '
					continue
				else:
					if res != '':
						res = res.strip()
						ress = res.split(',')
						for r in ress:
							r = r.strip()
							if len(r.split(' ')) > 1:
								names.add(r.strip())
						res = ""
			if res != '':
				res = res.strip()
				ress = res.split(',')
				for r in ress:
					r = r.strip()
					if len(r.split(' ')) > 1:
						names.add(r.strip())
		#STXTfile.close()
		for s in names:
			self.namesData.append(DataPerson(s))

	def extractLocation(self, sents):
		locmap = {}
		locmap.update(Coves)
		locmap.update(Seas)
		locmap.update(Bays)
		locmap.update(Islands)

		candidates = []

		for s in sents:
			ls = s.lower()
			for w in refWords:
				if ls.find(w) != -1:
					candidates.append(s)
					break
		locations = set()
		for sentence in candidates:
			wordsRaw, preds = self.extractorNer.extractFromSentence(sentence)
			res = ""
			for i, w in enumerate(wordsRaw):
				if preds[i] == "I-LOC" or preds[i] == "B-LOC":
					res += w + ' '# + ' {' + preds[i] + '} '
					continue
				else:
					if w == 'of' and res != '':
						res += w + ' '
						continue
				res = res.strip()
				if res != '':
					# get coords Coves, Seas, Bays, Islands
					for key in locmap:
						if self.extractorLoc.isFuzzyEqual(res, key, 3):
							r = key + '-' + ''.join(str(x)+'-' for x in locmap[key]) + '\n'
							locations.add(r)
							break
					res = ''
		for s in locations:
			self.locationsData.append(DataLocation(s))
		for s in locations:
			kw = s.split('-')[0]
			self.keywordsLocData.append(DataKeyword(kw))

	def extractKeyWords(self, txt):
		stopwords = []
		with open(self.config.stopWords, encoding=self.config.fileCodec) as f:
			for line in f:
				stopwords.append(line[:len(line)-1])


		ke = KeywordExtractor(stopwords=stopwords, punctuations=self.config.punctuations)
		ke.extractKeyWords(txt)
		ans = ke.getRankedPhrases()

		keys = []
		#STXTfile = codecs.open("regex.txt", "w", "utf-8")
		for w in ans:
			if len(keys) >= self.config.countKeyPhrases:
				break
			if len(w.split()) > self.config.maxKeyPhraseLength or len(w) < 4:
					continue
			if re.search('[\[\]\+\*]', w, re.IGNORECASE|re.UNICODE):
				continue
			_w = re.search(w, txt, re.IGNORECASE|re.UNICODE)
			if _w:
				keys.append(_w.group(0))
		#STXTfile.close()
		for k in keys:
			self.keywordsData.append(DataKeyword(k))

	def genIdentifier(self):
		res = ''
		for i in range(0, 8):
			res += random.choice(string.ascii_letters+"0123456789")
		res += "-"
		for i in range(0, 4):
			res += random.choice(string.ascii_letters+"0123456789")
		res += "-"
		for i in range(0, 4):
			res += random.choice(string.ascii_letters+"0123456789")
		res += "-"
		for i in range(0, 4):
			res += random.choice(string.ascii_letters+"0123456789")
		res += "-"
		for i in range(0, 12):
			res += random.choice(string.ascii_letters+"0123456789")
		return res

	def saveToISO19115v2(self):
		print(self.OUTFilename+' - OUT_FILE')

		year = datetime.date.today().year
		month = datetime.date.today().month
		day = datetime.date.today().day

		#<gmi:MI_Metadata xmlns:gmi="http://www.isotc211.org/2005/gmi" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gsr="http://www.isotc211.org/2005/gsr" xmlns:gss="http://www.isotc211.org/2005/gss" xmlns:gst="http://www.isotc211.org/2005/gst" xmlns:gmx="http://www.isotc211.org/2005/gmx" xmlns:gfc="http://www.isotc211.org/2005/gfc" xmlns:srv="http://www.isotc211.org/2005/srv" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.isotc211.org/2005/gmi ftp://ftp.ncddc.noaa.gov/pub/Metadata/Online_ISO_Training/Intro_to_ISO/schemas/ISObio/schema.xsd">
		res = """
		<gmd:MD_Metadata xmlns:gmd="http://www.isotc211.org/2005/gmd"
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			xmlns:gco="http://www.isotc211.org/2005/gco"
			xmlns:gml="http://www.opengis.net/gml"
			xsi:schemaLocation="http://www.isotc211.org/2005/gmd ../schema.xsd">
		<fileIdentifier>
			<gco:CharacterString>"""+self.genIdentifier()+"""</gco:CharacterString>
		</fileIdentifier>
		<gmd:language>
			<gco:CharacterString>eng</gco:CharacterString>
		</gmd:language>
		<gmd:characterSet>
			<gmd:MD_CharacterSetCode codeListValue="utf8"
				codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#MD_CharacterSetCode"/>
		</gmd:characterSet>

		<gmd:hierarchyLevel>
			gmd:<MD_ScopeCode codeList="http://www.isotc211.org/2005/resources/codeList.xml#MD_ScopeCode"
				codeListValue="dataset"/>
		</gmd:hierarchyLevel>
		<gmd:hierarchyLevelName>
			<gco:CharacterString>dataset</gco:CharacterString>
		</gmd:hierarchyLevelName>

		<gmd:dateStamp>
			<gco:DateTime>""" + str(year) + '-'+ str(month) + '-' + str(day) + """</gco:DateTime>
		</gmd:dateStamp>

		<gmd:metadataStandardName>
			<gco:CharacterString>ISO 19115:2003/19139</gco:CharacterString>
		</gmd:metadataStandardName>
		<gmd:metadataStandardVersion>
			<gco:CharacterString>1.0</gco:CharacterString>
		</gmd:metadataStandardVersion>

		
		"""

		#res += """
		#<gmd:abstract>
		#	<gco:CharacterString>""" + self.descriptAbstract + """</gco:CharacterString>
		#</gmd:abstract>
		#"""

		# Contact
		res += "<gmd:contact>"
		res += self.contact.genISO115v2()
		res += "</gmd:contact>"
		

		if self.metaTitle or self.metaAll:
			_date = re.search(r'[0-9]{4}', self.title).group(0)
			if _date is None:
				_date = ""
			_title = self.title.replace('\n', ' ')
			res += """
		<gmd:identificationInfo>
			<gmd:MD_DataIdentification>
				<gmd:citation>
					<gmd:CI_Citation>
						<gmd:title>
							<gco:CharacterString>""" + _title + """</gco:CharacterString>
						</gmd:title>
						<gmd:date>
							<gmd:CI_Date>
								<gmd:date>
									<gco:DateTime>""" + _date + """</gco:DateTime>
								</gmd:date>
							</gmd:CI_Date>
						</gmd:date>
					</gmd:CI_Citation>
				</gmd:citation>
			</gmd:MD_DataIdentification>
		"""
		res += """
		<abstract>
			<gco:CharacterString>"""+self.descriptAbstract+"""</gco:CharacterString>
		</abstract>
		<purpose>
			<gco:CharacterString>"""+self.descriptPurpose+"""</gco:CharacterString>
		</purpose>
		<status>
			<MD_ProgressCode
				codeList="http://www.isotc211.org/2005/resources/codeList.xml#MD_ProgressCode"
				codeListValue="""+'"'+self.statusProgress+'"'+"""/>
		</status>
		"""
		#if self.metaContent or self.metaAll:
		#	STXTfile.write('CONTENT\n')
		#	for t in self.pdf.getTitles():
		#		STXTfile.write(t+'\n')
		if self.metaName or self.metaAll:
			res += "<gmd:pointOfContact>"
			for s in self.namesData:
				res += s.genISO115v2()
			res += "</gmd:pointOfContact>"
		if self.metaLocation or self.metaAll:
			res += """
		<gmd:extent>
			<gmd:EX_Extent>
				<gmd:description>
					<gco:CharacterString>Spatial extent for locations</gco:CharacterString>
				</gmd:description>
		"""
			for s in self.locationsData:
				res += s.genISO115v2()
			res += """
			</gmd:EX_Extent>
		</gmd:extent>
		"""
		if self.metaKeyWord or self.metaAll:

			kwTypes = {}
			locTypes = {}

			for s in self.keywordsData:
				if s.type in kwTypes:
					if s.keyword != "":
						kwTypes[s.type].append(s)
				else:
					if s.keyword != "":
						kwTypes[s.type] = []
						kwTypes[s.type].append(s)
			
			for s in self.keywordsLocData:
				if s.type in locTypes:
					if s.keyword != "":
						locTypes[s.type].append(s)
				else:
					if s.keyword != "":
						locTypes[s.type] = []
						locTypes[s.type].append(s)
			res += """
			<gmd:descriptiveKeywords>
			"""
			for key in kwTypes.keys():
				res += "<gmd:MD_Keywords>\n"
				#res += "<themekt>" + key + "</themekt>\n"
				for val in kwTypes[key]:
					res += val.genISO115v2()
				res += """
				<type>
					<MD_KeywordTypeCode
						codeList="http://metadata.dgiwg.org/codelistRegistry?MD_KeywordTypeCode"
						codeListValue="""+'"'+ key +'"'+"""/>
				</type>
				"""
				res += "</gmd:MD_Keywords>\n"

			for key in locTypes.keys():
				res += "<gmd:MD_Keywords>\n"
				#res += "<themekt>" + key + "</themekt>\n"
				for val in locTypes[key]:
					res += val.genISO115v2()
				res += """
				<type>
					<MD_KeywordTypeCode
						codeList="http://metadata.dgiwg.org/codelistRegistry?MD_KeywordTypeCode"
						codeListValue="""+'"'+ key +'"'+"""/>
				</type>
				"""
				res += "</gmd:MD_Keywords>\n"


			#for s in self.keywordsData:
			#	res += s.genISO115v2()
			#for s in self.keywordsLocData:
			#	res += s.genISO115v2()
			res += """
			</gmd:descriptiveKeywords>
			"""
		#if self.metaRef or self.metaAll:
		#	res += "<gmd:citation>\n"
		#	for s in self.refs:
		#		res += s.genISO115v2()
		#	res += "</gmd:citation>\n"

		res += "</gmd:identificationInfo>\n</gmd:MD_Metadata>\n"

		#STXTfile = codecs.open(self.OUTFilename, "w", self.config.fileCodec)
		#STXTfile.write(res)
		#STXTfile.close()
		return res
		#self.saveFile(self.OUTFilename, res)

	def saveFile(self, fname, text):
		STXTfile = codecs.open(fname, "w", self.config.fileCodec)
		STXTfile.write(text)
		STXTfile.close()

	def saveToTXT(self):
		print(self.OUTFilename+' - OUT_FILE')
		res = ""
		if self.metaTitle or self.metaAll:
			res += 'TITLE\n'
			res += self.title+'\n'
		if self.metaContent or self.metaAll:
			res += 'CONTENT\n'
			for t in self.pdf.getTitles():
				res += t+'\n'
		if self.metaName or self.metaAll:
			res += 'NAMES\n'
			for s in self.namesData:
				res += s.genText()+'\n'
		if self.metaLocation or self.metaAll:
			res += 'LOCATIONS\n'
			for s in self.locationsData:
				res += s.genText()+'\n'
		if self.metaKeyWord or self.metaAll:
			res += 'KEY WORDS\n'
			i = 0
			for s in self.keywordsData:
				kp = s.genText()
				if i >= self.config.countKeyPhrases:
					break
				if len(kp.split()) > self.config.maxKeyPhraseLength or len(kp) < 4:
					continue
				res += kp+'\n'
				i += 1
			for s in self.keywordsLocData:
				kp = s.genText()
				res += kp+'\n'
		if self.metaRef or self.metaAll:
			res += 'REFS\n'
			for s in self.refs:
				res += s.genText()+'\n'

		#self.saveFile(self.OUTFilename, res)
		return res

	def saveToFGDC(self):
		print(self.OUTFilename+' - OUT_FILE')
		#STXTfile = codecs.open(self.OUTFilename, "w", self.config.fileCodec)

		year = datetime.date.today().year
		month = datetime.date.today().month
		day = datetime.date.today().day

		res = """
		<?xml version="1.0" encoding="UTF-8"?>
		<metadata xmlns:geonet="http://www.fao.org/geonetwork" xmlns:csw="http://www.opengis.net/cat/csw/2.0.2">
			<idinfo>\n"""

		#if self.metaRef or self.metaAll:
		#	res += "<citation>\n"
		#	for s in self.refs:
		#		res += s.genFGDC()
		#	res += "</citation>\n"
		res += "<citation>\n"
		_title = self.title.replace('\n', ' ')
		res += """
		<citeinfo>
			<origin>"""+self.origin+"""</origin>
			<pubdate>"""+self.dateBegin+"""</pubdate>
			<title>""" + _title + """</title>
			<onlink></onlink>
		</citeinfo>\n"""
		res += "</citation>\n"

		if self.metaTitle or self.metaAll:
			
			res += """
				<descript>
					<abstract>"""+self.descriptAbstract+"""</abstract>
					<purpose>"""+self.descriptPurpose+"""</purpose>
					<supplinf>"""+self.descriptSupplemental+"""</supplinf>
				</descript>
		"""

		## NEED UPDATE
		res += """
			<timeperd>
				<timeinfo>
					<rngdates>
						<begdate>""" + self.dateBegin + """</begdate>
						<enddate>""" + self.dateEnd + """</enddate>
					</rngdates>
				</timeinfo>
				<current>ground condition</current>
			</timeperd>
			<status>
				<progress>""" + self.statusProgress + """</progress>
				<update>""" + self.statusUpdate + """</update>
			</status>
			<accconst>""" + self.access + """</accconst>
			<useconst>
				Data not completely processed; some data experimental.
			</useconst>
		"""

		#if self.metaContent or self.metaAll:
		#	STXTfile.write('CONTENT\n')
		#	for t in self.pdf.getTitles():
		#		STXTfile.write(t+'\n')
		if self.metaLocation or self.metaAll:
			res += """
			<spdom>
			"""
			for s in self.locationsData:
				res += s.genFGDC()
			res += """
			</spdom>
			"""
		if self.metaKeyWord or self.metaAll:
			res += """
			<keywords>
			"""

			kwTypes = {}
			locTypes = {}

			for s in self.keywordsData:
				if s.type in kwTypes:
					if s.keyword != "":
						kwTypes[s.type].append(s)
				else:
					if s.keyword != "":
						kwTypes[s.type] = []
						kwTypes[s.type].append(s)
			
			for s in self.keywordsLocData:
				if s.type in locTypes:
					if s.keyword != "":
						locTypes[s.type].append(s)
				else:
					if s.keyword != "":
						locTypes[s.type] = []
						locTypes[s.type].append(s)
			
			for key in kwTypes.keys():
				res += "<theme>\n"
				res += "<themekt>" + key + "</themekt>\n"
				for val in kwTypes[key]:
					res += val.genFGDC()
				res += "</theme>\n"

			for key in locTypes.keys():
				res += "<place>\n"
				res += "<placekt>" + key + "</placekt>\n"
				for val in locTypes[key]:
					res += val.genFGDCloc()
				res += "</place>\n"
			res += """
			</keywords>
			"""
		res += """
		<ptcontac>
			<cntinfo>
				<cntperp>
					<cntper>""" + self.contact.name + """</cntper>
					<cntorg>""" + self.contact.organisation + """</cntorg>
				</cntperp>
				<cntaddr>
					<addrtype>mailing and physical</addrtype>
					<address>
						""" + self.contact.deliveryPoint + """
					</address>
					<city>""" + self.contact.city + """</city>
					<state>""" + self.contact.area + """</state>
					<postal>""" + self.contact.postalCode + """</postal>
					<country>""" + self.contact.country + """</country>
				</cntaddr>
				<cntvoice>""" + self.contact.phone + """</cntvoice>
				<cntfax>""" + self.contact.facs + """</cntfax>
				<cntemail>""" + self.contact.email + """</cntemail>
			</cntinfo>
		</ptcontac>
		"""
		res += """
			</idinfo>
		\n"""

		res += """
			<distinfo>
				<distrib>
					<cntinfo>
						<cntperp>
							<cntper>""" + self.contact.name + """</cntper>
							<cntorg>""" + self.contact.organisation + """</cntorg>
						</cntperp>
						<cntaddr>
							<addrtype>mailing and physical</addrtype>
							<address>
								""" + self.contact.deliveryPoint + """
							</address>
							<city>""" + self.contact.city + """</city>
							<state>""" + self.contact.area + """</state>
							<postal>""" + self.contact.postalCode + """</postal>
							<country>""" + self.contact.country + """</country>
						</cntaddr>
						<cntvoice>""" + self.contact.phone + """</cntvoice>
						<cntfax>""" + self.contact.facs + """</cntfax>
						<cntemail>""" + self.contact.email + """</cntemail>
					</cntinfo>
				</distrib>
				<distliab>[unknown]</distliab>
			</distinfo>
		"""

		res += "<metainfo>\n"

		year = datetime.date.today().year
		month = datetime.date.today().month
		day = datetime.date.today().day

		res += "<metd>" + str(year)+str(month)+str(day) + "</metd>\n"

		if self.metaName or self.metaAll:
			#res += "<ptcontac>"
			res += "<metc>"
			for s in self.namesData:
				res += s.genFGDC()
			res += "</metc>"
			#res += "</ptcontac>"
		res += """
			<metstdn>
				FGDC Content Standard for Digital Geospatial Metadata
			</metstdn>
			<metstdv>FGDC-STD-1998-1</metstdv>
		"""
		res += "</metainfo>\n"

		res += "</metadata>\n"

		#STXTfile.write(res)
		#STXTfile.close()
		#self.saveFile(self.OUTFilename, res)
		return res
	# <meta name="DC.Title" content="Заголовок страницы">
	# <meta name="DC.Creator" content="Имя сайта или создателя страницы">
	# <meta name="DC.Subject" content="Тема содержания ресурса">
	# <meta name="DC.Description" content="Описание страницы">
	# <meta name="DC.Publisher" content="Издатель">
	# <meta name="DC.Contributor" content="Соисполнитель">
	# <meta name="DC.Date" content="Дата создания материала">
	# <meta name="DC.Type" content="Тип ресурса">
	# <meta name="DC.Format" content="Формат ресурса">
	# <meta name="DC.Identifier" content="URL текущей страницы (Идентификатор ресурса)">
	# <meta name="DC.Source" content="Источник данных">
	# <meta name="DC.Language" content="Язык контента">
	# <meta name="DC.Coverage" content="Геотаргетинг">
	# <meta name="DC.Rights" content="Авторские права">
	def saveToDublin(self):
		print(self.OUTFilename+' - OUT_FILE')
		STXTfile = codecs.open(self.OUTFilename, "w", self.config.fileCodec)

		res = ""
		if self.metaTitle or self.metaAll:
			_date = re.search(r'[0-9]{4}', self.title).group(0)
			if _date is None:
				_date = ""
			_title = self.title.replace('\n', ' ')
			res += "<meta name=\"DC.Title\" content=\"" + _title +"\">\n"
			res += "<meta name=\"DC.Date\" content=\"" + _date + "\">\n"
			res += "<meta name=\"DC.Language\" content=\"en-EN\">\n"
			#res += "<meta name=\"DC.Coverage\" content=\"Eastern Pacific\">"
		
		#<meta name="DC.Description" content="Описание страницы">
		#if self.metaContent or self.metaAll:
		#	STXTfile.write('CONTENT\n')
		#	for t in self.pdf.getTitles():
		#		STXTfile.write(t+'\n')
		if self.metaName or self.metaAll:
			res += "<meta name=\"DC.Creator\" content=\""
			for s in self.namesData:
				res += s.name+","
			res = res[0:len(res)-1]
			res += "\">\n"
		#if self.metaLocation or self.metaAll:
		#	for s in self.locationsData:
		#		res += s.genFGDC()

		if self.metaKeyWord or self.metaAll:
			res += "<meta name=\"DC.Subject\" content=\""
			i = 0
			for s in self.keywordsData:
				kp = s.genText()
				if i >= self.config.countKeyPhrases:
					break
				if len(kp.split()) > self.config.maxKeyPhraseLength or len(kp) < 4:
					continue
				res += kp + ","
				i += 1
			res = res[0:len(res)-1]
			res +="\">\n"
		
		STXTfile.write(res)
		STXTfile.close()







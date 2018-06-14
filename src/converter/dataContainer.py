
import re

class DataPerson:
	def __init__(self, name, 
		organisation="",
		phone="",
		facs="",
		deliveryPoint="",
		city="",
		area="",
		postalCode="",
		country="",
		email=""):
	
		self.name = name
		self.organisation = organisation
		self.phone = phone
		self.facs = facs
		self.deliveryPoint = deliveryPoint
		self.city = city
		self.area = area
		self.postalCode = postalCode
		self.country = country
		self.email = email

	def setName(self, _in):
		self.name = _in
	def setOrganisation(self, _in):
		self.organisation = _in
	def setPhone(self, _in):
		self.phone = _in
	def setFacs(self, _in):
		self.facs = _in
	def setDeliveryPoint(self, _in):
		self.deliveryPoint = _in
	def setCity(self, _in):
		self.city = _in
	def setArea(self, _in):
		self.area = _in
	def setPostalCode(self, _in):
		self.postalCode = _in
	def setCountry(self, _in):
		self.country = _in
	def setEmail(self, _in):
		self.email = _in
		
	def genText(self):
		res = ""
		res += "Name: " + self.name + "\n"
		res += "Organisation: " + self.organisation + "\n"
		res += "Phone: " + self.phone + "\n"
		res += "Facs: " + self.facs + "\n"
		res += "DeliveryPoint: " + self.deliveryPoint + "\n"
		res += "City: " + self.city + "\n"
		res += "Area: " + self.area + "\n"
		res += "PostalCode: " + self.postalCode + "\n"
		res += "Country: " + self.country + "\n"
		res += "Email: " + self.email + "\n"
		return res

	def genISO115v2(self):
		res = """
			<gmd:CI_ResponsibleParty>
				<gmd:individualName>
					<gco:CharacterString>""" + self.name + """</gco:CharacterString>
				</gmd:individualName>
				<gmd:organisationName>
					<gco:CharacterString>""" + self.organisation + """</gco:CharacterString>
				</gmd:organisationName>
				<gmd:contactInfo>
					<gmd:CI_Contact>
						<gmd:phone>
							<gmd:CI_Telephone>
								<gmd:voice>
									<gco:CharacterString>""" + self.phone + """</gco:CharacterString>
								</gmd:voice>
								<gmd:facsimile>
									<gco:CharacterString>""" + self.facs + """</gco:CharacterString>
									</gmd:facsimile>
							</gmd:CI_Telephone>
						</gmd:phone>
						<gmd:address>
							<gmd:CI_Address>
								<gmd:deliveryPoint>
									<gco:CharacterString>""" + self.deliveryPoint + """</gco:CharacterString>
								</gmd:deliveryPoint>
								<gmd:city>
									<gco:CharacterString>""" + self.city + """</gco:CharacterString>
								</gmd:city>
								<gmd:administrativeArea>
									<gco:CharacterString>""" + self.area + """</gco:CharacterString>
								</gmd:administrativeArea>
								<gmd:postalCode>
									<gco:CharacterString>""" + self.postalCode + """</gco:CharacterString>
								</gmd:postalCode>
								<gmd:country>
									<gco:CharacterString>""" + self.country + """</gco:CharacterString>
								</gmd:country>
								<gmd:electronicMailAddress>
									<gco:CharacterString>""" + self.email + """</gco:CharacterString>
								</gmd:electronicMailAddress>
							</gmd:CI_Address>
						</gmd:address>
					</gmd:CI_Contact>
				</gmd:contactInfo>
				<gmd:role>
					<gmd:CI_RoleCode codeList="http://www.isotc211.org/2005/resources/codeList.xml#CI_RoleCode"
						codeListValue="pointOfContact"/>
				</gmd:role>
			</gmd:CI_ResponsibleParty>\n"""
		return res

	def genFGDC(self):
		res = """
			<cntinfo>
				<cntorgp>
					<cntorg>""" + self.organisation + """</cntorg>
					<cntper>""" + self.name + """</cntper>
				</cntorgp>
				<cntaddr>
					<addrtype>mailing and physical</addrtype>
					<address>""" + self.deliveryPoint + """</address>
					<city>""" + self.city + """</city>
					<state>""" + self.area + """</state>
					<postal>""" + self.postalCode + """</postal>
					<country>""" + self.country + """</country>
				</cntaddr>
				<cntvoice>""" + self.phone + """</cntvoice>
				<cntfax>""" + self.facs + """</cntfax>
				<cntemail>""" + self.email + """</cntemail>
			</cntinfo>\n"""
		return res

class DataKeyword:
	def __init__(self, keyword):
		self.keyword = keyword
		self.type = "None"

	def genText(self):
		return self.keyword

	def genISO115v2(self):
		return """
			<gmd:keyword>
				<gco:CharacterString>""" + self.keyword + """</gco:CharacterString>
			</gmd:keyword>\n"""

	def genFGDC(self):
		return """
				<themekey>""" + self.keyword + """</themekey>
				"""
	def genFGDCloc(self):
		return """
				<placekey>""" + self.keyword + """</placekey>
				"""
class DataRef:
	def __init__(self, ref):
		self.ref = ref

		_d = re.search("[0-9]{4}", self.ref)
		if _d is None:
			_date = ""
			_yPos = 0
		else:
			_date = _d.group(0)
			_yPos = _d.start()

		if _yPos != 0 and self.ref[_yPos-1] == "(":
			self.origin = self.ref[0:_yPos-1]
		else:
			self.origin = self.ref[0:_yPos]
		self.date = _date

		regexSepr = "(([0-9]+[\\-:][0-9]*\\.?)|([0-9]+[0-9\\-–\\n]*(\\s*)((pp)|(p))\\.?)|((\\s*)[0-9]+[\\-,–\\n]+[0-9]+\\.?)|((\\s*)((pp)|(p))\\.)(\\s*)[0-9]+[0-9\\-–\\n]*)"
		_tEnd = re.search(regexSepr, self.ref)
		if _tEnd is None:
			self.title = self.ref[_yPos+4:]
		else:
			self.title = self.ref[_yPos+4:_tEnd.start()]
		self.link = ""

	def genText(self):
		return self.ref

	def genISO115v2(self):
		#_d = re.search("[0-9]{4}", self.ref)
		#if _d is None:
		#	_date = ""
		#else:
		#	_date = _d.group(0)
		return """
			<gmd:CI_Citation>
				<gmd:title>
					<gco:CharacterString>""" + self.title + """</gco:CharacterString>
				</gmd:title>
				<gmd:date>
					<gmd:CI_Date>
						<gmd:date>
							<gco:Date>""" + self.date + """</gco:Date>
						</gmd:date>
						<gmd:dateType>
							<gmd:CI_DateTypeCode codeList=" http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode "
								codeListValue="creation">creation</gmd:CI_DateTypeCode>
						</gmd:dateType>
					</gmd:CI_Date>
				</gmd:date>
				<gmd:edition>
					<gco:CharacterString>Version</gco:CharacterString>
				</gmd:edition>
			</gmd:CI_Citation>\n"""

	def genFGDC(self):
		#_d = re.search("[0-9]{4}", self.ref)
		#if _d is None:
		#	_date = ""
		#else:
		#	_date = _d.group(0)
		return """
		 <citeinfo>
			<origin>""" + self.origin + """</origin>
			<pubdate>""" + self.date + """</pubdate>
			<title>""" + self.title + """</title>
			<onlink>""" + self.link + """</onlink>
		</citeinfo>\n"""

class DataLocation:
	def __init__(self, location):
		self.location = location
		if location == "":
			self.name = ""
			self.west = ""
			self.east = ""
			self.north = ""
			self.south = ""
		else:
			data = self.location.split('+')
			self.name = data[0]
			self.west = data[4]
			self.east = data[3]
			self.north = data[2]
			self.south = data[1]

	def genText(self):
		return self.location.replace('-', ' ')

	def genISO115v2(self):
		#data = self.location.split('-')
		return """
			<gmd:geographicElement>
				<gmd:EX_GeographicBoundingBox>
					<gmd:westBoundLongitude>
						<gco:Decimal>""" + self.west + """</gco:Decimal>
					</gmd:westBoundLongitude>
					<gmd:eastBoundLongitude>
						<gco:Decimal>""" + self.east + """</gco:Decimal>
					</gmd:eastBoundLongitude>
					<gmd:southBoundLatitude>
						<gco:Decimal>""" + self.south + """</gco:Decimal>
					</gmd:southBoundLatitude>
					<gmd:northBoundLatitude>
						<gco:Decimal>""" + self.north + """</gco:Decimal>
					</gmd:northBoundLatitude>
				</gmd:EX_GeographicBoundingBox>
			</gmd:geographicElement>\n"""

	def genFGDC(self):
		#data = self.location.split('-')
		return """
		<bounding>
			<westbc>""" + self.west + """</westbc>
			<eastbc>""" + self.east + """</eastbc>
			<northbc>""" + self.north + """</northbc>
			<southbc>""" + self.south + """</southbc>
		</bounding>\n"""

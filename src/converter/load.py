
import requests
import codecs

def insertDataFromFile(protocol, url, user, passwd, path):
	"""
	protocol: http/https
	url: url adress:port without http/https
	user: username
	passwd: username password
	path: path to xml data file
	"""
	
	xmlFile = codecs.open(path, "r", "utf-8")
	xmlPayload = xmlFile.read()
	xmlFile.close()
	insertData(protocol, url, user, passwd, xmlPayload)
	

def insertData(protocol, url, user, passwd, xmlPayload):
	insertURL = protocol+"://"+user+":"+passwd+"@"+url + '/srv/eng/csw-publication'
	session = requests.Session()

	xmlInsert = '''<?xml version="1.0" encoding="UTF-8"?>
	<csw:Transaction service="CSW" version="2.0.2" xmlns:csw="http://www.opengis.net/cat/csw/2.0.2">
	<csw:Insert>
	%s
	</csw:Insert>
	</csw:Transaction>''' % (xmlPayload)
	
	headers = {'Content-Type': 'application/xml'}
	response = session.post(insertURL, data=xmlInsert.encode('utf-8'), headers=headers)
	return(response.status_code, response.text)


def insertData2(protocol, url, user, passwd, inputPath):
	login_j = protocol+"://"+url + '/j_spring_security_check'
	logout_j = protocol+"://"+url + '/j_spring_security_logout'
	insert_url = protocol+"://"+url + '/srv/eng/csw-publication'
	
	session = requests.Session()
	
	headers = {'Mime-type': 'application/xml'}
	hdata = {'Content-Type': 'application/x-www-form-urlencoded'}
	params = {'username': '%s' % user, 'password': '%s' % passwd}

	session.post(url=logout_j, headers={'Connection': 'close'})
	
	response_login = session.post(url, data=params, headers=hdata)  # login to geonetwork
	#print(response_login.text.encode('utf-8'))  # debug
	xml_file = codecs.open(input_path, "r", "utf-8")
	xml_payload = xml_file.read()
	xml_file.close()
	xml_insert = '''<?xml version="1.0" encoding="UTF-8"?>
	<csw:Transaction service="CSW" version="2.0.2" xmlns:csw="http://www.opengis.net/cat/csw/2.0.2">
	<csw:Insert>
	%s
	</csw:Insert>
	</csw:Transaction>''' % (xml_payload)
	
	headers = {'Content-Type': 'application/xml'}
	response_insert = session.post(insert_url, data=xml_insert.encode('utf-8'), headers=headers)  # insert metadata
	
	session.post(url=logout_j, headers={'Connection': 'close'})
	
	return(response_insert.status_code, response_insert.text)
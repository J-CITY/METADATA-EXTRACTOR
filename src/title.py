from main import PDFContainer
import re
import codecs

title = ''

# pdf = PDFContainer(format="text", codec='utf-8')	
# pdf.convertPDF("53.pdf")
# txt = pdf.getPage(0)
# txts = txt.split('\n')
# 
# TXTfile = codecs.open("out1.txt", "w", "utf-8")
# TXTfile.write(txt)
# TXTfile.close()
txt = ''
with codecs.open("out1.txt", "r", "utf-8") as f:
    txt = f.read()
# txts = txt.split('\n')

title = re.search(r'PICES SCIENTIFIC REPORT(\s*)No\.(\s*)([0-9]+),(\s*)[0-9]{4}([a-zA-z0-9\.,\-\s]*)ISBN', txt) .group(0)

# isTitle = False
# isYear = False
# isNo = False
# isStart = False
# title = ''
# for t in txts:
# 	if not isStart and re.match(r'PICES SCIENTIFIC REPORT', t) == None:
# 		isStart = True
# 		continue
# 	_re = re.match(r'\s*', t)
# 	if _re == None:
# 		if isTitle:
# 			break
# 		else:
# 			continue
# 
# 	
# 	_re = re.search(r'[0-9]{4}', t)
# 	if _re != None:
# 		title += 'Year ' + _re.group(0) + '\n'
# 		isYear = True
# 		
# 	_re = re.search(r'No\.(\s*)[0-9]{1:}', t)
# 	if _re != None:
# 		title += _re.group(0) + '\n'
# 		isNo = True
# 		
# 	if not isYear or not isNo:
# 		continue
# 		
# 	_re0 = re.search(r'ISBN', t)
# 	_re1 = re.search(r'ISSN', t)
# 	if _re0 != None or _re1 != None:
# 		break
# 	else:
# 		isTitle = True
# 		title += t
		
print(title)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import codecs
import re

import nltk.data

class ExtracrReference:
	def __init__(self, text):
		# REGEX HARWORD
		self.regexName = "(((de)|(De)|(da)|(van)|(zu)|(di)|(der)|(tot)|(thoe))(\\s*)){0,1}([A-Z]{1})([A-Za-z\\-])+,(\\s*)([A-Za-z\\.]+)"
		self.regexNames = "(" + self.regexName + "(\\s*)[and,]*(\\s*)){1,}"
		self.regexEds = "(\\(Ed\\.\\))|(\\(Eds\\.\\))"
	
		self.regexNamesEds = self.regexNames + "(\\s*)" + "("+self.regexEds+")*"
		self.regexYear = "[0-9]{4}\\.";
		self.regexNamesEdsYear = self.regexNames + "(\\s*)" + "("+self.regexEds+")*" + "(\\s*)" + "("+self.regexYear+"){1}"
	
		self.regexTitleAndCharacteristics = "[A-Za-z0-9/\\.,\\s();\\-:–]{1,300}(([0-9]+[\\-:][0-9]*\\.?)|([0-9]+[0-9\\-–\\n]*(\\s*)((pp)|(p))\\.?)|((\\s*)[0-9]+[\\-,–\\n]+[0-9]+\\.?)|((\\s*)((pp)|(p))\\.)(\\s*)[0-9]+[0-9\\-–\\n]*)"
		# self.regexTitleAndCharacteristics = "[A-Za-z0-9/\\.,\\s();\\-:]{1,300}[0-9]+(([\\-:][0-9]+\\.)|((\\s*)pp\\.))"
		self.regexReference = self.regexNamesEdsYear  + "(\\s*)" + self.regexTitleAndCharacteristics
	
		###APA
		self.regexNameAPA = "[A-Z]+[A-Za-z\\-]+,(\\s*)([A-Za-z\\.]*)"
		self.regexNamesAPA = "(" + self.regexName + "(\\s*)[and,&]*(\\s*)){1,}"
		self.regexEdsAPA = "(\\(Ed\\.\\))|(\\(Eds\\.\\))"
		self.regexNamesEdsAPA = self.regexNames + "(\\s*)" + "("+self.regexEds+")*"
		self.regexYearAPA = "\\([0-9]*\\)\\.";
		self.regexNamesEdsYearAPA = self.regexNames + "(\\s*)" + "("+self.regexEds+")*" + "(\\s*)" + "("+self.regexYear+")*"
		self.regexTitleAndCharacteristicsAPA = "[A-Za-z0-9/\\.,\\s();\\-:]{1,300},(\\s*)[0-9]+(\\([A-Za-z]*\\))"
		self.regexPagesAPA = "(\\s*)[0-9\\-]\\."
		self.regexReferenceAPA = self.regexNamesEdsYear  + "(\\s*)" + self.regexTitleAndCharacteristics + "," + self.regexPagesAPA
		
		
		self.text = text
	
	def extract(self):
		outfile = codecs.open("refs.txt", "w", "utf-8")
		expr = re.compile(self.regexReference, re.UNICODE)
		for match in expr.finditer(self.text):
			outfile.write(match.group(0)+" ::-\n")
			#print(match.group(0)+"\n____________________\n")
		outfile.close()
		
class PDFContainer:
    def __init__(self, format='text', codec='utf-8'):
        self.format = format
        self.codec = codec
        self.password = ''
        self.pages = []

    def reinit(self):
        rsrcmgr = PDFResourceManager()
        retstr = BytesIO()
        laparams = LAParams()
        if self.format == 'text':
            device = TextConverter(rsrcmgr, retstr, codec=self.codec, laparams=laparams)
        elif self.format == 'html':
            device = HTMLConverter(rsrcmgr, retstr, codec=self.codec, laparams=laparams)
        elif self.format == 'xml':
            device = XMLConverter(rsrcmgr, retstr, codec=self.codec, laparams=laparams)
        else:
            raise ValueError('provide format, either text, html or xml!')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        return {'retstr': retstr, 'device': device, 'interpreter': interpreter}
    
    def convertPDF(self, path):
        fp = open(path, 'rb')

        ri = self.reinit()
        retstr = ri['retstr']
        device = ri['device']
        interpreter = ri['interpreter']

        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=self.password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
            self.pages.append(retstr.getvalue().decode())
            ri = self.reinit()
            device.close()
            retstr.close()
            retstr = ri['retstr']
            device = ri['device']
            interpreter = ri['interpreter']
        fp.close()
        device.close()
        retstr.close()
        return

    def getPage(self, p):
        return self.pages[p]

    def getPages(self, ps, pe):
        text = ''
        for i in range(ps, pe):
            text += self.pages[i]
        return text

#pdf = PDFContainer(format="text", codec='utf-8')	
#pdf.convertPDF("53.pdf")
#txt = pdf.getPage(1)
#TXTfile = codecs.open("out.txt", "w", "utf-8")
#TXTfile.write(txt)
#TXTfile.close()
#
#
#tokenizer = nltk.data.load('data/tokenizers/english.pickle')
#sents = tokenizer.tokenize(txt)
#sentstxt = ""
#for s in sents:
#	sentstxt += s
#	sentstxt += "___\n"
#STXTfile = codecs.open("outs.txt", "w", "utf-8")
#STXTfile.write(sentstxt)
#STXTfile.close()
t = ""
with open('53.txt', encoding='utf-8') as f:
  for line in f:
    t += line
	
extr = ExtracrReference(t)
extr.extract()
	
	
	
	
	
	
	
	
	
	
	
	
	


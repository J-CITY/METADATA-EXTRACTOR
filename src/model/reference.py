from io import BytesIO
import codecs
import re

import nltk.data

class ExtracrReference:
	def __init__(self, text):
		# REGEX HARWORD
		self.regexName = "(((de)|(De)|(da)|(van)|(zu)|(di)|(der)|(tot)|(thoe))(\\s*)){0,1}([A-ZС]{1})([A-Za-z\\-С])+,(\\s*)([A-Za-z\\.С]+)"
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
		
		
		self.regexSepr = "(([0-9]+[\\-:][0-9]*\\.?)|([0-9]+[0-9\\-–\\n]*(\\s*)((pp)|(p))\\.?)|((\\s*)[0-9]+[\\-,–\\n]+[0-9]+\\.?)|((\\s*)((pp)|(p))\\.)(\\s*)[0-9]+[0-9\\-–\\n]*)"

		self.text = text
	
	def test(self):
		expr = re.compile(self.regexReference, re.UNICODE)
		for match in expr.finditer(self.text):
			print(match.group(0))

	def extract(self):
		#outfile = codecs.open("refs.txt", "w", "utf-8")
		refs = []
		expr = re.compile(self.regexReference, re.UNICODE)
		sepr = re.compile(self.regexSepr, re.UNICODE)
		for match in expr.finditer(self.text):
			#r = sepr.split(match.group(0))
			#refs.append(match.group(0))
			r = match.group(0)
			start = 0
			for m in sepr.finditer(r):
				_r = r[start:m.span()[1]]
				if len(_r) < 15:
					continue
				refs.append(_r+"--")
				start = m.span()[1]
			#refs.extend(r)
			#print(r)
			#outfile.write(match.group(0)+" ::-\n")
			#print(match.group(0)+"\n____________________\n")
		#outfile.close()
		return refs

#er = ExtracrReference('Teng, S.T., Lim, P.T., Rivera-Vilarelle, M., Quijano-Scheggia, S., Takata, Y., Quilliam, M., Wolf, M., Bates, S.S. and Leaw, С.P. 2016. A non-toxigenic but morphologically and phylogenetically distinct new species of Pseudo-nitzschia, P. sabit sp. nov. (Bacillariophyceae). J. Phycol. 51: 706–725.  ')
#er.test()
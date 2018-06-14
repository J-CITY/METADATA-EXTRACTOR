import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
	
from converter.pdfextractor import PDFContainer
from collections import Counter, defaultdict

def test(expect, output):
	if expect == output:
		print("OK")
	else:
		print("ERR", expect, " ", output)

p = PDFContainer(format='filter')

p.convertPDF("test.pdf")

test(p.getTitles(), [])
test(p.getPage(0), "")
test(p.getPages(0,1), "")
test(p.getAllPages(), "")
test(p.getSize(), 1)

p.convertPDFAlternative("test.pdf")
test(p.getTitles(), [])
test(p.getPage(0), "")
test(p.getPages(0,1), "")
test(p.getAllPages(), " \n This is a test PDF document.\nIf you can read this, you have Adobe Acrobat Reader installed on your computer.")
test(p.getSize(), 2)
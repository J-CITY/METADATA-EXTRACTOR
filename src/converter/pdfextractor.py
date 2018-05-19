from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.layout import LTTextBoxHorizontal, LTTextBox
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import codecs
import re

import nltk.data

class PDFContainer:
    def __init__(self, format='text', codec='utf-8'):
        self.format = format
        self.codec = codec
        self.password = ''
        self.pages = []
        self.titles = []

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
        elif self.format == 'filter':
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
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

    def convertPDFFilter(self, path):
        fp = open(path, 'rb')

        ri = self.reinit()
        retstr = ri['retstr']
        device = ri['device']
        interpreter = ri['interpreter']

        parser = PDFParser(fp)
        document = PDFDocument(parser, self.password)
        try:
            outlines = document.get_outlines()
            for (level,title,dest,a,se) in outlines:
                self.titles.append(str(level) + ' ' + title)
                #print (level, title)
        except PDFNoOutlines:
            self.titles = []

        #metadata = document.info
        #print(metadata)
        #for x in metadata:
        #    if x == "Title":
        #        print(x)
        

        i = 0
        for page in PDFPage.get_pages(fp):
            print(i)
            if i > 20 and i < 40:
                i+=1
                continue
            i+=1
            interpreter.process_page(page)
            layout = device.get_result()
            ptxt = ''
            for e in layout:
                if isinstance(e, LTTextBoxHorizontal):
                    #print(element.get_text())
                    ptxt += e.get_text()
            self.pages.append(ptxt)
        fp.close()
        device.close()
        retstr.close()
        return

    def convertPDFAlternative(self, path):
        from PyPDF2.pdf import PdfFileReader
        pdf = PdfFileReader(open(path, "rb"))
        for i in range(0, pdf.getNumPages()):
            print(i)
            extractedText = pdf.getPage(i).extractText()
            self.pages.append(extractedText)

    def getTitles(self):
        return self.titles

    def getPage(self, p):
        if p < self.getSize():
            return self.pages[p]
        return self.pages[0]

    def getPages(self, ps, pe):
        if ps < pe and ps >= 0 and pe < self.getSize():
            text = ''
            for i in range(ps, pe):
                text += self.pages[i]
            return text
        return self.pages[0]
    def getAllPages(self):
        res = ''
        for p in self.pages:
            res += p
        return res

    def getSize(self):
        return len(self.pages)



#pdf = PDFContainer(format='filter', codec='utf-8')
#pdf.convertPDFFilter('38.pdf')
#txt = pdf.getPages(0,1)
#STXTfile = codecs.open("regex_1.txt", "w", "utf-8")
#STXTfile.write(txt)
#STXTfile.close()
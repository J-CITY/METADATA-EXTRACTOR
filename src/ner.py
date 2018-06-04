import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

from model.utils.utils import CoNLLDataset
from model.nerModel import NERModel
from config.config import Config

import codecs
import re

def runModel(sentences):
    config = Config()
    model = NERModel(config)
    model.build()
    model.reloadSession(config.dirModel)

    STXTfile = codecs.open("outNames.txt", "w", "utf-8")
    for sentence in sentences:
        wordsRaw = sentence.strip().split(" ")

        wR = []
        for w in wordsRaw:
            _w = re.sub(r'(\.*)[0-9]+', '', w)
            wR.append(_w)
        preds = model.predict(wR) 
        for i, w in enumerate(wR):
            res = ""
            res += w + " " + preds[i]
            res += "\n"
            STXTfile.write(res)
        STXTfile.write('-------------\n')
    STXTfile.close()

class NERExtractor:
    def __init__(self, config):
        self.config = config
        self.model = NERModel(self.config)
        self.model.build()
        self.model.reloadSession(self.config.dirModel)

    def extractFromSentence(self, sentence, isNames=False):
        _wordsRaw = sentence.strip().split(" ")
        wordsRaw = []
        if isNames:
            for w in _wordsRaw:
                wordRaw.append(re.sub(r'(\.*)[0-9]+', '', w))
        else:
            wordsRaw = _wordsRaw
        preds = self.model.predict(wordsRaw)
        return wordsRaw, preds

#runModel(['E.A. Pakhomov, A.V. Suntsov, M.P. Seki, R.D. Brodeur, R. Domokos, L.G. Pakhomova and K.R. Owen....3 '])
#ner = NERExtractor()
#ner.extractFromSentence("Bob and Daniil go to New York.")


from converter.pdfextractor import PDFContainer
import nltk.data

pdf = PDFContainer(format="filter", codec='utf-8')	
pdf.convertPDFFilter("50.pdf")
txt = pdf.getPages(0, 5)

tokenizer = nltk.data.load('data/tokenizers/english.pickle')
sents = tokenizer.tokenize(txt)

ofile = codecs.open("outtext.txt", "w", "utf-8")
for w in sents:
    ofile.write(w+'\n\n')
ofile.close()


runModel(sents)

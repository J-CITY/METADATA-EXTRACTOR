from model.utils.utils import CoNLLDataset
from model.nerModel import NERModel
from model.config import Config

import codecs

def runModel(sentences):
    config = Config()
    model = NERModel(config)
    model.build()
    model.reloadSession(config.dirModel)

    STXTfile = codecs.open("outs.txt", "w", "utf-8")
    for sentence in sentences:
        wordsRaw = sentence.strip().split(" ")
        preds = model.predict(wordsRaw) 
        for i, w in enumerate(wordsRaw):
            res = ""
            res += w + " " + preds[i]
            res += "\n"
            if preds[i] == "I-PER":
                STXTfile.write(res)
    STXTfile.close()

class NERExtractor:
    def __init__(self):
        self.config = Config()
        self.model = NERModel(self.config)
        self.model.build()
        self.model.reloadSession(self.config.dirModel)

    def extractFromSentence(self, sentence):
        wordsRaw = sentence.strip().split(" ")
        preds = self.model.predict(wordsRaw)
        return wordsRaw, preds

#from main import PDFContainer
#import nltk.data
#
#pdf = PDFContainer(format="text", codec='utf-8')	
#pdf.convertPDF("53.pdf")
#txt = pdf.getPages(1, 5)
#
#tokenizer = nltk.data.load('data/tokenizers/english.pickle')
#sents = tokenizer.tokenize(txt)
#
#runModel(sents)

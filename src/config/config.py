import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

from converter.preferences import Preferences
from model.utils.utils import getCompactGloveVectors, loadDictionary, getProcessingWord

class Config():
    def __init__(self, load=True):
        # directory for training outputs
        if not os.path.exists(self.dirOutput):
            os.makedirs(self.dirOutput)
        if load:
            self.load()

    def load(self):
        # 1. dict
        self.dictWords = loadDictionary(self.filenameWords)
        self.dictTags  = loadDictionary(self.filenameTags)
        self.dictChars = loadDictionary(self.filenameChars)

        self.nwords = len(self.dictWords)
        self.nchars = len(self.dictChars)
        self.ntags  = len(self.dictTags)

        # 2. get processing functions that map str -> id
        self.processingWord = getProcessingWord(self.dictWords,
                self.dictChars, lowercase=True, chars=self.useChars)
        self.processingTag  = getProcessingWord(self.dictTags,
                lowercase=False, allowUNK=False)

        # 3. get pre-trained embeddings
        self.embeddings = (getCompactGloveVectors(self.filenameCompact)
                if self.usePretrained else None)


    # general config
    dirOutput = "data/result/"
    dirModel  = dirOutput + "model.weights/"

    # embeddings
    dimWord = 300
    dimChar = 100

    # glove files
    filenameGlove = "data/glove/glove.6B.{}d.txt".format(dimWord)
    filenameCompact = "data/glove.6B.{}d.compact.npz".format(dimWord)
    usePretrained = True

    # dataset
    filenameDev = "data/conll/en/eng.testa"
    filenameTest = "data/conll/en/eng.testb"
    filenameTrain = "data/conll/en/eng.train"

    maxIter = None # if not None, max number of examples in Dataset

    # created from dataset with buildData.py
    filenameWords = "data/words.txt"
    filenameTags = "data/tags.txt"
    filenameChars = "data/chars.txt"

    # training
    trainEmbeddings = False
    nepochs         = 15
    dropout         = 0.5
    batchSize       = 20
    lrMethod        = "adam"
    lr              = 0.001
    lrDecay         = 0.9
    clip            = -1
    nepochNoImprove = 3

    hiddenSizeChar = 100
    hiddenSizeLstm = 300

    useCrf = True
    useChars = True

    # othe params
    fileCodec = 'utf-8'
    outPDFFormat = 'filter'
    sentencesSplitterModel = 'data/tokenizers/english.pickle'
    minTanimoto = 0.6
    stopWords = 'data\stopwords\en'
    punctuations = '!@#$%^&*()_+=?/.,;:°–'

    maxKeyPhraseLength = 4
    countKeyPhrases = 50
    
    protocol = "http"
    url = "localhost:8080/geonetwork2"
    user = "Daniil"
    passwd = "qwerty"
    inputPath = '_iso'

    def makeDafaultPreferences(self):
        pref = Preferences('data/prefs')

        pref.setPref("EXTRACT", "fileCodec", self.fileCodec)
        pref.setPref("EXTRACT", "outPDFFormat", self.outPDFFormat)
        pref.setPref("EXTRACT", "sentencesSplitterModel", self.sentencesSplitterModel)
        pref.setPref("EXTRACT", "minTanimoto", str(self.minTanimoto))
        pref.setPref("EXTRACT", "stopWords", self.stopWords)
        pref.setPref("EXTRACT", "punctuations", self.punctuations)

        pref.setPref("EXTRACT", "maxKeyPhraseLength", str(self.maxKeyPhraseLength))
        pref.setPref("EXTRACT", "countKeyPhrases", str(self.countKeyPhrases))

        pref.setPref("LOGIN", "protocol", self.protocol)
        pref.setPref("LOGIN", "url", self.url)
        pref.setPref("LOGIN", "user", self.user)
        pref.setPref("LOGIN", "passwd", self.passwd)
        pref.setPref("LOGIN", "inputPath", self.inputPath)

        pref.save()

    def loadPreferences(self):
        try:
            file = open('data/prefs')
            file.close()
        except IOError as e:
            self.setDefaultPreferences()
        else:
            pref = Preferences('data/prefs')
            pref.load()

            self.fileCodec = pref.getPref("EXTRACT", "fileCodec")
            self.outPDFFormat = pref.getPref("EXTRACT", "outPDFFormat")
            self.sentencesSplitterModel = pref.getPref("EXTRACT", "sentencesSplitterModel")
            self.minTanimoto = float(pref.getPref("EXTRACT", "minTanimoto"))
            self.stopWords = pref.getPref("EXTRACT", "stopWords")
            self.punctuations = pref.getPref("EXTRACT", "punctuations")
            self.protocol = pref.getPref("LOGIN", "protocol")
            
            self.maxKeyPhraseLength = int(pref.getPref("EXTRACT", "maxKeyPhraseLength"))
            self.countKeyPhrases = int(pref.getPref("EXTRACT", "countKeyPhrases"))
            
            self.url = pref.getPref("LOGIN", "url")
            self.user = pref.getPref("LOGIN", "user")
            self.passwd = pref.getPref("LOGIN", "passwd")
            self.inputPath = pref.getPref("LOGIN", "inputPath")

    def setDefaultPreferences(self):
        self.makeDafaultPreferences()
        self.loadPreferences()

    def updatePreferences(self, section, par, val):
        pref = Preferences('data/prefs')
        pref.load()
        pref.setPref(section, par, val)
        pref.save()
    
    def getPreferences(self):
        pref = Preferences('data/prefs')
        pref.load()
        return pref
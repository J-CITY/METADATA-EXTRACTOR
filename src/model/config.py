import os

from .utils.utils import getCompactGloveVectors, loadDictionary, getProcessingWord

class Config():
    def __init__(self, load=True):
        # directory for training outputs
        if not os.path.exists(self.dirOutput):
            os.makedirs(self.dirOutput)
        # load if requested (default)
        if load:
            self.load()


    def load(self):
        # 1. dict
        self.dictWords = loadDictionary(self.filenameWords)
        self.dictTags  = loadDictionary(self.filenameTags)
        self.dictChars = loadDictionary(self.filenameChars)

        self.nwords     = len(self.dictWords)
        self.nchars     = len(self.dictChars)
        self.ntags      = len(self.dictTags)

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
    pathLog   = dirOutput + "log.txt"

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

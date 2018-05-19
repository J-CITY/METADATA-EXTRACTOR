import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

from config.config import Config
from model.utils.utils import CoNLLDataset, getDictionary, UNK, NUM, \
    getGloveDictionary, saveDictionary, loadDictionary, getCharDictionary, \
    exportCompactGloveVectors, getProcessingWord


def main():
    # get config and processing of words
    config = Config(load=False)
    processingWord = getProcessingWord(lowercase=True)

    # Generators
    dev   = CoNLLDataset(config.filenameDev, processingWord)
    test  = CoNLLDataset(config.filenameTest, processingWord)
    train = CoNLLDataset(config.filenameTrain, processingWord)

    # Build Word and Tag
    dictWords, dictTags = getDictionary([train, dev, test])
    dictGlove = getGloveDictionary(config.filenameGlove)

    dictionary = dictWords & dictGlove
    dictionary.add(UNK)
    dictionary.add(NUM)

    # Save
    saveDictionary(dictionary, config.filenameWords)
    saveDictionary(dictTags, config.filenameTags)

    # Compact GloVe Vectors
    dictionary = loadDictionary(config.filenameWords)
    exportCompactGloveVectors(dictionary, config.filenameGlove, config.filenameCompact, config.dimWord)

    # Build and save char vocab
    train = CoNLLDataset(config.filenameTrain)
    dictChars = getCharDictionary(train)
    saveDictionary(dictChars, config.filenameChars)


if __name__ == "__main__":
    main()

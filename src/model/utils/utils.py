import numpy as np
import os
from .logger import printLog

UNK = "$UNK$"
NUM = "$NUM$"
NONE = "O"

class ParrotIOError(Exception):
    def __init__(self, filename):
        message = "ERROR: Can not find file {}.".format(filename)
        super(ParrotIOError, self).__init__(message)

# Class that iterates over CoNLL Dataset
class CoNLLDataset(object):
    def __init__(self, filename, processingWord=None, processingTag=None,
                maxIter=None):
        self.filename = filename
        self.processingWord = processingWord # function that takes a word as input
        self.processingTag = processingTag   # function that takes a tag as input
        self.maxIter = maxIter               # max number of sentences to yield
        self.length = None


    def __iter__(self):
        niter = 0
        with open(self.filename, encoding='utf-8') as f:
            words, tags = [], []
            for line in f:
                line = line.strip() # delete spaces in start and end
                if (len(line) == 0 or line.startswith("-DOCSTART-")):
                    if len(words) != 0:
                        niter += 1
                        if self.maxIter is not None and niter > self.maxIter:
                            break
                        yield words, tags
                        words, tags = [], []
                else:
                    ls = line.split(' ')
                    word, tag = ls[0],ls[-1]
                    if self.processingWord is not None:
                        word = self.processingWord(word)
                    if self.processingTag is not None:
                        tag = self.processingTag(tag)
                    words += [word]
                    tags += [tag]


    def __len__(self):
        if self.length is None:
            self.length = 0
            for _ in self:
                self.length += 1
        return self.length

#Create a dictionary from dataset
def getDictionary(datasets):
    printLog("Building dictionary: ")
    dictWords = set()
    dictTags = set()
    for dataset in datasets:
        for words, tags in dataset:
            dictWords.update(words)
            dictTags.update(tags)
    printLog("DONE: " + str(len(dictWords)) + " size")
    return dictWords, dictTags

def getCharDictionary(dataset):
    dictChar = set()
    for words, _ in dataset:
        for word in words:
            dictChar.update(word)
    return dictChar

#filename - path wo file with vectors
def getGloveDictionary(filename):
    printLog("Building dictionary")
    dictGlove = set()
    with open(filename, encoding='utf-8') as f:
        for line in f:
            word = line.strip().split(' ')[0]
            dictGlove.add(word)
    printLog("DONE: "+ str(len(dictGlove)) +" tokens")
    return dictGlove

def saveDictionary(dictionary, filename):
    printLog("SAVE")
    with open(filename, "w", encoding='utf-8') as f:
        for i, word in enumerate(dictionary):
            if i != len(dictionary) - 1:
                f.write("{}\n".format(word))
            else:
                f.write(word)

def loadDictionary(filename):
    try:
        d = dict()
        with open(filename, encoding='utf-8') as f:
            for idx, word in enumerate(f):
                word = word.strip()
                d[word] = idx
    except IOError:
        raise ParrotIOError(filename)
    return d

def exportCompactGloveVectors(dictionary, gloveFilename, trimmedFilename, dim):
    embeddings = np.zeros([len(dictionary), dim])
    with open(gloveFilename, encoding='utf-8') as f:
        for line in f:
            line = line.strip().split(' ')
            word = line[0]
            if word in dictionary:
                embedding = [float(x) for x in line[1:]] #glove coords
                wordID = dictionary[word]
                embeddings[wordID] = np.asarray(embedding)
    np.savez_compressed(trimmedFilename, embeddings=embeddings) # store glove matrix

def getCompactGloveVectors(filename):
    try:
        with np.load(filename) as data:
            return data["embeddings"]
    except IOError:
        raise ParrotIOError(filename)

def getProcessingWord(dictWords=None, dictChars=None,
                    lowercase=False, chars=False, allowUNK=True):
    def f(word):
        # char ids for word
        if (dictChars is not None) and (chars == True):
            charIDs = []
            for char in word:
                if (char in dictChars):
                    charIDs.append(dictChars[char])
        if lowercase:
            word = word.lower()
        if word.isdigit():
            word = NUM
        # word id
        if (dictWords is not None):
            if word in dictWords:
                word = dictWords[word]
            elif allowUNK:
                word = dictWords[UNK]
            else:
                raise Exception("Unknow tag.")
        if (dictChars is not None) and (chars == True):
            # chars ids and word id
            return charIDs, word
        # word id
        return word
    return f


def _padSequences(sequences, padtok, maxLength):
    sequencePadded, sequenceLength = [], []

    for seq in sequences:
        seq = list(seq)
        seq_ = seq[:maxLength] + [padtok]*max(maxLength - len(seq), 0)
        sequencePadded +=  [seq_]
        sequenceLength += [min(len(seq), maxLength)]
        # all sublist have same length

    return sequencePadded, sequenceLength


def padSequences(sequences, padtok, nlevels=1):
    if nlevels == 1:
        maxLength = max(map(lambda x : len(x), sequences))
        sequencePadded, sequenceLength = _padSequences(sequences,
                                            padtok, maxLength)

    elif nlevels == 2:
        maxLengthWord = max([max(map(lambda x: len(x), seq))
                               for seq in sequences])
        sequencePadded, sequenceLength = [], []
        for seq in sequences:
            # all words are same length
            sp, sl = _padSequences(seq, padtok, maxLengthWord)
            sequencePadded += [sp]
            sequenceLength += [sl]

        maxLengthSentence = max(map(lambda x : len(x), sequences))
        sequencePadded, _ = _padSequences(sequencePadded,
                [padtok]*maxLengthWord, maxLengthSentence)
        sequenceLength, _ = _padSequences(sequenceLength, 0,
                maxLengthSentence)

    return sequencePadded, sequenceLength


def minibatches(data, minibatchSize):
    x_batch, y_batch = [], []
    for (x, y) in data:
        if len(x_batch) == minibatchSize:
            yield x_batch, y_batch
            x_batch, y_batch = [], []

        if type(x[0]) == tuple:
            x = zip(*x)
        x_batch += [x]
        y_batch += [y]

    if len(x_batch) != 0:
        yield x_batch, y_batch


def getChunkType(tok, idxToTag):
    tagName = idxToTag[tok]
    tagClass = tagName.split('-')[0]
    tagType = tagName.split('-')[-1]
    return tagClass, tagType


def getChunks(seq, tags):
    """Given a sequence of tags, group entities and their position
    Args:
        seq: [4, 4, 0, 0, ...] sequence of labels
        tags: dict["O"] = 4
    Returns:
        list of (chunkType, chunkStart, chunkEnd)
    Example:
        seq = [4, 5, 0, 3]
        tags = {"B-PER": 4, "I-PER": 5, "B-LOC": 3}
        result = [("PER", 0, 2), ("LOC", 3, 4)]
    """
    default = tags[NONE]
    idxToTag = {idx: tag for tag, idx in tags.items()}
    chunks = []
    chunkType, chunkStart = None, None
    for i, tok in enumerate(seq):
        # End of a chunk 1
        if tok == default and chunkType is not None:
            # Add a chunk.
            chunk = (chunkType, chunkStart, i)
            chunks.append(chunk)
            chunkType, chunkStart = None, None

        # End of a chunk + start of a chunk!
        elif tok != default:
            tokChunkClass, tokChunkType = getChunkType(tok, idxToTag)
            if chunkType is None:
                chunkType, chunkStart = tokChunkType, i
            elif tokChunkType != chunkType or tokChunkClass == "B":
                chunk = (chunkType, chunkStart, i)
                chunks.append(chunk)
                chunkType, chunkStart = tokChunkType, i
        else:
            pass
    # end condition
    if chunkType is not None:
        chunk = (chunkType, chunkStart, len(seq))
        chunks.append(chunk)
    return chunks

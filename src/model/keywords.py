import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)

import string
from collections import Counter, defaultdict
from itertools import chain, groupby, product
from config.dictionary import supportWords
import nltk
from enum import Enum
from nltk.tokenize import wordpunct_tokenize
import nltk.data
import codecs
import re

METRIC_DEGREE_DIV_FREQUENCY = 0  # d / f
METRIC_DEGREE = 1  # d
METRIC_FREQUENCY = 2  # f


class KeywordExtractor:
    def __init__(self, stopwords=None, punctuations=None,
        metric=METRIC_DEGREE_DIV_FREQUENCY,
        minWordLength=5, maxPhraseLength=5, minWordAppears=5):

        self.metric = metric
        self.stopwords = stopwords
        #self.stopwords = nltk.corpus.stopwords.words('english')
        self.punctuations = punctuations
        #self.punctuations = string.punctuation
        #print(self.stopwords)
        self.minWordLength = minWordLength
        self.minWordAppears = minWordAppears
        self.maxPhraseLength = maxPhraseLength

        self.tokenizer = nltk.data.load('data/tokenizers/english.pickle')
        self.ignore = set(chain(self.stopwords, self.punctuations))
        self.frequency = None
        self.degree = None
        self.rankList = None
        self.rankedPhrases = None

    def _filter(self, sents):
        res = []
        for s in sents:
            flag = False
            for sw in supportWords:
                if s.find(sw) != -1:
                    flag = True
                    break
            if flag:
                res.append(s)

        return res

    def extractKeyWords(self, text):
        sents = self.tokenizer.tokenize(text)
        fsents = self._filter(sents)
        #sents = nltk.tokenize.sent_tokenize(text)
        self.extractKeyWordsFromSentences(fsents)

    def extractKeyWordsFromSentences(self, sentences):
        phraseList = self._genPhrases(sentences)
        self._calcFrequency(phraseList)
        self._calcWordGraph(phraseList)
        self._calcRank(phraseList)
        self._filterPhrases()

    def _filterPhrases(self):
        res = []
        expr = re.compile('[!@#$%^&*()_+=?/.,;:°–\\-0-9”`~]+', re.UNICODE)
        for p in self.rankedPhrases:
            if expr.search(p) != None:
                continue
            res.append(p)
        self.rankedPhrases = res

    def getRankedPhrases(self):
        return self.rankedPhrases

    def getRankedList(self):
        return self.rankList

    def getFrequency(self):
        return self.frequency

    def getWordDegrees(self):
        return self.degree

    def _calcFrequency(self, phrases):
        self.frequency = Counter(chain.from_iterable(phrases))
    
    def _calcWordGraph(self, phrases):
        graph = defaultdict(lambda: defaultdict(lambda: 0))
        for phrase in phrases:
            for (word, coword) in product(phrase, phrase):
                graph[word][coword] += 1
        self.degree = defaultdict(lambda: 0)
        for key in graph:
            self.degree[key] = sum(graph[key].values())

    def _calcRank(self, phrases):
        self.rankList = []
        for phrase in phrases:
            rank = 0.0
            for word in phrase:
                if self.metric == METRIC_DEGREE_DIV_FREQUENCY:
                    rank += 1.0 * self.degree[word] / self.frequency[word]
                elif self.metric == METRIC_DEGREE:
                    rank += 1.0 * self.degree[word]
                else:
                    rank += 1.0 * self.frequency[word]
            self.rankList.append((rank, " ".join(phrase)))
        self.rankList.sort(reverse=True)
        self.rankedPhrases = [ph[1] for ph in self.rankList]

    def _genPhrases(self, sentences):
        phrases = set()
        for sentence in sentences:
            words = [word.lower() for word in wordpunct_tokenize(sentence)]

            #porter = nltk.PorterStemmer()
            #_words = [porter.stem(t) for t in words]

            phrases.update(self._getPhraseWords(words))
        return phrases

    def _getPhraseWords(self, words):
        groups = groupby(words, lambda x: x not in self.ignore)
        return [tuple(group[1]) for group in groups if group[0]]

#txt = ""
#with open('53out.txt', encoding='utf-8') as f:
#    for line in f:
#        txt += line
#
#stopwords = []
#with open('data\stopwords\en', encoding='utf-8') as f:
#    for line in f:
#        stopwords.append(line[:len(line)-1])
#
#punctuations = '!@#$%^&*()_+=?/.,;:°–'
#
#ke = KeywordExtractor(stopwords = stopwords, punctuations=punctuations)
#ke.extractKeyWords(txt)
#ans = ke.getRankedPhrases()
#
#ofile = codecs.open("outkw.txt", "w", "utf-8")
#for w in ans:
#    _w = re.search(w, txt, re.IGNORECASE)
#    if _w:
#        ofile.write(_w.group(0)+'\n---------------\n')
#    #ofile.write(w+'\n---------------\n')
#ofile.close()


import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
	
from model.keywords import KeywordExtractor
from collections import Counter, defaultdict

def test(expect, output):
	if expect == output:
		print("OK")
	else:
		print("ERR", expect, " ", output)


import codecs
import re
txt = """
Set within a year after the events of Batman Begins, Batman, Lieutenant James Gordon, and new district attorney Harvey Dent successfully begin to round up the criminals that plague Gotham City until a mysterious and sadistic criminal mastermind known only as the Joker appears in Gotham, creating a new wave of chaos. Batman's struggle against the Joker becomes deeply personal, forcing him to "confront everything he believes" and improve his technology to stop him. A love triangle develops between Bruce Wayne, Dent and Rachel Dawes. Written by Leon Lombardi
"""
#txt = """
#Board the Millennium Falcon and journey to a galaxy far, far away in Solo: A Star Wars Story, an all-new adventure with the most beloved scoundrel in the galaxy. Through a series of daring escapades deep within a dark and dangerous criminal underworld, Han Solo meets his mighty future copilot Chewbacca and encounters the notorious gambler Lando Calrissian, in a journey that will set the course of one of the Star Wars saga’s most unlikely heroes.
#"""
stopwords = []
with open('data\stopwords\en', encoding='utf-8') as f:
    for line in f:
        stopwords.append(line[:len(line)-1])
punctuations = '!@#$%^&*()_+=?/.,;:°–'

ke = KeywordExtractor(stopwords = stopwords, 
    punctuations=punctuations, maxPhraseLength=5, minWordLength=5)
ke.extractKeyWords(txt)
ans = ke.getRankedPhrases()

ofile = codecs.open("outkw.txt", "w", "utf-8")
for w in ans:
    _w = re.search(w, txt, re.IGNORECASE)
    if _w:
        ofile.write(_w.group(0)+'\n---------------\n')
    ofile.write(w+'\n---------------\n')
ofile.close()


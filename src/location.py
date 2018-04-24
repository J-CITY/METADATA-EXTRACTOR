
class Location:
	def __init__(self, tw):
		self.ThresholdWord = tw

	def normalize(self, str):
		res = ''
		for c in str:
			if self.isNorm(c):
				res += c
		return res
	
	def isNorm(self, c):
		return c.isalpha() or c.isdigit() or c.isspace()
	
	def getLoc(self, arrloc):
		ne = ''
		for e in arrloc:
			ne = self.normalize(e).strip().lower()
			#ae = ne.split()
		return ne
	
	def isFuzzyEqual(self, _s1, _s2, SubtokenLength=3):
		s1 = self.getLoc([_s1])
		s2 = self.getLoc([_s2])
		eqCount = 0
		usedTokens = [False]*(len(s2)-SubtokenLength+1)
		for i in range(0, len(s1) - SubtokenLength + 1):
			subtokenFirst = s1[i:i+SubtokenLength]
			for j in range(0, len(s2) - SubtokenLength + 1):
				if not usedTokens[j]:
					subtokenSecond = s2[j:j+SubtokenLength]
					if subtokenFirst == subtokenSecond:
						#print(subtokenFirst ,' ', subtokenSecond)
						eqCount+=1
						usedTokens[j] = True;
						break;
					
				
		subtokenFirstCount = len(s1) - SubtokenLength + 1;
		subtokenSecondCount = len(s2) - SubtokenLength + 1;
		tanimoto = (1.0 * eqCount) / (subtokenFirstCount + subtokenSecondCount - eqCount);
		
		eq = 0
		if self.ThresholdWord <= tanimoto:
			eq = 1
		resultValue = (1.0 * eq) / (2 - eq)
		#print(s1, s2, resultValue, eqCount)
		return resultValue
			
l = Location(0.6)

#l.isFuzzyEqual("Ostrov Morskaya Chapura", "People’s Republic ofChina", 3)


import nltk.data
from dictionary import refWords, Coves, Seas, Bays, Islands
from run import NERExtractor
import codecs

locmap = {}
locmap.update(Coves)
locmap.update(Seas)
locmap.update(Bays)
locmap.update(Islands)

txt = ""
with open('53.txt', encoding='utf-8') as f:
  for line in f:
    txt += line
	
tokenizer = nltk.data.load('data/tokenizers/english.pickle')
sents = tokenizer.tokenize(txt)

extractor = NERExtractor()
candidates = []

for s in sents:
	ls = s.lower()
	for w in refWords:
		if ls.find(w) != -1:
			candidates.append(s)
			break

OUTfile = codecs.open("outsloc.txt", "w", "utf-8")
OUTLOCfile = codecs.open("outsloccoord.txt", "w", "utf-8")
for sentence in candidates:
	wordsRaw, preds = extractor.extractFromSentence(sentence)
	test = False
	res = ""
	for i, w in enumerate(wordsRaw):
		if preds[i] == "I-LOC" or preds[i] == "B-LOC":
			test = True
			res += w + ' '# + ' {' + preds[i] + '} '
			continue
		else:
			if w == 'of' and res != '':
				res += w + ' '
			else:
				test = False
		res = res.strip()
		if not test and res != '':
			# get coords Coves, Seas, Bays, Islands
			for key in locmap:
				if l.isFuzzyEqual(res, key, 3):
					r = key + ' ' + ''.join(str(x)+', ' for x in locmap[key]) + '\n'
					#print(key + ' - ' + res)
					OUTLOCfile.write(r)
					break
			res += "\n---------------\n"
			OUTfile.write(res)
			res = ''
OUTfile.close()
OUTLOCfile.close()

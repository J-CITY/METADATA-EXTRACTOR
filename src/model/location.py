
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
			
	def w(self, c1, c2, eps=False):
		if eps:
			return 1
		if c1 == c2:
			return 0
		else:
			return 1
		
	def VangerFisher(self, _s1, _s2, maxTransform=3):
		s1 = self.getLoc([_s1])
		s2 = self.getLoc([_s2])
		d = [[0 for i in s2] for i in s1]
		for i in range(1, len(s1)):
			d[i][0] = d[i-1][0] + self.w(s1[i], s1[i], eps=True)
		for i in range(1, len(s2)):
			d[0][i] = d[0][i-1] + self.w(s2[i], s2[i], eps=True)
			
		for i in range(1, len(s1)):
			for j in range(1, len(s2)):
				d[i][j] = min(
					[d[i-1][j]+self.w(s1[i],s1[i],eps=True),
					d[i][j-1]+self.w(s2[j],s2[j],eps=True),
					d[i-1][j-1]+self.w(s1[i],s2[j])])
		#for _d in d:
		#	print(_d)
		
		ans = d[len(s1)-1][len(s2)-1]
		if ans <= maxTransform:
			return True
		return False
		
#l = Location(0.6)
##print(l.VangerFisher('Morskaya', 'Morskoy'))
##l.isFuzzyEqual("Ostrov Morskaya Chapura", "People’s Republic ofChina", 3)
#
#
#import nltk.data
#from dictionary import refWords, Coves, Seas, Bays, Islands
#from run import NERExtractor
#import codecs
#
#locmap = {}
#locmap.update(Coves)
#locmap.update(Seas)
#locmap.update(Bays)
#locmap.update(Islands)
#
#txt = ""
#with open('53.txt', encoding='utf-8') as f:
#  for line in f:
#    txt += line
#	
#tokenizer = nltk.data.load('data/tokenizers/english.pickle')
#sents = tokenizer.tokenize(txt)
#
#extractor = NERExtractor()
#candidates = []
#
#for s in sents:
#	ls = s.lower()
#	for w in refWords:
#		if ls.find(w) != -1:
#			candidates.append(s)
#			break
#
#OUTfile = codecs.open("outslocvf.txt", "w", "utf-8")
#OUTLOCfile = codecs.open("outsloccoordvf.txt", "w", "utf-8")
#for sentence in candidates:
#	wordsRaw, preds = extractor.extractFromSentence(sentence)
#	res = ""
#	for i, w in enumerate(wordsRaw):
#		if preds[i] == "I-LOC" or preds[i] == "B-LOC":
#			res += w + ' '# + ' {' + preds[i] + '} '
#			continue
#		else:
#			if w == 'of' and res != '':
#				res += w + ' '
#				continue
#		res = res.strip()
#		if res != '':
#			# get coords Coves, Seas, Bays, Islands
#			for key in locmap:
#				#if l.VangerFisher(res, key, 1):
#				if l.isFuzzyEqual(res, key, 3):
#					r = key + ' ' + ''.join(str(x)+', ' for x in locmap[key]) + '\n'
#					print(key + ' - ' + res)
#					OUTLOCfile.write(r)
#					break
#			res += "\n---------------\n"
#			OUTfile.write(res)
#			res = ''
#OUTfile.close()
#OUTLOCfile.close()

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

k = KeywordExtractor(['The', 'a', 'in'], "!.?")
test(k._filter(['It is a good sea.']), ['It is a good sea.'])
test(k._filter(['It is a good day.']), [])

k.extractKeyWords('It is a good sea.')
ans = k.getRankedPhrases()
test(ans, ['it is', 'good sea'])
k.extractKeyWordsFromSentences(['It is good sea.'])
ans = k.getRankedPhrases()
test(ans, ['it is good sea'])

test(k._genPhrases(['It is good sea.']), {('it', 'is', 'good', 'sea')})
test(k._getPhraseWords({('it', 'is', 'good', 'sea')}), [(('it', 'is', 'good', 'sea'),)])
k._calcFrequency({('it', 'is', 'good', 'sea')})
test(k.frequency, Counter({'is': 1, 'it': 1, 'good': 1, 'sea': 1}))
k._calcWordGraph({('it', 'is', 'good', 'sea')})
k._calcRank({('it', 'is', 'good', 'sea')})
test(k.rankedPhrases,['it is good sea'])

import codecs
import re
txt = """
This publication includes reports given at a workshop on “Conditions promoting Pseudo-nitzschia events in the eastern Pacific but not the western Pacific” co-convened by Drs. Vera L. Trainer (USA) and Polina Kameneva (Russia) on November 3, 2016 at the PICES 2016 Annual Meeting in San Diego, USA (see Appendix 2). The workshop was focused on the diatom, Pseudo-nitzschia, historically associated with dramatic negative impacts on the economy of shellfish harvests, the well-being of  marine life and human health in the northeastern Pacific PICES member countries (Canada, USA), with little or no impact in the northwestern Pacific (China, Japan, Korea and Russia).  Diatoms of the genus Pseudo-nitzschia (H. Peragallo, 1900) are widely distributed in the plankton assemblages of both coastal and open ocean waters (Hasle et al., 1996; reviewed in Lelong et al., 2012 and Trainer et al., 2012). Nineteen of the 46 currently recognized Pseudo-nitzschia species are known to produce the potent marine neurotoxin, domoic acid (DA; Teng et al., 2016), which can accumulate in fish and shellfish and leads to Amnesic Shellfish Poisoning (ASP) in humans, seabirds and marine mammals when they consume contaminated fish and shellfish (e.g., Lefebvre et al., 2002). It has been suggested that repeated exposure to low levels of DA may cause neuropathic injury to vertebrates, including people (Grattan et al., 2007).  There is clear evidence of contrasting occurrence and impact of the toxin-producing diatom, Pseudonitzschia, between the northwestern and northeastern Pacific. In Canadian and American Pacific waters, numerous cases of toxic Pseudo-nitzschia bloom events and mortalities of sea birds, sea lions, whales, and other marine mammals have been registered from the time of the discovery of DA in 1987 (Bates et al., 1989) up to the present day. In 2015, a massive bloom spanning from California to Alaska, linked to anomalously warm ocean conditions associated with both El Niño and the Pacific Decadal Oscillation (PDO cycles), had major impacts on the economic viability of the shellfish industry and on marine life health (McCabe et al., 2016). In contrast, Pseudo-nitzschia did not cause significant economic losses in the northwestern Pacific in 2015. Gathered data provide a unique opportunity to make East–West Pacific comparisons, and to identify and rank those environmental factors which promote Pseudo-nitzschia success as a harmful algae species. Special attention should be paid to the climate-driven environmental changes such as ocean acidification, warming of the sea surface, stratification pattern changes, and the availability of nutrients to definitively characterize those factors promoting toxic blooms. The recent PICES-supported symposium on HABs and Climate Change (May 19–22, 2015 Göteburg, Sweden) and the related synthesis paper (Wells et al., 2015) emphasize the importance of studying such extreme events to further our understanding of climate impacts on toxic blooms.
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


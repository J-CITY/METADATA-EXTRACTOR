import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
	
from model.reference import ExtracrReference
from collections import Counter, defaultdict

def test(expect, output):
	if expect == output:
		print("OK")
	else:
		print("ERR", expect, " ", output)

r = ExtracrReference('')
r.text = 'Nagata, Y. and Lobanov, V.B. (Eds.) 1998.  Multilingual Nomenclature of Place and Oceanographic Names in the Region of the Okhotsk Sea.  PICES Sci. Rep. No. 8, 57 pp.'
test(r.extract(), ['Nagata, Y. and Lobanov, V.B. (Eds.) 1998.  Multilingual Nomenclature of Place and Oceanographic Names in the Region of the Okhotsk Sea.  PICES Sci. Rep. No. 8, 57 pp.--'])

r.text = 'Nagata, Y. and Lobanov, V.B. (Eds.)  Multilingual Nomenclature of Place and Oceanographic Names in the Region of the Okhotsk Sea.  PICES Sci. Rep. No. 8, 57 pp.'
test(r.extract(), [])

r.text = 'oweroejwrjwol'
test(r.extract(), [])




import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
	
from model.title import extractTitle
from collections import Counter, defaultdict

def test(expect, output):
	if expect == output:
		print("OK")
	else:
		print("ERR", expect, " ", output)

test(extractTitle('PICES SCIENTIFIC REPORT No. 9, 2020 Some report. '), 'PICES SCIENTIFIC REPORT No. 9, 2020 Some report. \n')
test(extractTitle('dasda 2312 asd PICES SCIENTIFIC REPORT No. 9, 2020 Some report. \n \ndawdad af '), 'PICES SCIENTIFIC REPORT No. 9, 2020 Some report. \n')
test(extractTitle('wertyuikxcvbn1qerty dyudtaut6tdaw76d'), '')

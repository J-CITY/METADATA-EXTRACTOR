import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
	
from converter.preferences import Preferences
from collections import Counter, defaultdict

def test(expect, output):
	if expect == output:
		print("OK")
	else:
		print("ERR", expect, " ", output)

p = Preferences("in")

p.setPref("a", "b", "c")
p.setPref("a", "d", "e")
test(p.getPref("a", "b"), "c")
test(p.getPref("a", "d"), "e")
test(p.getPref("d", "d"), "")

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
	
from model.location import Location

def test(expect, output):
	if expect == output:
		print("OK")
	else:
		print("ERR", expect, " ", output)

l = Location(0.5)
test(l.isNorm('a'), True)
test(l.isNorm(' '), True)
test(l.isNorm('1'), True)
test(l.isNorm(')'), False)
test(l.normalize('It is a good day.'),'It is a good day')
test(l.getLoc(['It is a good day.']),'it is a good day')
test(l.isFuzzyEqual('It is a good day.', 'It is a good night.'),1.0)
test(l.isFuzzyEqual('It is a good day.', 'It is a bad night.'),0.0)
test(l.VangerFisher('Morskaya', 'Morskoy'), True)
test(l.VangerFisher('Morskaya', 'Mars'), False)

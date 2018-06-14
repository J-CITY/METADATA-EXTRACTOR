import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
	
from model.utils.utils import getDictionary, getCharDictionary, padSequences, getChunkType,getChunks
from collections import Counter, defaultdict

def test(expect, output):
	if expect == output:
		print("OK")
	else:
		print("ERR", expect, " ", output)


test(getDictionary([[["a", "ta"], ["b","tb"], ["c","ta"]]]), ({'a', 'c', 'b'}, {'a', 'b', 't'}))
test(getCharDictionary([["a", "ta"], ["b","tb"], ["a","ta"]]), {'b', 'a'})
test(padSequences(["a", "ab","aaa"], 0), ([['a', 0, 0], ['a', 'b', 0], ['a', 'a', 'a']], [1, 2, 3]))
test(getChunkType(1, {1 : "I-ORG"}), ('I', 'ORG'))
test(getChunks([0,1,0], {"a":0, "b":1, "O":-1}), [('a', 0, 1), ('b', 1, 2), ('a', 2, 3)])


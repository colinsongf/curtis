import re
import numpy as np
import nltk
from numpy.lib.recfunctions import merge_arrays

def createVariableRegexes(definition):
	parsers = []
	cursor=0
	results=re.finditer(r"<VAR:[\w]+>",definition);
	for r in results:
		if (len(parsers)>0):
			parsers[len(parsers)-1][2] = definition[cursor:r.start()] #update previous item to end at new variable
		name = r.group(0)[r.group(0).index(":")+1:r.group(0).index(">")]
		parsers.append([name,definition[cursor:r.start()],definition[r.end():]])
		cursor=r.end()
	return parsers



def extractChunk(src, regStart, regEnd):
	startPosition=re.search(regStart,src)
	if (startPosition):
		startPosition=startPosition.end()
	else:
		startPosition=0
	if (regEnd == ""):
		endPosition=None
	else:
		endPosition	 =re.search(regEnd,src[startPosition:])
		if (endPosition):
			if ((endPosition.start()==0) and (endPosition.end()==0)):
				endPosition=None
			else:
				endPosition=endPosition.start()+startPosition
		else:
			endPosition=None
	return src[startPosition:endPosition]
	
	
def updateFrequenciesForRow(tokens,rowNum,ndMat):
	if ((len(ndMat)!=0) and (len(ndMat)<=rowNum)):
		ndMat = np.resize(ndMat,rowNum+1)
		ndMat[rowNum]=np.zeros(len(ndMat[rowNum]))
	for tok in tokens:
		if ((len(ndMat)==0) or (tok not in ndMat.dtype.names)):
			ndMat=addTermToMatrix(tok,ndMat)
		ndMat[rowNum][tok]+=1
	return ndMat

def classifyTokensWithMatrix(tokens,ndMat):
	#returns index of row that the supplied tokens most closely match
	#distance used is angle between vectors.
	classification=None
	classificationDistance=7 #start with something very high, greater than 2pi
	names = list(ndMat.dtype.names)
	vector = np.zeros(len(names),dtype='i8')
	for tok in tokens:
		if (tok in names):
			vector[names.index(tok)] += 1
	for rowNum in range(0,len(ndMat)):
		row=ndMat[rowNum]
		currentAngle=angleBetween(np.asarray(list(row)),vector)
		if (currentAngle<classificationDistance):
			classification=rowNum
			classificationDistance=currentAngle
	return classification

def addTermToMatrix(term,ndMat):
	rows = len(ndMat)
	if (rows == 0):
		rows=1
	newfield = np.zeros((rows,1),dtype=[(term,'i8')])
	newarr = merge_arrays([ndMat,newfield],flatten=True)
	if ('f0' in newarr.dtype.names): 
		#this clears up the first column if the array started as 0x0
		#newarr.dtype.names is a tuple, needs to be a list for remove
		names=list(newarr.dtype.names)
		names.remove('f0')
		newarr=newarr[names]
	return newarr

def angleBetween(v1,v2):
	#computes angle between two vectors in radians
	#requires numpy as np for trig and vector ops
	return np.arccos(np.vdot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))


def buildMatrix(classes):
	mat = np.zeros(0)
	mat = updateFrequenciesForRow("what is the price of what is the cost for whats how much does cost how much is".split(" "),classes.index("price"),mat)
	mat = updateFrequenciesForRow("how many people are in whats the population of what is".split(" "),classes.index("population"),mat)
	mat = updateFrequenciesForRow("schedule a meeting wtih schedule time with book time setup set up for on".split(" "),classes.index("schedule"),mat)
	mat = updateFrequenciesForRow("what can you do what can I do what do you know how to do what can ask".split(" "),classes.index("help"),mat)
	return mat
import re

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

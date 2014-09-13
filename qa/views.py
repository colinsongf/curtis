from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,JsonResponse
from qa.nlp import *
import nltk
import re

def index(request):
	return render_to_response("homepage.html")

def question(request,qtext):
	#setup
	types={'price':{'name':'price','action':'getPrice','definitions':[r"how much (is|does|for) (the|an|a)?<VAR:object>(cost)?",r"what(\sis|s|'s) the (cost|price) (of|for) (a\s|an\s)?<VAR:object>"]},'schedule':{'name':'schedule','action':'scheduleMeeting','definitions':[r"(set up|setup|schedule|book|create) ((a|an) )?(meeting|appointment|event|time) with <VAR:person>\b(for|on|at)\b<VAR:time>"]},'population':{'name':'population','action':'populationLookup','definitions':[r".*(population of) <VAR:place>",r".*in <VAR:place>"]}}
	
	#tokenize... questionTokens = nltk.word_tokenize(qtext)
	#then classify...
	classList=["price","population","schedule"]
	classificationMatrix = buildMatrix(classList)
	#className=classify(qtext)
	toks = qtext.split(" ")
	#className = classList[classifyTokensWithMatrix(nltk.word_tokenize(qtext),classificationMatrix)]
	className = classList[classifyTokensWithMatrix(toks,classificationMatrix)]
	if (className is None):
		return HttpResponse("Couldn't classify.")
	currentClass=types[className]
	return JsonResponse(processTextForType(qtext,currentClass))

def classify(text):
	#this is dumb right now, just checking for certain words
	if (re.match(r".*(much|price|cost|pay).*",text)):
		return "price"
	elif (re.match(r".*(schedule|setup|set up|book|create).*",text)):
		return "schedule"
	elif (re.match(r".*(how many people|population).*",text)):
		return "population"
	else:
		return None

def processTextForType(text,type):
	#params: source text; dictionary containing name, action, and definitions for matched type
	#returns JSON object with requested chunks.
	chunks=[]
	matchFound=False
	definitions=type['definitions']
	for definition in definitions:
		matchRegexpDef = re.sub(r"<VAR:\w+>",r".*",definition)
		if (re.search(matchRegexpDef,text)):
			matchFound=True
			regexps = createVariableRegexes(definition)
			for i in range(0,len(regexps)):
				value = extractChunk(text,regexps[i][1],regexps[i][2])
				chunks.append([regexps[i][0],value])
			if (matchFound):
				break
	if (matchFound):
		return DictifyChunks(chunks)
	else:
		return dict()

def DictifyChunks(chunks):
	d = dict()
	for chunk in chunks:
		d[chunk[0]]=chunk[1]
	return d

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from qa.nlp import *

import re

def index(request):
	return HttpResponse("Good afternoon!")

def question(request,qtext):
	#setup
	types={'price':{'name':'price','action':'getPrice','definitions':[r"how much (is|does|for) (the|an|a)?<VAR:object>(cost)?",r"what(\sis|s) the (cost|price) (of|for) (a\s|an\s)?<VAR:object>"]},'schedule':{'name':'schedule','action':'scheduleMeeting','definitions':[r"(set up|setup|schedule|book|create) ((a|an) )?(meeting|appointment|event|time) with <VAR:person>\b(for|on|at)\b<VAR:time>"]}}
	
	#tokenize... questionTokens = nltk.word_tokenize(qtext)
	#then classify...
	className=classify(qtext)
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
		if (re.match(matchRegexpDef,text)):
			matchFound=True
			regexps = createVariableRegexes(definition)
			for var in regexps:
				value = extractChunk(text,regexps[0][1],regexps[0][2])
				chunks.append([regexps[0][0],value])
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

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,JsonResponse
from qa.nlp import *
from qa.actions import *
import nltk
import re

def index(request):
	return render_to_response("homepage.html")

def question(request,qtext):
	#setup
	types={'price':{'name':'price','action':getPrice,'definitions':[r"how much (is|does|for) (the\s|an\s|a\s)?<VAR:object>(cost)?",r"what(\sis|s|'s) the (cost|price) (of|for) (a\s|an\s)?<VAR:object>",r"(of|for) <VAR:object>"]},'schedule':{'name':'schedule','action':scheduleMeeting,'definitions':[r"(set up|setup|schedule|book|create) ((a|an) )?(meeting|appointment|event|time) with <VAR:person>\b(for|on|at)\b<VAR:time>"]},'population':{'name':'population','action':populationLookup,'definitions':[r".*(population of) <VAR:place>",r".*in <VAR:place>"]},'help':{'name':'help','action':help,'definitions':[]}}
	#tokenize... questionTokens = nltk.word_tokenize(qtext)
	#then classify...
	classList=["price","population","schedule","help"]
	classificationMatrix=buildMatrix(classList)
	toks = qtext.split(" ")
	className = classList[classifyTokensWithMatrix(toks,classificationMatrix)]
	if (className is None):
		return HttpResponse("Couldn't classify.")
	currentClass=types[className]
	args = processTextForType(qtext,currentClass)
	return HttpResponse(currentClass['action'](args))
	#return JsonResponse(processTextForType(qtext,currentClass))




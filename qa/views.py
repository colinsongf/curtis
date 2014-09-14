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
	response = currentClass['action'](args)
	return HttpResponse(response)
	#return JsonResponse(processTextForType(qtext,currentClass))




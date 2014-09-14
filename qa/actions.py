def getPrice(args):
	if ("object" not in args):
		return "I'm not sure what price I'm supposed to be looking for"	
	else:
		return "Now I would do a price check on "+args["object"]

def populationLookup(args):
	if ("place" not in args):
		return "Can you rephrase? I'm not sure what population you're looking for."
	else:
		return "There are N people in "+args["place"]
	
def scheduleMeeting(args):
	if (("person" not in args) and ("time" not in args)):
		return "I'm not sure who you want to meet with or when. Can you rephrase?"
	elif ("person" not in args): 
		return "I'll set up something for "+args["time"]
	elif ("time" not in args):
		return "I'll set up something with "+args["person"]
	else:
		return "I'll set up something with "+args["person"] + " for "+args["time"]
	
def help(args):
	return "You can ask me about prices, populations, for a phone number, or to schedule a meeting"

def greetings(args):
	return "Hello again!"
	
def phoneNumber(args):
	if ("person" not in args):
		return "Whose number are you looking for?"
	else:
		return args["person"]+"'s number is 555-555-5555"

types={'price':{'name':'price','action':getPrice,'definitions':[r"how much (is|does|for) (the\s|an\s|a\s)?<VAR:object>(cost)?",r"what(\sis|s|'s) the (cost|price) (of|for) (a\s|an\s)?<VAR:object>",r"(of|for) <VAR:object>"]},'schedule':{'name':'schedule','action':scheduleMeeting,'definitions':[r"(set up|setup|schedule|book|create) ((a|an) )?(meeting|appointment|event|time) with <VAR:person>\b(for|on|at)\b<VAR:time>",r"(set up|setup|schedule|book|create) ((a|an) )?(meeting|appointment|event|time) with <VAR:person>"]},'population':{'name':'population','action':populationLookup,'definitions':[r".*(population of) <VAR:place>",r".*in <VAR:place>"]},'help':{'name':'help','action':help,'definitions':[]},'greetings':{'name':'greetings','action':greetings,'definitions':[]},'phone':{'name':'phone','action':phoneNumber,'definitions':[r"number (for|of) <VAR:person>",r"('s|is) <VAR:person>('s)? (phone\s)?number"]}}
classList=["price","population","schedule","help","greetings","phone"]
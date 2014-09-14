def getPrice(args):
	if ("object" not in args):
		return "I'm not sure what price I'm supposed to be looking for"	
	else:
		return "Price check on "+args["object"]

def populationLookup(args):
	if ("place" not in args):
		return "Can you rephrase? I'm not sure what population you're looking for."
	else:
		return "There are 2000 people in "+args["place"]
	
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
	return "You can ask me about prices, populations, or to schedule a meeting"
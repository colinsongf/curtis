def getPrice(args):
	return "Price check on "+args["object"]

def populationLookup(args):
	return "There are 2000 people in "+args["place"]
	
def scheduleMeeting(args):
	return "Your meeting with "+args["person"]+" is on the calendar for "+args["time"]
	
def help(args):
	return "You can ask me about prices, populations, or to schedule a meeting"
##########################################################################################
#Imports
##########################################################################################

#from singleChainv2 import runNMEngine #NOTE: This is from Previous Version of Implemention and is not compatible with new version 
from singleChainRegexParser import runParser

from Bugger import Bugger 
metaBugger = Bugger(False) #Can change this to true for meta runs

from os import system
from os import name as OSName

import huepy as hp
##########################################################################################
#Declrations
##########################################################################################

NMSettings = {	
    "EchoInput": True,
    "SuggestImprovements":False,
	"TripleBondEntryCharacter": '#', # What character you use to enter triple bonds
	"TripleBondDisplayCharacter": '≡', # What character you display triple bonds with; similar looking: ASCII: "÷" '#' '≈' '£' '¥' 'ε' UNICODE: '≡'
	"CommentChar":"//",
	"Debugging":False
}

HelpText = hp.cyan("""Type a condensed organic formula and press enter
 Use right case characters for elements for example C for carbon and H for Hydrogen
 use following symbols for bonds
	minus (-) for single bond, 
	equals (=) for double bond and 
	hash symbol (#) for triple bonds
 
 The Hydrocarbonator internally uses ≡ for triple bond, and if you can manage to type it, that is ok too.
 
 Some example formulae that you could try out..
	CH3-CH3
	CH2=CH2
	CH#CH
	CH3-CH2-C#CH

Use cmds or commands for the list of all commands available
""")

commands = ['cmds','commands','clear','cls','exit','quit','settings','config','help','?','dbg-toggle','dbg']

##########################################################################################
#Command Handling Method Definition
##########################################################################################

def printIUPACResults(condensedFormula, comment, IUPACName):
	global NMSettings
	tbdDisplayChar = NMSettings["TripleBondDisplayCharacter"]
	cFormula = condensedFormula.replace("≡",tbdDisplayChar)
	
	if(NMSettings["EchoInput"]):	
		# print(f"{cFormula} => {IUPACName} {comment}")
		print(f"{hp.italic(hp.lgreen(cFormula))} => {hp.lgreen(IUPACName)} {hp.yellow(comment)}")
	else:
		print(f"{hp.lgreen(IUPACName)} {hp.yellow(comment)}")

def handleNonPNomen(cmdString):
	cmdString = cmdString.lower()	
	if cmdString in ['clear','cls']:
		if OSName == 'nt':
			_ = system('cls')

	if cmdString in ['exit','quit']:
		exit(hp.purple("Bye."))
	
	if cmdString in ['help', '?']:
		print(HelpText)
		
	if cmdString in ['settings','config']:
		print(hp.lightred(NMSettings))

	if cmdString in ['cmds','commands']:
		print(f"The available commands are: {hp.lblue(commands)}")

	if cmdString in ['dbg-toggle','dbg']:
		__ds = NMSettings['Debugging']
		print(f"Current Debug State is {hp.orange(__ds)} ")
		print(f"Setting it to {hp.green(not __ds)} ")
		NMSettings['Debugging'] = not __ds

##########################################################################################
#Main
##########################################################################################

while 1:
	text = input("NM => ")

	if text in commands:
		handleNonPNomen(text)

	elif '\n' in text: #Handle Just Enter
		continue

	elif ' \n' in text: #Handle Just Enter
		continue

	else:
		comment=''
		commentChar = NMSettings["CommentChar"]
		condensedFormula=text
		if commentChar in text: #Comment Handling
			comment = text[text.index(commentChar)::]
			condensedFormula = text[:text.index(commentChar)]

		#we have built the unicode char '≡' to represent triple bonds in our parser
		#however the unicode character is hard to type, but if the user managed to type it, it is ok
		#otherwise, we give an easy option to type a # as input instead of the more difficult unicode char
		__entryChar = NMSettings["TripleBondEntryCharacter"]
		cFormula = condensedFormula.replace(__entryChar,"≡",condensedFormula.count(__entryChar))
		metaBugger.log(f"Debugging state parser is {hp.under(NMSettings['Debugging'])}")
		IUPACName, err = runParser(cFormula,NMSettings['Debugging'])

		if err: 
			metaBugger.print(cFormula)
			# print(err.stringify())
			print(hp.under(hp.red(err.stringify())))
		else:
			metaBugger.print(cFormula)
			printIUPACResults(cFormula, comment, IUPACName)
##########################################################################################
#Imports
##########################################################################################

from singleChainv2 import runNMEngine
from singleChainRegexParser import runParser

from Bugger import Bugger 
metaBugger = Bugger(False) #Can change this to true for meta runs

from os import system
from os import name as OSName

##########################################################################################
#Declrations
##########################################################################################

NMSettings = {	
    "EchoInput": True,
    "SuggestImprovements":False,
	"DefaultTBDDisplayChar": '≡', # Fixed by engine; do not allow edit
	"TripleBondDisplayCharacter": '≡', # similar looking: SAFE: '~' ASCII: "÷" '#' '≈' '£' '¥' 'ε' UNICODE: '≡'
	"UseHashForTripleBonds": False,
	"CommentChar":"//",
	"Debugging":False
}

HelpText = """Type an condensed organic formula and press enter
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
"""

commands = ['cmds','commands','clear','cls','exit','quit','settings','config','help','?','dbg-toggle']

##########################################################################################
#Command Handling Method Definition
##########################################################################################

def printIUPACResults(condensedFormula, comment, IUPACName):
	tbdDisplayChar = NMSettings["TripleBondDisplayCharacter"]
	tbdDefaultChar = NMSettings["DefaultTBDDisplayChar"]
	cFormula = condensedFormula.replace(tbdDefaultChar,tbdDisplayChar)
	
	if(NMSettings["EchoInput"]):	
		print(f"{cFormula} = {IUPACName} {comment}")
	else:
		print(f"{IUPACName} {comment}")

def handleNonPNomen(cmdString):
	cmdString = cmdString.lower()	
	if cmdString in ['clear','cls']:
		if OSName == 'nt':
			_ = system('cls')

	if cmdString in ['exit','quit']:
		exit("Exiting...")
	
	if cmdString in ['help', '?']:
		print(HelpText)
		
	if cmdString in ['settings','config']:
		print(NMSettings)

	if cmdString in ['cmds','commands']:
		print(f"The available commands are: {commands}")

	if cmdString in ['dbg-toggle']:
		__ds = NMSettings['Debugging']
		print(f"Current Debug State is: {__ds} ")
		print(f"Setting it to: {not __ds} ")
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
		cFormula = condensedFormula.replace('#',"≡",condensedFormula.count('#'))
		metaBugger.log(f"Debugging State of nm engine is {NMSettings['Debugging']}")
		IUPACName, err = runParser(cFormula,NMSettings['Debugging'])

		if err: 
			print(err.stringify())
		else: 
			printIUPACResults(cFormula, comment, IUPACName)
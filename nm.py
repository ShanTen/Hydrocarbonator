from singleChainv2 import runNMEngine
from singleChainRegexParser import runParser

from os import system
from os import name as OSName

NMSettings = {	
    "EchoInput": True,
    "SuggestImprovements":False,
	"DefaultTBDDisplayChar": '≡', # Fixed by engine; do not allow edit
	"TripleBondDisplayCharacter": '≡', # similar looking: SAFE: '~' ASCII: "÷" '#' '≈' '£' '¥' 'ε' UNICODE: '≡'
	"UseHashForTripleBonds": False,
	"CommentChar":"'"	
}

HelpText = """Type an condensed organic formula and press enter
 Use right case characters for elements for example C for carbon and H for Hydrogen
 use following symbols for bonds
	minus (-) for single bond, 
	equals (=) for double bond and 
	hash symbol (#) for triple bonds
 
 The Nomenclature machine internally uses ≡ for triple bond, and if you can manage to type it, that is ok too.
 
 Some example formulae that you could try out..
	CH3-CH3
	CH2=CH2
	CH#CH
	CH3-CH2-C#CH
	"""

commands = ['clear','cls','exit','quit','settings','config','help','?']

def printIUPACResults(condensedFormula, comment, IUPACName):
	tbdDisplayChar = NMSettings["TripleBondDisplayCharacter"]
	tbdDefaultChar = NMSettings["DefaultTBDDisplayChar"]
	cCount = condensedFormula.count(tbdDefaultChar)
	#print(f"DBG: BEFORE {condensedFormula} count{cCount} occurances dispChar {tbdDisplayChar}")
	cFormula = condensedFormula.replace(tbdDefaultChar,tbdDisplayChar)
	#print(f"DBG: AFTER{cFormula}")
	
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
		
	if (cmdString) in ['settings','config']:
		print(NMSettings)


while 1:
	text = input("NM >> ")

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

		#we have built the unicode char '≡' to reprresent triple bonds in our parser
		#however the unicode character is hard to type, but if the user managed to type it , it is ok
		#otherwise, we give an easy option to type a # as input instead of the more difficult unicode char
		cFormula = condensedFormula.replace('#',"≡",condensedFormula.count('#'))

		# IUPACName, err = runNMEngine(cFormula)
		IUPACName, err = runParser(cFormula) 

		if err: 
			print(err.stringify())
		else: 
			printIUPACResults(cFormula, comment, IUPACName)

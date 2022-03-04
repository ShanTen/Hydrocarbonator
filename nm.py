##########################################################################################
#Imports
##########################################################################################

#from singleChainv2 import runNMEngine #NOTE: This is from Previous Version of Implemention and is not compatible with new version 
from asyncore import read
from singleChainRegexParser import runParser

from Bugger import Bugger 
metaBugger = Bugger(False) #Can change this to true for meta runs

from os import system
from os import name as OSName

import huepy as hp
import pickle as pic

##########################################################################################
#Declrations
##########################################################################################

NMSettings = {	
    "EchoInput": True,
    "SuggestImprovements":False,
	"TripleBondEntryCharacter": '#', # What character you use to enter triple bonds
	"TripleBondDisplayCharacter": '≡', # What character you display triple bonds with; similar looking: ASCII: "÷" '#' '≈' '£' '¥' 'ε' UNICODE: '≡'
	"CommentChar":"//",
	"UpdateCacheAfterEachRun":False, #Set to True if you want to update cache after every single run instead of during exit.
	"Debugging":False #For NM engine, to debug nm.py use meta bugger.
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

commands = ['cmds','commands','clear','cls',
	'exit','quit','settings','config',
	'help','?','dbg-toggle','dbg',
	'show-cache',"display-cache","dc","clear-cache"]

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
	global cacheDict, changedCache
	cmdString = cmdString.lower()	
	if cmdString in ['clear','cls']:
		if OSName == 'nt':
			_ = system('cls')

	if cmdString in ['exit','quit']:
		if changedCache:
			print(hp.blue("Updating cache..."))
			updateCache(cacheDict)
			print(hp.green("Updated cache."))
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

	if cmdString in ['clear-cache']:
		print(hp.info("THIS OPERATION RESETS YOUR CACHE TO BASE, PROCEED WITH CAUTION"))
		resetCache()

	if cmdString in ['show-cache',"display-cache","dc"]:
		print(cacheDict)

##########################################################################################
#Main
##########################################################################################

cacheLocation = "./cache.bin" #Location of cache file (try not to change this name or location)
cacheDict = None
changedCache = False

def updateCache(data): #Choice for updating after each cycle or at the end, Handle EoF errs
	with open(cacheLocation,'rb+') as f:
		pic.dump(data,f)
		f.flush();f.close()

def resetCache():
	global cacheDict, changedCache, cacheLocation
	dec = input(hp.red("ARE YOU SURE YOU WANT TO RESET CACHE? (Y/N): ")).upper()
	if dec in ["Y", "YES"] :
		with open(cacheLocation,'rb+') as f:
			empSet = {"CH4":"Methane"}
			pic.dump(empSet,f)
			f.flush();f.close()
		print(hp.cyan("Cache reset."))
		readCache(); changedCache = True
	else:
		print(hp.cyan("Reset Operation Cancelled."))

def readCache():
	global cacheDict
	with open(cacheLocation,'rb+') as f:
		cacheDict = pic.load(f)
		f.close()

readCache()

while 1:
	try:
		text = input("NM => ")
	except EOFError:
		updateCache(cacheDict)
		metaBugger.log("Updated Cache (EOF ERR)")
		print(hp.blue("Updated Cache if any changed were made."))
		exit(hp.red(f"An EoF Error occurred due to either a bad input (empty input from file) or forced termination of program."))

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
			condensedFormula = text[:text.index(commentChar)].strip() #Remove trailing spaces

		#we have built the unicode char '≡' to represent triple bonds in our parser
		#however the unicode character is hard to type, but if the user managed to type it, it is ok
		#otherwise, we give an easy option to type a # as input instead of the more difficult unicode char
		__entryChar = NMSettings["TripleBondEntryCharacter"]
		cFormula = condensedFormula.replace(__entryChar,"≡",condensedFormula.count(__entryChar))
		metaBugger.log(f"Debugging state parser is {hp.under(NMSettings['Debugging'])}")
		
		if(cFormula.strip() in cacheDict):
			cIUPACNAME = cacheDict[cFormula]
			metaBugger.log("Hitting cache")
			printIUPACResults(cFormula, comment, cIUPACNAME)
			metaBugger.log("Result obtained from from cache.")
		else:
			IUPACName, err = runParser(cFormula,NMSettings['Debugging'])
			
			if NMSettings["UpdateCacheAfterEachRun"]:
				updateCache(cacheDict)
				metaBugger.log("Updated Cache.")

			if err: 
				metaBugger.print(cFormula)
				# print(err.stringify())
				print(hp.under(hp.red(err.stringify())))
			else:
				metaBugger.print(cFormula)
				printIUPACResults(cFormula, comment, IUPACName)
				cacheDict[cFormula.strip()] = IUPACName
				changedCache = True
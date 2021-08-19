##########################################################################################
# Single Chain V2 Brings Hydrogen identification and Proper Element Count Storing by tweaking lexer and parser
##########################################################################################

##########################################################################################
#Lexer
##########################################################################################

from ErrorClass import ErrorClass
from PureHydrocarbons import Hydrocarbon

TknBonds = {
    "SingleBond":"-",
    "DoubleBond":"=",
    "TripleBond":"≡"
}

Tkn_Carbon = "C"
Tkn_Hydrogen = "H"

TknElements = [Tkn_Carbon,Tkn_Hydrogen] #NOTE:Change this to elemental class later + dont do raw entry 

#Types of Values in this code 
TknTypeBond = "BOND"
TknTypeElement = "ELEMENT_NODE"
TknTypeElementCount = "ELEMENT_COUNT"

TknNums = {
    "Meth":1,
    "Eth":2,
    "Prop":3,
    "But":4,
    "Pent":5,
    "Hex":6,
    "Hept":7,
    "Oct":8,
    "Non":9,
    "Dec":10,
    "UnDec":11,
    "DoDec":12,
    "TriDec":13
}

class Token:
    def __init__(self,_tknType,_tknVal,startPos=None,endPos=None):
        self.type = _tknType
        self.value = _tknVal
    
        if startPos:
            self.startPos = startPos.copy()
            self.endPos = startPos.copy()
            self.endPos.advance()

        if endPos:
            self.endPos = endPos

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexer: #End Result should be TokenArr(If any) and Error (If Any)
    def __init__(self,chain):
        self.chain = chain
        self.pos = -1
        self.currentChar = None
        self.advance()

    def advance(self):
        self.pos += 1

        if self.pos < len(self.chain):
            self.currentChar = self.chain[self.pos]
        else:
            self.currentChar = None

    def makeTokens(self):
        tokens = []

        while self.currentChar != None: #While we have a character value in a chain
            
            if self.currentChar in ' \t':
                self.advance()

            elif self.currentChar in TknElements:
                tokens.append(Token(TknTypeElement,self.currentChar))
                self.advance()

            elif self.currentChar.isnumeric() and int(self.currentChar != 0):
                tokens.append(Token(TknTypeElementCount,self.currentChar))
                self.advance()

            elif self.currentChar in TknBonds.values():
                tokens.append(Token(TknTypeBond,list(TknBonds.keys())[list(TknBonds.values()).index(self.currentChar)]))
                self.advance()

            else:#throw invalid character error
                _char_ = self.currentChar
                self.advance()
                _error = IllegalCharacterError(f"Illegal Character --> '{_char_}'")
                return [],_error
    

    #CHANGE TO TYPE BASED
        if tokens == []:
            return "NULL_LINE",None

        if tokens[0].value not in TknElements: #NOTE:You should change this the tokens[0].type != TknTypeElement in later versions
            return None,IllegalTerminalError(tokens[0],"start")

        return tokens,None
#########################################################################################
#NodeMaker:
#########################################################################################

class SimpleNode: #work back on this later

    def __init__(self, carbonCount, hydrogenCount, prevBond=None,nextBond=None):
        self.carbonCount = carbonCount
        self.hydrogenCount = hydrogenCount
        self.prevBond = prevBond #singleDoubletripleNone
        self.nextBond = nextBond #singleDoubletripleNone

##########################################################################################
#Parser:
##########################################################################################

#Need to check carbon count per node and see if it doesnt exceed 1!

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = -1 #POSITION IS THE POSITION IN THE LIST OF TOKENS FED
        self.bondPos = 0
        self.NullLine = False
        self.advance()

    def closestUnsat(self):
        arr = self.tokens
        spl1, spl2 = arr[:-int(len(arr)/2)],arr[int(len(arr)/2):]
        spl1 = [tk.value for tk in spl1]
        spl2 = [tk.value for tk in spl2]
        
        if "DoubleBond" in spl2 or "TripleBond" in spl2: #Fix this later to be cascading in terms of bonds. i,e a cascading order of bonds --> trpl,dbl,sngl
            arr = arr[::-1] #inverting tkn array
        return arr

    def advance(self):
        if self.tokens == "NULL_LINE": #Analyse Nothing
            self.NullLine = True
            return

        self.pos+=1
        if self.pos < len(self.tokens):
            self.currentToken = self.tokens[self.pos]

    def parse(self):
        #Parse Nothing
        if self.NullLine == True:
            return '',None

        #parseResult objeect looks like a mess rn
        parseResult = {"ChainLength":0,"ChainLengthDenotation":'',"BondPosArr":[],"NodalAttachedCount":[]}
        
        _hydrogenWithoutCoeff = 0

        #SCV3
        # self.tokens = self.closestUnsat()
        # print(self.closestUnsat())

        validEndTerminalTypes = [TknTypeElement,TknTypeElementCount]
        if self.tokens[-1].type not in validEndTerminalTypes:
            return None,IllegalTerminalError(self.tokens[-1],"end")

        while self.pos < len(self.tokens):
            tkn = self.currentToken
            #NOTE:For RL config just invert the array ig 
            #A bond can only follow an elemental carbon node and not another bond itself.
            
            #Changed this to chain length wrt to Carbon
            if (tkn.value == Tkn_Carbon):#Some sort of isValidNode() method to be used here in later version 
                parseResult["ChainLength"] += 1

            if(tkn.value == Tkn_Hydrogen and ((self.pos+1 == len(self.tokens)) or (not self.tokens[self.pos+1].value.isnumeric()))):
                _hydrogenWithoutCoeff += 1

            if (tkn.type == TknTypeBond):

                if(self.tokens[self.pos+1].type == TknTypeBond):
                    return {},IllegalBondError("A bond can only follow an elemental carbon node and not another bond itself.")

                self.bondPos += 1 #??

                parseResult["BondPosArr"].append((self.bondPos,
                tkn.value
                ))

            if(tkn.type == TknTypeElementCount): #FIX THIS BAKA

                if(self.tokens[self.pos-1].type != TknTypeElement):
                    return {},IllegalChainError("Count Cannot be assigned to anything other than an Elemental Node.")

                #posOfAttachedElement is the index position of the attached element in the chain of carbons
                parseResult["NodalAttachedCount"].append({"posOfAttachedElement":self.pos-1,"attachedToelement":self.tokens[self.pos-1].value,"count":int(self.currentToken.value)}) 

            self.advance()

        if parseResult["ChainLength"] >= 14:
            return '',IllegalChainError("Single Chain Longer than 13 nodes.")

        parseResult["ChainLengthDenotation"] = list(TknNums.keys())[parseResult["ChainLength"]-1]

        #Making Tweaks to parse results before returning
        totalBondsCount = {'SingleBond':0,'DoubleBond':0,'TripleBond':0}
        
        for bond in parseResult["BondPosArr"]:
            if bond[1] in ['SingleBond','DoubleBond','TripleBond']:
                totalBondsCount[bond[1]] += 1

        def HydrogenWithCoeff():
            hc = 0
            for obj in parseResult["NodalAttachedCount"]:
                if obj["attachedToelement"] == Tkn_Hydrogen:
                  hc += obj["count"]

            return hc
        
        HydrogenCount = HydrogenWithCoeff() + _hydrogenWithoutCoeff

        parsedHydroCarbon = Hydrocarbon(parseResult["ChainLength"], HydrogenCount, totalBondsCount).type

        suffix,err = parsedHydroCarbon #Either result or error

        if(err):
            return '',err
        #pos,val in bondposarr : getting positions of each bond
        
        def getBondPos(_suffix): #returns choice depending on suffix
            for bp in parseResult["BondPosArr"]:

                if _suffix == "Alkene":
                    if bp[1] == "DoubleBond":
                        return bp[0]

                elif _suffix == "Alkyne":
                    if bp[1] == "TripleBond":
                        return bp[0]

        #SCV3
        # print(parseResult["Node"])

        if suffix == "Alkane": 
            return f"n-{parseResult['ChainLengthDenotation']}{suffix[-3:]}",None #NOTE: Adding "ane" to the name 

        elif suffix in ["Alkene","Alkyne"]: 
            bond_pos = getBondPos(suffix) 

            if bond_pos>(parseResult["ChainLength"]-bond_pos):
                bond_pos = parseResult["ChainLength"]-bond_pos #Set bond_pos to lower value


            return f"{parseResult['ChainLengthDenotation']}-{bond_pos}-{suffix[-3:]}",None #NOTE: Adding "ene" or "yne" to the name 

    def __repr__(self):
        pass #Work on making rep look pretty later, too tired now.

##########################################################################################
#Error Sub Classes
##########################################################################################
class IllegalCharacterError(ErrorClass):
    def __init__(self,_errMsg):
        super().__init__("Illegal Character Error",_errMsg)

class IllegalTerminalError(ErrorClass):
    def __init__(self,_terminalChar,_startOrEnd):
        _errMsg = f"Illegal Character '{_terminalChar}' at {_startOrEnd} of chain. Terminal Character Must be a valid elemental node."
        super().__init__("Illegal Terminal Error",_errMsg)

class IllegalBondError(ErrorClass):
    def __init__(self,_errMsg): #A bond can only follow an elemental carbon node and not another bond itself.
        super().__init__("Illegal Bond Error",_errMsg)

class IllegalChainError(ErrorClass):
    def __init__(self,_errMsg):
        super().__init__("Illegal Chain Error",_errMsg)
##########################################################################################
#Run
##########################################################################################

# def test():
#     while 1:
#         inputChain = input(">>> ")
#         lxr = Lexer(inputChain)
#         tkns,_err = lxr.makeTokens()

#         if _err:
#             print(_err)
#             return
#         for t in tkns:
#             print(t.value, end="")
#         print()
# test()

def passTokens(inputChain):
    lxr = Lexer(inputChain)
    tkns,_err = lxr.makeTokens()
    return tkns,_err

def runNMEngine(inputChain):
    lxr = Lexer(inputChain)
    tkns,_err = lxr.makeTokens()
    
    if(_err): return [], _err

    prsr = Parser(tkns)
    # print(prsr.parse())
    prsr_res, prsr_err = prsr.parse()

    if(prsr_err): return {}, prsr_err

    return prsr_res, None

# :)
from ErrorClass import * 
from Bugger import Bugger
import re

#################################################
#Program Convention
#NOTE: for notes
#TODO: For inline features to add
#################################################

##########################################################################################
#Constants
##########################################################################################

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
    "TriDec":13,
    "tetradec": 14,	
    "pentadec":15,
    "hexadec": 16,
    "heptadec": 17,
    "octadec": 18,
    "nonadec": 19,
    "icos": 20  
}

#NOTE: used based off number of double bonds and triple bonds
IUPACmultipliers = {
    1  : "", #mono
    2  : "di", 
    3  : "tri", 
    4  : "tetr", 
    5  : "pent", 
    6  : "hex", 
    7  : "hept", 
    8  : "oct", 
    9  : "non", 
    10 : "dec", 
    11 : "undec", 
    12 : "dodec",
    13 :"tridec",
    14 :"tetradec",
    15 :"pentadec",
    16 :"hexadec",
    17 :"heptadec",
    18 :"octadec",
    19 :"nonadec",
    20 :"icosa"
}

max_chain_len = 20

##########################################################################################
#Error Sub Classes
##########################################################################################
class IllegalNodeError(ErrorClass):
    def __init__(self,_errMsg):
        super().__init__("Illegal Node Error",_errMsg)

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
#Lexer
##########################################################################################
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
        self.pos += 1 #basically the index

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

##########################################################################################
#Naming Class
##########################################################################################

chainDebugger = Bugger()

class NameClass:

    global chainDebugger

    def __init__(self, parseObj):
        self.parseObj = parseObj
        self.satType = None
        self.satOrder = None
        self.rev = False
        self.name = ''


    def nameChain(self): #Identify if Alkane, Alkene, Alkyne

        bondsArr = self.parseObj["BondArr"]
        get_indexes = lambda __lst,__item : [__i for __i, __x in enumerate(__lst) if __x == __item]
        global IUPACmultipliers

        tripleBondCount = 0
        trplBondIndexes = []

        doubleBondCount = 0
        dblBondIndexes = []

        totalBondsCount = self.parseObj["CarbonCount"]-1

        trplBondIndexes = get_indexes(bondsArr,"TripleBond")
        dblBondIndexes = get_indexes(bondsArr,"DoubleBond")

        doubleBondCount = len(dblBondIndexes)
        tripleBondCount = len(trplBondIndexes)

#################################New Implementation#################################################
        #Always pref to name dbl bonds 
        self.name += f"{self.parseObj['ChainLengthDenotation']}"
        if not dblBondIndexes and not trplBondIndexes:
            self.satType = "Alkane"
            nfix = ""
            if self.parseObj['CarbonCount'] > 3: nfix = "n-"
            self.name = f"{nfix}{self.name}{self.satType[-3:]}"

        if dblBondIndexes:
            
            self.satType = "Alkene"
            dbl_reversed_indices = [len(bondsArr)-n for n in dblBondIndexes[::-1]]
            dblBondIndexes = [di+1 for di in dblBondIndexes]
            
            if sum(dbl_reversed_indices) <= sum(dblBondIndexes):
                self.rev = True
                self.name += f"-{dbl_reversed_indices}-{IUPACmultipliers[doubleBondCount]}{self.satType[-3:]}"
            else:
                self.name += f"-{dblBondIndexes}-{IUPACmultipliers[doubleBondCount]}{self.satType[-3:]}"

        if trplBondIndexes:

            self.satType = "Alkyne"
            trpl_reversed_indices = [len(bondsArr)-n for n in trplBondIndexes[::-1]]
            trplBondIndexes = [ti+1 for ti in trplBondIndexes]

            if dblBondIndexes: #deffo double bond 
                if self.rev:
                    self.name += f"-{trpl_reversed_indices}-{IUPACmultipliers[tripleBondCount]}{self.satType[-3:]}"
                else:
                    self.name += f"-{trplBondIndexes}-{IUPACmultipliers[tripleBondCount]}{self.satType[-3:]}"
            else:
                if sum(trpl_reversed_indices) <= sum(trplBondIndexes):
                    self.rev = True
                    self.name += f"-{trpl_reversed_indices}-{IUPACmultipliers[tripleBondCount]}{self.satType[-3:]}"
                else:
                    self.name += f"-{trplBondIndexes}-{IUPACmultipliers[tripleBondCount]}{self.satType[-3:]}"

#####################################################################################################

        chainDebugger.print(f"Parse Object: {self.parseObj}")
        return

##########################################################################################
#Simple Node Class
##########################################################################################

class SimpleNode: #work back on this later

    def __init__(self, carbonCount, hydrogenCount, prevBond=None,nextBond=None):
        
        self.carbonCount = carbonCount
        self.hydrogenCount = hydrogenCount
        self.prevBond = prevBond #singleDoubletripleNone
        self.nextBond = nextBond #singleDoubletripleNone

    def isValidNode(self):
        #NOTE: Based off attributes 
        carbonComp = 4
        hydrogenComp = -1 
        pbv = 0
        nbv = 0
        valDict = {
            "SingleBond":-1,
            "DoubleBond":-2,
            "TripleBond":-3
        }
        if self.prevBond != None:
            pbv = valDict[self.prevBond]
        if self.nextBond != None:
            nbv = valDict[self.nextBond]

        nodeSum = carbonComp + (self.hydrogenCount*hydrogenComp) + (nbv+pbv)

        if nodeSum < 0:
            return False, f"Too Many Hydrogen Atoms! ({self.hydrogenCount} atoms)"
        
        if nodeSum > 0:
            return False, f"Too Few Hydrogen Atoms! ({self.hydrogenCount} atoms)"

        return True, ""

    def __repr__(self):
        brp, brn = self.prevBond,self.nextBond #NOTE: Bond rep prev, bond rep next
        
        if not self.prevBond: brp = ''
        else: brp = TknBonds[brp]

        if not self.nextBond: brn = ''
        else: brn = TknBonds[brn]
        
        return f"{brp}CH{self.hydrogenCount}{brn}"

##########################################################################################
#Chad Regex parser
##########################################################################################

class RegexParser:

    global max_chain_len

    def __init__(self,tokensArr):
        self.NullLine = False
        self.rawTokens = tokensArr
        
        if tokensArr == "NULL_LINE": #Analyse Nothing
            self.NullLine = True
            return

        self.tokens = [tok.value for tok in tokensArr]

    def evaluate(self):

        if self.NullLine:
            return '',''

        def generatePrevBondNextBond(bonds): #NOTE: I outsourrced this to a seperate funtion so that during inversion I only have to make one function call
            totalBondSet = [None] + bonds + [None] #NOTE: This is because there is nothing to the left of the first node and nothing to the right of the last node

            prevNextBondSet = []
            for i in range(len(totalBondSet)-1):
                p, n = totalBondSet[i], totalBondSet[i+1]
                prevNextBondSet.append((p,n))

            return prevNextBondSet

        parseResult = {
            "CarbonCount":0, #NOTE: Carbon Count = Chain Length
            "HydrogenCount":0, 
            "BondArr":[],
            "ChainLengthDenotation":'',
            "EachNodePrevBondNextBond":[],
            "Nodes":[]
        }

        #NOTE: These nodes do not implicitly parse single bonds anymore like they did in SC1 and SC2 so you NEED to specify them
        nodes = re.split(r'SingleBond|DoubleBond|TripleBond', "".join(self.tokens)) 
        bondsArr = re.findall(r'(?:SingleBond|DoubleBond|TripleBond)', "".join(self.tokens))
        prevNextBonds = generatePrevBondNextBond(bondsArr)

        if len(nodes) > max_chain_len:
            return '', IllegalChainError(f"Max Chain Length is {max_chain_len}, given chain has {len(nodes)} nodes.")

        ##############################################################################
        #NOTE: Node Handling Starts here all blocks following respec fall under node-handling
        for ni in range(len(nodes)): 
            node = nodes[ni]
            hydrogenCount = 0
            carbonCount = node.count(Tkn_Carbon)

        ##############################################################################
        #NOTE: These are checks before Hydrogen Parsing

            shouldCountH = True #In case of C only in a node
            _i = 0 #Hack-ish solution #NOTE: Incase of reversal errors check here

            if node == '': #NOTE: for trailing bonds Ex: CH3=CH3= <- bad!
                errCompound = ''
                _kekw = errCompound.join(self.tokens).replace("SingleBond",TknBonds["SingleBond"]).replace("DoubleBond",TknBonds["DoubleBond"]).replace("TripleBond",TknBonds["TripleBond"]) #LMAOOOOO
                return '',IllegalChainError(f"Chain cannot end with a trailing bond; -> '{_kekw}' ends with -> '{TknBonds[bondsArr[-1]]}' In Carbon of position {ni+1}")

            #NOTE: Node follows: CHn or CH*n; 
            if node[0] != Tkn_Carbon:#Positional 
                return '',IllegalNodeError("Node must start with Carbon")

            if len(node) == 1:
                shouldCountH = False
            
            if shouldCountH and node[1] != Tkn_Hydrogen:
                if node[1].isnumeric():
                    node_unit = int(node[1])
                    if node_unit > 1 or node_unit == 0: 
                        return '',IllegalNodeError(f"Number of carbon atoms per node can only be 1; Here it is --> {node[1]}")
                    if node_unit == 1:
                        _i = 1 #nICe hAcK vRo 
                    

            #Numeric/Count Based
            if carbonCount > 1:
                return '',IllegalNodeError(f"Maximum number of Carbon atoms per node can only be 1; Here it is --> {carbonCount}")

        ##############################################################################
        #NOTE: Hydrogen Parsing from here
            if shouldCountH:
                hydrogenAtoms = node[1+_i:] #NOTE:Removing the Carbon nodes since its CHn | CH*n

                for i in range(len(hydrogenAtoms)):
                    unit = hydrogenAtoms[i]
                    if unit==Tkn_Hydrogen:
                        hydrogenCount += 1
                    
                    if unit.isnumeric(): #NOTE: if an error comes wrt CANNOT INT this obj its from here                    
                        hydrogenCount += int(unit) - 1 

                if hydrogenCount > 4:
                    return '',IllegalNodeError(f"Maximum number of Hydrogen atoms per node can only be 4 (Methane); Here it is --> {hydrogenCount}")

        ##############################################################################
        #NOTE: SimpleNode making starts here
            nodeIndex = ni
            p, n = prevNextBonds[nodeIndex]
            newNode = SimpleNode(carbonCount,hydrogenCount,p,n) 

            nodeIsValid, msg = newNode.isValidNode()

            if nodeIsValid:
                parseResult["HydrogenCount"] += hydrogenCount
                parseResult["Nodes"].append(newNode)
            else:
                return '',IllegalNodeError(f"Node {newNode} is not a valid combination; {msg}")

        ##############################################################################

        parseResult["CarbonCount"] = len(nodes)
        parseResult["EachNodePrevBondNextBond"] = prevNextBonds
        parseResult["BondArr"] = bondsArr #NOTE: All bonds are to the RIGHT of the respective nodes
        parseResult["ChainLengthDenotation"] = list(TknNums.keys())[parseResult["CarbonCount"]-1]

        rez = NameClass(parseResult)
        rez.nameChain()

        return rez.name, None 

##########################################################################################
#Final Exported Method to interface (nm.py) and internal run methods
##########################################################################################
def passTokens(inputChain):
    lxr = Lexer(inputChain)
    tkns,_err = lxr.makeTokens()
    return tkns,_err

def runParser(inputChain,debugging=False):

    if debugging == True: #Shove all Bugger Objects here
        chainDebugger.activate()
    else: 
        chainDebugger.deactivate()

    lxr = Lexer(inputChain)
    tkns,_err = lxr.makeTokens()
    print(tkns)

    if(_err): return [], _err

    prsr = RegexParser(tkns)
    prsr_res, prsr_err = prsr.evaluate()

    chainDebugger.print(f"FROM PARSER: {inputChain}")
    if(prsr_err): return '', prsr_err

    return prsr_res, None

##############################################################################################
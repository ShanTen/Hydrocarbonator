from singleChainv2 import IllegalChainError, IllegalTerminalError, passTokens, TknNums, Lexer, Tkn_Carbon, Tkn_Hydrogen, TknBonds #Im not not making a parser again from scratch
from ErrorClass import * 
import re

#################################################
# Goal: 
#    Implemnt SV2 in RegexParser -- done
#    Implement Node Array -- done 

#Shantanu's Convention
#NOTE: for notes
#TODO: For inline features to add
#################################################

##########################################################################################
#Constants
##########################################################################################

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

##########################################################################################
#Error Sub Classes
##########################################################################################

class IllegalNodeError(ErrorClass):
    def __init__(self,_errMsg):
        super().__init__("Illegal Node Error",_errMsg)

##########################################################################################
#Diene Chain (Identification Class)
##########################################################################################

class NameClass:
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

        if "TripleBond" in bondsArr:
            self.satType = "Alkyne"
            trplBondIndexes = get_indexes(bondsArr,"TripleBond")
            if (trplBondIndexes[0]) > (self.parseObj["CarbonCount"]-trplBondIndexes[0]):
                bondsArr = bondsArr[::-1]
                self.rev = True
                trplBondIndexes = get_indexes(bondsArr,"TripleBond")
            tripleBondCount = bondsArr.count("TripleBond")            

        if "DoubleBond" in bondsArr:

            if tripleBondCount == 0:
                self.satType = "Alkene"
                dblBondIndexes = get_indexes(bondsArr,"DoubleBond")
                if (dblBondIndexes[0]) > (self.parseObj["CarbonCount"]-dblBondIndexes[0]):
                    bondsArr = bondsArr[::-1]
                    self.rev = True
                doubleBondCount = bondsArr.count("DoubleBond")

            else:
                #NOTE: arr alr reversed from triple bond if needed
                dblBondIndexes = get_indexes(bondsArr,"DoubleBond")
                doubleBondCount = bondsArr.count("DoubleBond")

        if self.satType not in ["Alkene","Alkyne"]:
            self.satType = "Alkane"

        if self.satType == "Alkane":
            nFix = ''
            if self.parseObj["CarbonCount"] > 2:
                nFix = "n-"

            self.name = f"{nFix}{self.parseObj['ChainLengthDenotation']}{self.satType[-3:]}" #NOTE: Adding "ane" to the name 

        dblBondIndexes = [di+1 for di in dblBondIndexes]

        if self.satType == "Alkene":
            _len = doubleBondCount
            self.name = f"{self.parseObj['ChainLengthDenotation']}-{dblBondIndexes}-{IUPACmultipliers[_len]}{self.satType[-3:]}"#NOTE: Adding "ene" or "yne" to the name 

        trplBondIndexes = [ti+1 for ti in trplBondIndexes]

        if self.satType == "Alkyne":
            _len = tripleBondCount
            if doubleBondCount == 0:
                self.name =  f"{self.parseObj['ChainLengthDenotation']}-{trplBondIndexes}-{IUPACmultipliers[_len]}{self.satType[-3:]}" #NOTE: Adding "ene" or "yne" to the name 
            else:
                d_len = doubleBondCount
                self.name =  f"{self.parseObj['ChainLengthDenotation']}-{dblBondIndexes}-{IUPACmultipliers[d_len]}ene-{trplBondIndexes}-{IUPACmultipliers[_len]}{self.satType[-3:]}" #NOTE: Adding "ene" or "yne" to the name 

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
                return '',IllegalChainError(f"Chain cannot end with a trailing bond; -> '{_kekw}' ends with -> '{TknBonds[bondsArr[-1]]}'")

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
                continue
            else:
                return '',IllegalNodeError(f"Node {newNode} is not a valid combination; {msg}")

            parseResult["HydrogenCount"] += hydrogenCount
            parseResult["Nodes"].append(newNode)

        ##############################################################################

        parseResult["CarbonCount"] = len(nodes)
        parseResult["EachNodePrevBondNextBond"] = prevNextBonds
        parseResult["BondArr"] = bondsArr #NOTE: All bonds are to the RIGHT of the respective nodes
        parseResult["ChainLengthDenotation"] = list(TknNums.keys())[parseResult["CarbonCount"]-1]

        max_chain_len = 20
        if parseResult["CarbonCount"] > max_chain_len:
            return '',IllegalChainError(f"Chain is too long ({parseResult['CarbonCount']} nodes)! Max length is {max_chain_len}")



        rez = NameClass(parseResult)
        rez.nameChain()

        return rez.name, None 

##########################################################################################
#Final Exported Method to interface (nm.py)
##########################################################################################

def runParser(inputChain):

    lxr = Lexer(inputChain)
    tkns,_err = lxr.makeTokens()
    
    if(_err): return [], _err

    prsr = RegexParser(tkns)
    prsr_res, prsr_err = prsr.evaluate()

    if(prsr_err): return '', prsr_err

    return prsr_res, None

##########################################################################################
#Testing Funtions
##########################################################################################

def test_ch(node):
    Tkn_Hydrogen = "H"
    hydrogenCount  = 0
    hydrogenAtoms = node[1:] #Removing the Carbon nodes since its CHn | CH*n

    for i in range(len(hydrogenAtoms)):
        unit = hydrogenAtoms[i]
        if unit==Tkn_Hydrogen:
            hydrogenCount += 1
        
        if unit.isnumeric(): #NOTE: if an error comes wrt CANNOT INT this obj its from here
            if int(unit):
                hydrogenCount += int(unit) - 1

    return hydrogenCount

def test():
    while 1:
        inputChain = input(">>> ")
        tkns,_err = passTokens(inputChain)
        
        if _err:
            print(_err)
            break
        
        prsr = RegexParser(tkns)
        res, err = prsr.evaluate()

        if(err):
            print(_err)
            break

        print(res)
    return
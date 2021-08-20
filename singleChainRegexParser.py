from singleChainv2 import passTokens, TknNums, Lexer, Tkn_Carbon, Tkn_Hydrogen, TknBonds #Im not not making a parser again from scratch
from ErrorClass import ErrorClass #Ifstg if the import is the error
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
#Error Sub Classes
##########################################################################################

class IllegalNodeError(ErrorClass):
    def __init__(self,_errMsg):
        super().__init__("Illegal Node Error",_errMsg)

##########################################################################################
#Diene Chain (Identification Class)
##########################################################################################

#TODO: Working on diene class
#NOTE: CH3​−CH=CH−C#CH => Pent-3-en-1-yne
#NOTE: CH#C-CH2-CH=CH-CH3 => Hex-4-ene-1-yne
class DieneChain:
    pass

##########################################################################################
#Simple Node Class
##########################################################################################

class SimpleNode: #work back on this later

    def __init__(self, carbonCount, hydrogenCount, prevBond=None,nextBond=None):
        
        self.carbonCount = carbonCount
        self.hydrogenCount = hydrogenCount
        self.prevBond = prevBond #singleDoubletripleNone
        self.nextBond = nextBond #singleDoubletripleNone

    def validateNode(self):
        #NOTE: Based off attributes 
        pass

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
        
    def closestUnsat(self):
        pass

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
        nodes = re.split(r'SingleBond|DoubleBond|TripleBond', "".join(self.tokens)) #TODO: parse as CH* till bond then verify node 
        bondsArr = re.findall(r'(?:SingleBond|DoubleBond|TripleBond)', "".join(self.tokens))
        prevNextBonds = generatePrevBondNextBond(bondsArr)

        ##############################################################################
        #NOTE: Node Handling Starts here all blocks following respec fall under node-handling
        for ni in range(len(nodes)): #TODO: Making this int based loop rather than obj based
            
            node = nodes[ni]

            hydrogenCount = 0
            carbonCount = node.count(Tkn_Carbon)

        ##############################################################################
        #NOTE: These are checks before Hydrogen Parsing

            shouldCountH = True #In case of C only in a node
            _i = 0 #Hack-ish solution #NOTE: Incase of reversal errors check here

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
            newNode = SimpleNode(carbonCount,hydrogenCount,p,n) #TODO: Validate node    
            parseResult["HydrogenCount"] += hydrogenCount
            parseResult["Nodes"].append(newNode)

        ##############################################################################

        parseResult["CarbonCount"] = len(nodes)
        parseResult["EachNodePrevBondNextBond"] = prevNextBonds
        parseResult["BondArr"] = bondsArr #NOTE: All bonds are to the RIGHT of the respective nodes
        parseResult["ChainLengthDenotation"] = list(TknNums.keys())[parseResult["CarbonCount"]-1]

        return parseResult, None #TODO: Actually Name the compound using the diene class
        # return f"{parseResult['ChainLengthDenotation']}", None 

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
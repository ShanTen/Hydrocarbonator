from singleChainv2 import passTokens, TknNums, Lexer, Tkn_Carbon, Tkn_Hydrogen #Im not not making a parser again from scratch
import re

#################################################
# Goal: 
#    Implemnt SV2 in RegexParser
#    Implement Node Array 

#Shantanu's Convention
#NOTE: for notes
#TODO: For inline features to add
#################################################

class DieneChain:
    pass

class SimpleNode: #work back on this later

    def __init__(self, carbonCount, hydrogenCount, prevBond=None,nextBond=None):
        self.carbonCount = carbonCount
        self.hydrogenCount = hydrogenCount
        self.prevBond = prevBond #singleDoubletripleNone
        self.nextBond = nextBond #singleDoubletripleNone

    def validateNode(self):
        pass


class RegexParser:
    def __init__(self,tokensArr):
        self.rawTokens = tokensArr
        self.tokens = [tok.value for tok in tokensArr]
        
    def closestUnsat(self):
        pass

    def evaluate(self):

        parseResult = {
            "CarbonCount":0, #NOTE: Carbon Count = Chain Length
            "HydrogenCount":0, 
            "BondArr":[],
            "ChainLengthDenotation":'',
            "Nodes":[]
        }

        # #NOTE:Only Parses CHn (For Now)
        # parsedTokens = re.findall(r'(?:CH[1-4]|CH|C|SingleBond|DoubleBond|TripleBond)', "".join(self.tokens))

        #NOTE: These nodes do not implicitly parse single bonds anymore so you NEED to specify them
        nodes = re.split(r'SingleBond|DoubleBond|TripleBond', "".join(self.tokens)) #TODO: parse as CH* till bond then verify node 


        ##############################################################################
        #NOTE: Node Handling Starts here all blocks following respec fall under node-handling
        for node in nodes:
            carbonCount = node.count(Tkn_Carbon)

        ##############################################################################
        #NOTE: These are checks before Hydrogen Parsing

            #NOTE: Node follows: CHn or CH*n; 
            if node[0] != Tkn_Carbon:#Positional 
                print("Illegal node error: Node must start with Carbon")
                break 

            if node[1] != Tkn_Hydrogen:
                if node[1].isnumeric():
                    print(f"Illegal node error: Number of carbon atoms per node can only be 1\nHere it is -->{node[1]}")
                    break

            #Numeric/Count Based
            if carbonCount > 1:
                print(f"Illegal node error: Maximum number of Carbon atoms per node can only be 1\nHere it is -->{carbonCount}")
                break
        ##############################################################################
        #NOTE: Hydrogen Parsing from here
            
            hydrogenAtoms = node[1:] #Removing the Carbon nodes since its CHn | CH*n

            for i in range(len(hydrogenAtoms)):
                unit = hydrogenAtoms[i]
                if unit==Tkn_Hydrogen:
                    hydrogenCount += 1
                
                if unit.isnumeric(): #NOTE: if an error comes wrt CANNOT INT this obj its from here
                    if int(unit):
                        hydrogenCount += int(unit) - 1

            if hydrogenCount > 4:
                print(f"Illegal node error: Maximum number of Hydrogen atoms per node can only be 4 (Methane)\nHere it is -->{hydrogenCount}")

        ##############################################################################

        bondPosArr = re.findall(r'(?:SingleBond|DoubleBond|TripleBond)', "".join(self.tokens))
        parseResult["CarbonCount"] = len(nodes)
        parseResult["Nodes"] = nodes #TODO: Change this to SimpleNode class instances 
        parseResult["BondArr"] = bondPosArr #NOTE: All bonds are to the RIGHT of the respective nodes
        parseResult["ChainLengthDenotation"] = list(TknNums.keys())[parseResult["CarbonCount"]-1]

        print(f"nodes: {nodes}")
        print(parseResult)

        

        return f"{parseResult['ChainLengthDenotation']}", None 

def runParser(inputChain):

    lxr = Lexer(inputChain)
    tkns,_err = lxr.makeTokens()
    
    if(_err): return [], _err

    prsr = RegexParser(tkns)
    # print(prsr.parse())
    prsr_res, prsr_err = prsr.evaluate()

    if(prsr_err): return '', prsr_err

    return prsr_res, None

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


        # tks = []
        # for t in tkns: #We can start test regex parsing from here
        #     tks.append(t.value)
        # print(f"Tokens: {tks}")
        # # (?:a|b)
        # parsedTokens = re.findall(r'(?:CH[1-4]|CH|C|SingleBond|DoubleBond|TripleBond)', "".join(tks))
        # print(f"Standing Hydrogen: {re.findall(r'(?:CH.+?(?=SingleBond|DoubleBond|TripleBond)|CHH[1-3]|CH[1-3]H)',''.join(tks) )}")
        # nodes = re.findall(r'CH[0-4]', "".join(tks))
        
        # print(f"parsedTokens: {parsedTokens}")
        # print(f"nodes: {nodes}")
    return
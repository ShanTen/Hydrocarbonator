##########################################################################################
# singleChainv1.py is a wrap
# Features Are:
# Elemenatal Carbon and Bond Lexer. I.e Token Types -> ElementalCarbon && BondType
# Chain Length Calculation and Naming 
# Bond Type and Position Identifier
# Note: This version works with terminal verification only with Carbon, ref line 68 for implementation of that
# Messups:
#     Got Token Typing Messed up a little
#     For ChaintLenght, Count determined purely on if node is elemental node rather than a carbon node + elements attached to it 
##########################################################################################



##########################################################################################
#Lexer
##########################################################################################

TknBonds = {
    "SingleBond":"-",
    "DoubleBond":"=",
    "TripleBond":"≡"
}

Tkn_Carbon = "C"
Tkn_Hydorgen = "H"

TknElements = [Tkn_Carbon] #NOTE:Change this to elemental class later + dont do this bs raw entry shit

#Types of Values in this code 
TknTypeBond = "BOND"
TknTypeElement = "ELEMENT_NODE"

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

            elif self.currentChar in TknBonds.values():
                tokens.append(Token(TknTypeBond,list(TknBonds.keys())[list(TknBonds.values()).index(self.currentChar)]))
                self.advance()

            else:#throw invalid character error
                _char_ = self.currentChar
                self.advance()
                _error = IllegalCharacterError(f"Illegal Character --> '{_char_}'")
                return [],_error
    
        if tokens[0].value != Tkn_Carbon: #NOTE:You should change this the tokens[0].type != TknTypeElement in later versions
            return None,IllegalTerminalError(tokens[0],"start")
        if tokens[-1].value != Tkn_Carbon:
            return None,IllegalTerminalError(tokens[-1],"end")

        return tokens,None
##########################################################################################
#Parser:
#   Chain Lenght Counter (No.Carbons)
#   Bond Pos Indicator as an object
# No Error Handling here for now except bond to bond error ig
##########################################################################################

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = -1
        self.bondPos = 0
        self.advance() 

    def advance(self):
        self.pos+=1
        if self.pos < len(self.tokens):
            self.currentToken = self.tokens[self.pos]

    def parse(self):
        
    # Okay Assume Alignment Either LEFT to Right (LR) or RIGHT to LEFT (RL) depending on our rules [Very Low Level Simplification Not great strat for high level implementation welp]
    # The position of the Bond will be towards the Alignment of the character it is bonded towards
    # Example:
    #     LR
    #     c=c-c => there are 3 C's => C0=C1=C2 => Double Bond at C0 => Single Bond at C1 => (Pos,Bond) Vector => [(0,DoubleBond),(1,SingleBond)]
    #     RL
    #     c≡c-c=c => [(0,DoubleBond),(1,SingleBond),(2,TripleBond)]
    # For now Ig I'll hardcode Alignment

        parseResult = {"ChainLength":0,"ChainLengthDenotation":'',"BondPosArr":[]}
        
        while self.pos < len(self.tokens):
            tkn = self.currentToken
            #NOTE:For RL config just invert the array ig 
            #A bond can only follow an elemental carbon node and not another bond itself.

            if (tkn.type == TknTypeElement):#Some sort of isValidNode() method to be used here in later version 
                parseResult["ChainLength"] += 1

            if (tkn.type == TknTypeBond):

                if(self.tokens[self.pos+1].type == TknTypeBond):
                    return {},IllegalBondError("A bond can only follow an elemental carbon node and not another bond itself.")

                self.bondPos += 1 #This might be biggest bren movie or 0 tier low IQ shit. We shall find out soon.
                parseResult["BondPosArr"].append((self.bondPos,
                tkn.value
                ))

            self.advance()

        if parseResult["ChainLength"] >= 14:
            return {},IllegalChainError("Single Chain Longer than 13 nodes.")

        parseResult["ChainLengthDenotation"] = list(TknNums.keys())[parseResult["ChainLength"]-1]

        return parseResult,None

    def __repr__(self):
        pass #Work on making rep look pretty later, too tired now.

##########################################################################################
#Error Class
##########################################################################################
class ErrorClass:
    def __init__(self, errorType, details):
        self.errorType = errorType
        self.details = details

    def stringify(self):
        string = f'{self.errorType}:\n{self.details}'
        return string

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
def run(inputChain):
    lxr = Lexer(inputChain)
    tkns,_err = lxr.makeTokens()
    
    if(_err): return [], _err

    prsr = Parser(tkns)
    prsr_res, prsr_err = prsr.parse()

    if(prsr_err): return {}, prsr_err

    return prsr_res, None

# :)
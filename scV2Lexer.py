from singleChainv2 import Parser,TknBonds, Tkn_Carbon, Tkn_Hydorgen, TknTypeElement, TknTypeElementCount, TknTypeBond, TknNums
from singleChainv2 import IllegalTerminalError, IllegalBondError, IllegalChainError
from PureHydrocarbons import Hydrocarbon
#SCV3 ignore name of file this is SCV3


#-----BIG BOI COMMENTS---------------------------------------------

#what is a simple node? --> Carbon with 4 attachments  
# either [4 singlely bonded] or 
# [2 doubly] or 
# [1 triple and 1 single] or 
# [2 single and 1 double]. 


"""
You can make an override constructors for all the different permutations possible for each simple chain node

Constructor Types --> Only Hydrogen and Oxygen

s,d,t --> Singly,Doubly,Tripley

ToNode - 4s ; FromNode - 0 [Methane]
ToNode - 3s; FromNode - 1s
ToNode - 2s; fromNode - 2s
ToNode - 2s; fromNode - 1d
ToNode - 1s; fromNode - 3s
"""

    # This  should mean that if a carbon is bonded to a hydrogen that is counted as a carbon being singly bonded
    # Double Bonded and triplely bonded usually happens between nodes. [This is only for chain if carbon is attached]
    # themselves because each node is connected to the other
    # This would mean that we would give rise to a tree like object where each next node is dictated by what type of bond is attached to it
    # IntraNodalBonding --> Carbon to Carbon Main Chain Bonds --> NodeBirthingBond
    # ExtroNodalBonding --> Bonding to Soley that Carbon not giving rise to another 
    # node also can be named --> NonBirthingBond Ex(Singly Attached H, Doubly Attached Oxygen etc)
    # Given that this is SCV3 and we're still only focused on pure Hydrocarbons no need to
    # No need to normalize code for anything apart from Hydrogen and Carbon.


        #You have both with and without coeff in one method.
        #I am sending in the whole chain for this la so why not if next char != int just +1 ?
        # hCount = 0

        # #tackling last index first to prevent an out of bounds err
        #CHHH-CHH=CH2H --> CH3-CH2=CH3 everything in between a bond is a node. yes? yes.
        # if self.tokens[-1].type == TknTypeElementCount and self.tokens[-2].value == Tkn_Hydorgen:
        #     hCount += int(self.tokens[-1].value) #Take last element if its int and preceeded by Hydrogen


#-----------------------------------------------------------------------

class SimpleNode: #work back on this later
    #Make validate here later
    def __init__(self, carbonCount=None, hydrogenCount=0, prevBond=None,nextBond=None):
        self.carbonCount = 1 #isnt this always going to be 1?
        self.hydrogenCount = hydrogenCount
        self.prevBond = prevBond #singleDoubletriple 
        self.nextBond = nextBond #singleDoubletriple


class WorkingSCV3: #28-07-21 Started becuase old one was a mess in this file
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = -1 #POSITION IS THE POSITION IN THE LIST OF TOKENS FED
        self.bondPos = 0
        self.NullLine = False
        self.advance()

    def closestUnsat(self): #Seems pointless
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
        #SCV3
        # self.tokens = self.closestUnsat()
        # print(self.closestUnsat())

        #Parse Nothing
        if self.NullLine == True:
            return '',None

        #parseResult objeect looks like a mess rn
        #"ChainLength":0,"ChainLengthDenotation":'',"BondPosArr":[],"NodalAttachedCount":[]
        parseResult = {
            "ChainLength":0
        }
        
        validEndTerminalTypes = [TknTypeElement,TknTypeElementCount]
        if self.tokens[-1].type not in validEndTerminalTypes:
            return None,IllegalTerminalError(self.tokens[-1],"end")

        while self.pos < len(self.tokens):
            tkn = self.currentToken

            #Changed this to chain length wrt to Carbon
            if (tkn.value == Tkn_Carbon):#Some sort of isValidNode() method to be used here in later version 
                parseResult["ChainLength"] += 1

            if(tkn.value == Tkn_Hydorgen and ((self.pos+1 == len(self.tokens)) or (not self.tokens[self.pos+1].value.isnumeric()))):
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
                if obj["attachedToelement"] == Tkn_Hydorgen:
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
            return f"n-{parseResult['ChainLengthDenotation']}{suffix[-3:]}",None

        elif suffix in ["Alkene","Alkyne"]: 
            bond_pos = getBondPos(suffix)

            if bond_pos>(parseResult["ChainLength"]-bond_pos):
                bond_pos = parseResult["ChainLength"]-bond_pos #Set bond_pos to lower value


            return f"{parseResult['ChainLengthDenotation']}-{bond_pos}-{suffix[-3:]}",None

    def __repr__(self):
        pass #Work on making rep look pretty later, too tired now.


class SCV3(Parser):


    def parseNew(self):
        self.nodeArr = []
        for tok in self.tokens:
            tokIndex = self.tokens.index(tok)

            #carbon node starts only with Carbon >:(
            if tok.value == Tkn_Carbon:
                node2append = SimpleNode()
                
                if tokIndex == 0: #If It is starting it doesnt have prevBond so None
                    node2append.prevBond = None 
                else: #if I have a prevBond
                    node2append.prevBond=self.tokens[tokIndex-1].value  


    def parseOld(self):
        #parseResult objeect looks like a mess rn
        parseResult = {
            "ChainLenght":0,#basically just carbon count
            "HydrogenCount":0, #Hydrogen count
            "ChainLengthDenotation":'',
            "BondPosArr":[], #Type of Bond and Position of it wrt to closest element
            "Nodes":[] #Each node is a nodal object you can invert this to obtain RL config from LR config; leabe for now
        }

        validEndTerminalTypes = [TknTypeElement,TknTypeElementCount]
        if self.tokens[-1].type not in validEndTerminalTypes:
            return None,IllegalTerminalError(self.tokens[-1],"end")



        for el in self.tokens:

            if el.type == TknTypeBond:
                #get all elements before this index
                bondIndex = self.tokens.index(el)
                parseResult["BondPosArr"].append((bondIndex,el.value))   #pos, index
                nodeRawItems = self.tokens[0,bondIndex]
                self.nodeAnalysisArr = nodeRawItems
                self.makeNode(self.nodeAnalysisArr)
    

        while self.pos < len(self.tokens):
            tkn = self.currentToken
            
            #Changed this to chain length wrt to Carbon
            if (tkn.value == Tkn_Carbon):#Some sort of isValidNode() method to be used here in later version 
                parseResult["ChainLength"] += 1

            if(tkn.value == Tkn_Hydorgen and ((self.pos+1 == len(self.tokens)) or (not self.tokens[self.pos+1].value.isnumeric()))):
                _hydrogenWithoutCoeff += 1

                parseResult["BondPosArr"].append((self.bondPos,
                tkn.value
                ))

            if(tkn.type == TknTypeElementCount): #FIX THIS BAKA --> FIX TO include 'CH' also and not just CnHn

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

        def hydrogenWithCoef():
            hc = 0
            for obj in parseResult["NodalAttachedCount"]:
                if obj["attachedToelement"] == Tkn_Hydorgen:
                  hc += obj["count"]

            return hc
        
        HydrogenCount = hydrogenWithCoef() + _hydrogenWithoutCoeff

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

        print(parseResult["Nod"])

        if suffix == "Alkane": 
            return f"n-{parseResult['ChainLengthDenotation']}{suffix[-3:]}",None

        elif suffix in ["Alkene","Alkyne"]: 
            bond_pos = getBondPos(suffix)
            return f"{parseResult['ChainLengthDenotation']}-{bond_pos}-{suffix[-3:]}",None
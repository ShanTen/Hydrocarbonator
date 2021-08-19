from ErrorClass import ErrorClass

#EVALS PARSED OBJECT OF CHAIN TO DETERMINE IF ALKANE, ALKENE, ALKYNE

class VerificationErr(ErrorClass):
    def __init__(self,_errMsg): #A bond can only follow an elemental carbon node and not another bond itself.
        super().__init__("Illegal Pure Hydrocarbon Error --> ",_errMsg)

class Hydrocarbon: #OH GOD THE BOND COUNT DURING DECLARATION
    def __init__(self,CarbonCount,HydrogenCount,bondCountObj):
        
        self.carbonCount = CarbonCount
        self.hydrogenCount = HydrogenCount

        self.bndCountObj = bondCountObj

        self.snglBondCount = bondCountObj["SingleBond"]
        self.dblBondCount = bondCountObj["DoubleBond"]
        self.trplBondCount = bondCountObj["TripleBond"]


        self.type = self.determineType()

    def determineType(self):
        #CnH2n+2
        if (self.carbonCount*2) + 2 == (self.hydrogenCount) and self.snglBondCount>=0 and not self.dblBondCount and not self.trplBondCount:
            return "Alkane",None
        #CnH2n
        elif self.carbonCount*2 == (self.hydrogenCount) and self.dblBondCount == 1 and not self.trplBondCount:
            return "Alkene",None
        #CnH2n-2
        elif (self.carbonCount*2) - 2 == self.hydrogenCount and self.trplBondCount == 1 and not self.dblBondCount:
            return "Alkyne",None

        else:

            debugErrMsg = f'{self.bndCountObj} CarbonCount:{self.carbonCount} HydrogenCount:{self.hydrogenCount}'
            return '',VerificationErr(debugErrMsg) #Point out specifics later
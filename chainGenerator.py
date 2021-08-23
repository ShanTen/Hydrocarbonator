#For making make shift rudimentary test cases 
def makeAlkanes(_range):
    alkanes = []
    for s in _range:
        chain = "CH3-" + "CH2-"*(s-2) + "CH3"
        alkanes.append(chain)
    
    return alkanes

def makeAlkenePermutations(size):
    #NOTE: Size >= 4
    #Doesn't do terminal adjustment (yet)
    res = []
    for pos in range(1,size-2):
        sl, sr = pos-1, size-pos-2
        k = "CH3-" + "CH2-"*sl + "CH=CH-" + "CH2-"*sr + "CH3"
        res.append(k)
    return res


for chainSize in range(4,20):
    kenes = makeAlkenePermutations(chainSize)
    # print(f"Chain Size: {chainSize+1}")
    [print(i) for i in kenes]



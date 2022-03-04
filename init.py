import pickle as p
with open("./cache.bin","wb") as f:
    empSet = {"CH4":"Methane"} #Empty dict is uncomfortable so we start with a preset one.
    p.dump(empSet,f)
    f.flush();f.close()
print("Cache set up.")
import pickle as p
with open("./cache.bin","wb") as f:
    empSet = {"CH4":"Methane"}
    p.dump(empSet,f)
    f.flush();f.close()
print("Cache set up.")
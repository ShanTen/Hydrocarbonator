import pickle as p
with open("./cache.bin") as f:
    p.dump({"CH4":"Methane"},f)
    print("Cache set up.")
    f.flush();f.close()
import pickle

vbic = pickle.load(open('vbic4.p', 'rb'))

for x in vbic:
    if x['Categories']:
        for y in x['Categories']:
            if type(y) is tuple:
                print(y)
                temp = [y[0],y[1]]
                y = temp
                print(y)
                
        
pickle.dump(vbic, open("vbic5.p", "wb"))

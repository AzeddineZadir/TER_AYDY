import pandas as pd
import re
import json


regles = pd.read_csv('regle.txt', encoding="utf-8", header=None, delimiter = "\t")
pos = [[{'la': 'E'},{'la': 'Det'}, {'maison': 'Nom'}]]
regle = regles[0]
# print(regle)
Dict = []
for r in regle :
    r_dict = []
    re = r.split(",")
    for dict_r in re :
        d = json.loads(dict_r)
        r_dict.append(d)
    Dict.append(r_dict)


for phrase in pos :
    position_mot = 0
    equal =0
    for mot in phrase:
        
        for pattern in Dict:
            long = len(pattern)
            for element in pattern:
               
                if str(element.values()) == str(mot.values()):
                    i = 0
                    while(i<long):
                        print(pattern[i])
                        print(phrase[position_mot])
                        if(str(pattern[i].values())==str(phrase[position_mot].values())):
                            print("yes")
                        i+=1
                # else :
        
        position_mot+=1
                
        
    
    
       

# print(Dict[0][0])
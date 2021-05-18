from jdmLink import *
from functions import * 
import json

# termes = getTermesR0("restauration")
# print(termes)
# print(len(termes))
# termes = getAllTermesR0(["restauration"])
# print(termes)
# print(len(termes))

# print("filter termes ************************************************************************************ ")
# filtered= filterVocabularyByFile(termes)
# print(filtered)
# # print(len(filtered))


# c_liste = getCommentsScoreByVect(filtered)
# for c in c_liste : 
#     print(c["id"])

user_req = formatUserReq("je veux une grande chambre")
comments = getCommentsScoreByVect(user_req)
newlist = sorted(comments, key=lambda k: k['score'],reverse=True) 
for c in newlist : 
    print (f"{c['id']} score : {c['score']}")

print(len(comments))
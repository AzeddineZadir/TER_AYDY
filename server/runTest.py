from jdmLink import *
from functions import * 
import json

termes = getTermesR0("piscine")
# print(termes)
# print(len(termes))
print("filter termes ************************************************************************************ ")
filtered= filterVocabularyByFile(termes)
print(filtered)
# print(len(filtered))


c_liste = getCommentsScoreByVect(filtered)
for c in c_liste : 
    print(c["id"])


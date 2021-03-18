import os, json, re
import pandas as pd
import requests 
os.system("clear")
from flask import Flask, render_template, request
from functions import *
from jdmLink import *

app = Flask(__name__)




@app.route('/')  # route localhost:5000
def index():
   
   print("relations sortantes et entrantes")
   # words2 =getTermesR0("piscine")
   # print(len(words2))
   # print(words2)
   # print("seulemment les relations sortantes ")
   # words1 =getTermesR0Sortants("piscine")
   # print(len(words1))
   # print(words1)

   # print(reseauxDump("mer",""))
   #print(getTermesR0("mer"))
   # print(len(getTermesR0Sortants("piscine")))
   # getCommentsScore(["vue","mer","lit","chambre"])
   #
   # filterWordsByOntologie(getTermesR0Sortants("vue"))
   # creatOntologiWordsFiles(getMyOntologie())
   # print (getWordScore("couette"))
   # print(getTermesR0("vue"))

   # print(getTermesR0Sortants("vue"))
   getCommentsScore(["vue"])

   return " index page "


# recupérer tous les mots lies grace a r_assicieted R0  au mot passer en parametre 
@app.route('/<word>')  # route localhost:5000
def r_associated(word):
   results= getTermesR0(word)          
   return json.dumps(results, ensure_ascii=False)

# récupérer tous les mots lier a une liste de mots 
@app.route('/releated',methods = ['POST'])
def releated():
   result = request.json
   phrase=result['phrase']
 
   print(phrase)
    
     
   return json.dumps(phrase, ensure_ascii=False)




app.run()
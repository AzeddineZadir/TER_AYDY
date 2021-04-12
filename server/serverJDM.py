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
   
  
   # wordss = getTermesR0Sortants("mer")
   # print(len(wordss))
   # # print(wordss)

   # filter_termes = filterVocabulary(wordss)

   # print(len(filter_termes))
   # print(filter_termes)
   # print(getTermesR0("mer"))

   # print(getTermesR9("mer"))
   # print(getWordScore("mer"))
   # print(getWordScore("vue"))
   # getCommentsScore(["piscine","lit","chambre"])
   print(reseauxDump("vue", 4))


  
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
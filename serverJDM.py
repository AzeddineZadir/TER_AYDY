import os, json, re
import pandas as pd
# importing the requests library 
import requests 
os.system("clear")
from flask import Flask, render_template, request
from functions import getAllTermes, getTermes, reseauxDump ,searchInComments

app = Flask(__name__)




@app.route('/')  # route localhost:5000
def index():
   
   searchInComments(["piscine","mer"])
   return " index page "


# recupérer tous les mots lies grace a r_assicieted R0  au mot passer en parametre 
@app.route('/<word>')  # route localhost:5000
def r_associated(word):
   results= getTermes(word)          
   return json.dumps(results, ensure_ascii=False)

# récupérer tous les mots lier a une liste de mots 
@app.route('/releated',methods = ['POST'])
def releated():
   result = request.json
   phrase=result['phrase']
 
   print(phrase)
    
     
   return json.dumps(phrase, ensure_ascii=False)




app.run()
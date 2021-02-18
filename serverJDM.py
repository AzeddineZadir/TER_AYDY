import os, json, re
import pandas as pd
# importing the requests library 
import requests 
os.system("clear")
from flask import Flask, render_template, request
from functions import Sortpertinance, getTermes, reseauxDump

app = Flask(__name__)
comments = pd.read_csv('comments.txt', header = None)
commentaires = comments[0]



@app.route('/')  # route localhost:5000
def index():

   return " index page "


# recupérer tous les mots lies grace a r_assicieted R0  au mot passer en parametre 
@app.route('/rel/<word>')  # route localhost:5000
def r_associated(word):
   results= getTermes(word)          
   return json.dumps(results, ensure_ascii=False)

# récupérer tous les mots lier a une liste de mots 
@app.route('/releated',methods = ['POST'])
def releated():
   result = request.json
   phrase=result['phrase']
   BestComments = Sortpertinance(phrase,commentaires)
   
   return json.dumps(BestComments, ensure_ascii=False)




app.run()
import os, json, re
import pandas as pd
# importing the requests library 
import requests 
os.system("clear")
from flask import Flask, render_template, request
from functions import getTermes, reseauxDump

app = Flask(__name__)




@app.route('/')  # route localhost:5000
def index():
   

   return " index page "


# recupérer tous les mots lies grace a r_assicieted R0  au mot passer en parametre 
@app.route('/<word>')  # route localhost:5000
def r_associated(word):
   results= getTermes(word)         
       
   return json.dumps(results, ensure_ascii=False)
# get ID of the word




app.run()
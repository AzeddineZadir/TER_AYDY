import os, json, re
import pandas as pd
# importing the requests library 
import requests 
os.system("clear")
from flask import Flask, render_template, request
from functions import getTermes, reseauxDump, reseauxDump_norelin


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

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')

#app.run()
import os, json, re
import pandas as pd
import requests 
os.system("clear")
from flask import Flask, render_template, request
from functions import *
from jdmLink import *
from flask_cors import CORS
app = Flask(__name__)


app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')  # route localhost:5000
def index():
   
   return " server index page "


# recupérer tous les mots lies grace a r_assicieted R0  au mot passer en parametre 
@app.route('/<word>')  # route localhost:5000
def r_associated(word):
   results= getTermesR0(word)          
   return json.dumps(results, ensure_ascii=False)

# récupérer tous les mots lier a une liste de mots 
@app.route('/releated',methods = ['POST'])
def releated():
   result = request.json
   souhait = result[0]["souhait"]
   print(result)
   Nom = getNom(souhait)
   selectors = []
   for select in result[1].values():
      selectors = select
   Id = result[2]["id"]
   user_req=[]
   if int(Id) == 1:
      user_req = formatUserReqByR0(souhait,selectors)
      print("user_req")
      print(user_req)
      comments=[]
      comments = getCommentsScoreByVect(user_req)
      # print("comments")
      print(comments)
      Hotels = CommentsPolarisation(comments,Nom) 
     
   else:
      user_req = formatUserReqByR5(souhait,selectors)
      comments = getCommentsScoreByVect(user_req)

      Hotels = CommentsPolarisation(comments,Nom)  

   return json.dumps(Hotels, ensure_ascii=False)




app.run()
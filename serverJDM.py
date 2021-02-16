import os, json, re
import pandas as pd
# importing the requests library 
import requests 

os.system("clear")
from flask import Flask, render_template, request
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from spacy import displacy
from functions import reseauxDump

app = Flask(__name__)




@app.route('/')  # route localhost:5000
def index():
   doRequest()
   return "Ceci est la page d'accueil. du serveur simplifier "
# get ID of the word


def doRequest ():

   reseauxDump("mer",0)
   

app.run()
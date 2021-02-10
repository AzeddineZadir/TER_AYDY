#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os, json, re
import pandas as pd
import spacy

os.system("clear")

from flask import Flask, render_template, request
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from spacy import displacy

stopWords = set(stopwords.words('french'))
app = Flask(__name__)
nlp = spacy.load("fr_core_news_sm")
# 0 r_associated
typesRelations = {
    "5": "r_syn",
    "6": "r_isa"
   }

# Chargements des mots
motsParIds = {}
relationsParIdMots = {}
nomsParIdAdjectifs = {}
print('Chargement des mots')
fd = open("motsJDM.txt","r",encoding='utf-8')
for ligne in fd :
    data = ligne.split(":")
    motsParIds[data[0]] = data[1][:-1]
print("Nombre de mots :", len(motsParIds.keys()))

for numRel in typesRelations :
    print("Chargement des relations", numRel, "("+typesRelations[numRel]+")")
    fd = open("relations"+str(numRel)+".txt")
    for ligne in fd :
        data = ligne.split(":")
        idMot = data[0]
        idn2 = data[1]
        poids = data[2][:-1]
        if idn2 in motsParIds :
            if numRel != "19" and numRel != "164" :
                if idMot in relationsParIdMots :
                    relationsParIdMots[idMot].append((idn2, numRel, poids))
                else :
                    relationsParIdMots[idMot] = [(idn2, numRel, poids)]
            if numRel == "164" : # r_adj>verbe
                nomsParIdAdjectifs[idMot] = motsParIds[idn2]

@app.route('/')  # route localhost:5000
def index():
   return "Ceci est la page d'accueil. du serveur simplifier "

@app.route('/mot/<idMot>')
def mot(idMot):
    print("/mot/"+idMot)
    if idMot in motsParIds :
        return motsParIds[idMot]
    return "-1"

# récupérer tous les synonyme d'un mot
@app.route('/syno/<mot>')
def syno(mot):
    results=[]
    id=0
    for idMot in motsParIds :
        if motsParIds[idMot] == mot:
            id = idMot

    for rel in relationsParIdMots[id] :
            print(rel)
            if rel[0] in motsParIds and rel[1]=="5" :
                results.append([motsParIds[rel[0]], typesRelations[rel[1]], rel[2]])

    return json.dumps(results, ensure_ascii=False)


comments = pd.read_csv('comments.txt', header = None)
commentaires = comments[0]

def return_token(sentence):
    doc = nlp(sentence)
    return [X.text for X in doc]

def removeStopWords(sentence):
    tokens = return_token(sentence)
    clean_words = []
    for token in tokens:
        if token.lower() not in stopWords:
         clean_words.append(token)

    return clean_words

def get_comments_from_synonymes(researched_expression):
    
    returned_comments = []
    
    for c in commentaires : 
        l = removeStopWords(c)
        if (researched_expression in l) and (c not in returned_comments): 
            returned_comments.append(c)
    return returned_comments

def get_synonymes(word):
    results=[]
    id=0
    for idMot in motsParIds :
        if motsParIds[idMot] == word:
            id = idMot

    for rel in relationsParIdMots[id] :
            # print(rel)
            if rel[0] in motsParIds and rel[1]=="5" :
                #results.append([motsParIds[rel[0]], typesRelations[rel[1]], rel[2]])
                if (int (rel[2])>30) :
                    results.append(motsParIds[rel[0]])
                    print (motsParIds[rel[0]])                   
    return results

# récupérer les commentaire lier a un mot
@app.route('/releated',methods = ['POST'])
def releated():
    result = request.json
    phrase=removeStopWords(result['phrase'])
    Comments = []
    print(phrase)
    for mot in phrase :
        results=[]
        synonymes = get_synonymes(mot)
        if mot not in synonymes :
            synonymes.append(mot)
        print(len(synonymes))
        for s in synonymes :
            results.extend(get_comments_from_synonymes(s))

        for com in results:
            if com not in Comments:
                Comments.append(com)
       
    #results = related_comment(mot)
    print(len(Comments))
    
    return json.dumps(Comments, ensure_ascii=False)



app.run()
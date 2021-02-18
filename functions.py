import urllib.request
import pandas as pd
import re
import numpy as np
import spacy
nlp = spacy.load("fr_core_news_sm")
# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et une relation
dictio=[]

def reseauxDump(terme, numRel):

    idDuTerme = -1
    termeURL = terme.replace("é", "%E9").replace("è", "%E8").replace("ê", "%EA").replace(
        "à", "%E0").replace("ç", "%E7").replace("û", "%FB").replace(" ", "+")

    with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}".format(termeURL, numRel)) as url:
        s = url.read().decode('ISO-8859-1')
        line = s.split("\n")

        # words = filterTermesAndRelations(line)

        return formatResault(filterTermesAndRelations(line))


# flitres les liens de la page Html recupérer auprés de Reseaux Dump en
# ne retournant que les lignes de type termes et relation
def filterTermesAndRelations(lines):
    words = []
    regx = "((e;[0-9]+;.*)|(r;[0-9]+;.*))"
    for item in lines:

        x = re.search("((e;[0-9]+;.*)|(r;[0-9]+;.*))", item)
        if x != None:
            words.append(x.group())

    # print(words)
    return words


# crreation d'une liste de dictionaire des mots retourné par Reseaux Dump
def formatResault(lines):
    words = []
    # e;eid;'name';type;w;'formated name'
    # les termes contentant cest carachtéres doivent etre filtrer
    en = "en:"
    sup = ">"
    inf = "<"
    for line in lines:
        casesTermes = line.split(";")
        # on filtre les lignes des relations ainsi que les termes en anglais
        if (not casesTermes[0] == "r" and not en in casesTermes[2] and not sup in casesTermes[2] and not inf in casesTermes[2]):

            if(len(casesTermes) == 6):

                terme1 = casesTermes[2]
                word_dict1 = {"id": int(casesTermes[1]), "t": terme1[1:len(
                    terme1)-1], "nt": casesTermes[3], "w": int(casesTermes[4]), "ft": casesTermes[5]}

                words.append(word_dict1)
            elif (len(casesTermes) == 5):

                terme2 = casesTermes[2]
                word_dict2 = {"id": int(casesTermes[1]), "t": terme2[1:len(
                    terme2)-1], "nt": casesTermes[3], "w": int(casesTermes[4])}
                # print(word_dict)
                words.append(word_dict2)

    # for item in words:
    #     print(item)
    return words


# Récupérer  seulement les terme apartire de chaque dictionaire
def getTermes(word):
    words_list = []
    words_dict = reseauxDump(word, 0)
    for word in words_dict:
        words_list.append(word.get("t"))

    return words_list




def return_token(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte de chaque token
    return [X.text for X in doc]


def pertinence(phrase,comment):
    user =[]
    avis =[]
    for token in return_token(phrase) :
        user.append(1)

    for token in return_token(phrase):
        if token in return_token(comment):
                avis.append(1)
        else : 
            if token in dictio:
                avis.append(1)
            else :
                avis.append(0)
    mult = np.multiply(user,avis)    
    result = np.sum(mult)
    return result

def dictionnaire(phrase):
    for token in return_token(phrase) :
        dictio.append(getTermes(token))
    


def Sortpertinance(phrase,comments):
    dictionnaire(phrase) #améliorer le dictionnaire
    bestComments = []
    pert =[]
    for comment in comments:
        pert.append(pertinence(phrase,comment))

    dico = "{"
    for index,item in enumerate(pert):
        
        dico+="'{}':'{}',".format(index,item)
    size = len(dico)
    dico = dico[0:size-1]
    dico+="}"
    finalDic = eval(dico)
    finalDic = {k: v for k, v in sorted(finalDic.items(), key=lambda item: int(item[1]) ,reverse=True)}
    
    
    print(finalDic)
    for key in finalDic :
        
        if finalDic[key] not in '0':
            bestComments.append(comments[int(key)])
        
    return bestComments

  
            
        


    

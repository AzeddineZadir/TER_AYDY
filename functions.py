import urllib.request
import pandas as pd
import re

# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et une relation


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


# récupérer la liste les mots lies a une liste de mots 
def getAllTermes(words_list):
    words = []
    for word in words_list:
        words.extend(getTermes(word))

    print(words)


# recupérer la liste des vecteurs des commentaires 
def getCommentsVecteurs(words_list):
    comments_list = getCommentes()
    vecteurs_list =[]
    for c in comments_list :
        vecteurs_list.append(creatVecteur(words_list,c))

    print(vecteurs_list)
    return vecteurs_list


# récupérer tous les commentaires du fichier
def getCommentes():
    comments_file = pd.read_csv('comments.txt', header=None)
    commentaires = comments_file[0]
    # liste des commentaires
    comments_list = []
    # tableau d'existance
    comments_existence= []
    for c in commentaires:
        comments_list.append(c)
    # print(comments_list)
    return comments_list    


# retrourner un vecteur d'existance des mot dans le commentaire
def creatVecteur(words_list,comment):
    vecteur = []
    for w in  words_list:
        if w in comment :
            vecteur.append(1)
        else :
            vecteur.append(0)
        # print(vecteur)    
    return vecteur


# creer un vecteur pour les mots de l'utilisateur
def creatUserVecteur(words_list):
    user_vecteur = []
    for w in words_list:
        user_vecteur.append(1)
    return user_vecteur


# avoire la list des scores des commentaires en fonction des mots de 'ljutilisateur
def getCommentsScore(words_list):
    
    liste_score =[]
    score = 0
    user_vecteur= creatUserVecteur(words_list)
    comments_vecteurs = getCommentsVecteurs(words_list)
    
    for i in range(len(comments_vecteurs)):
        
        for j in range(len(user_vecteur)):

            # print(comments_vecteurs[i][j])
            # print(user_vecteur[j])
            score += comments_vecteurs[i][j] * user_vecteur[j]
            # print(f"socre ={score}")
        liste_score.append(score) 
        score = 0   
        
    print(liste_score) 
    return liste_score   
        



import urllib.request
import pandas as pd
from operator import itemgetter
from jdmLink import *
import re




# recupérer la liste des vecteurs des commentaires
def getCommentsVecteurs(words_list):
    comments_list = getCommentes()
    vecteurs_list = []
    for c in comments_list:
        vecteurs_list.append(creatVecteur(words_list, c))

    # print(vecteurs_list)
    return vecteurs_list


# récupérer tous les commentaires du fichier
def getCommentes():
    comments_file = pd.read_csv('comments.txt', header=None)
    commentaires = comments_file[0]
    # liste des commentaires
    comments_list = []
    # tableau d'existance
    comments_existence = []
    for c in commentaires:
        comments_list.append(c)
    # print(comments_list)
    return comments_list


# retrourner un vecteur d'existance des mot dans le commentaire
def creatVecteur(words_list, comment):
    vecteur = []
    for w in words_list:
        if w in comment:
            vecteur.append(1)
        else:
            vecteur.append(0)
        # print(vecteur)
    return vecteur


# creer un vecteur pour les mots de l'utilisateur
def creatUserVecteur(words_list,user_words_list):
    user_vecteur = []
    for w in words_list:
        if w in user_words_list:
            user_vecteur.append(10)
        else :
            user_vecteur.append(1)
    return user_vecteur


# avoire la list des scores des commentaires en fonction des mots de 'ljutilisateur
def getCommentsScore(user_words_list):

    liste_score = []
    score = 0
    commentaires = getCommentes()

    # words_from_JDM = getAllTermes(user_words_list)
    words_from_JDM = getAllTermes(user_words_list)
    # print(f"words from jdm {words_from_JDM}")
    filtered_words = filterVocabulary(words_from_JDM)
    print(f"words filtered  from jdm {filtered_words}")
    user_vecteur = creatUserVecteur(filtered_words,user_words_list)
    comments_vecteurs = getCommentsVecteurs(filtered_words)

    for i in range(len(comments_vecteurs)):

        for j in range(len(user_vecteur)):

            # print(comments_vecteurs[i][j])
            # print(user_vecteur[j])
            score += comments_vecteurs[i][j] * user_vecteur[j]
            # print(f"socre ={score}")
        comment_dict = {"id": i+1, "score": score}
        # ne pas rettourner les commentaires ayant un scor null
        if comment_dict.get("score") != 0:
            liste_score.append(comment_dict)
        score = 0
    # newlist = sorted(liste_score, key=itemgetter('score')) 
    newlist = sorted(liste_score, key=itemgetter('score'), reverse=True)

    print(liste_score)
    print("after sorting ")
    print(newlist)
    return liste_score


def getMyOntologie():
    ontologie = ["hotel", "chambre", "propreté", "literie", "matelas", "drap", "housse",
                 "salle de bain", "lavabo", "douche", "baignoire", "rangement", "décoration", "climatisation"]
    # ontologie = ["chambre", "matelas"]
    return ontologie


def getOntologieDomainsWords():

    ontologie = getMyOntologie()
    domain_words_list = []
    for w in ontologie:
        domain_words_list.extend(getTermesR3(w))

    # print(domain_words_list)
    return domain_words_list


def isRelatedToOntologie(word ,ontologie_words):
    resault = False
    related_domains = getTermesR3(word)
    
    for r in related_domains :
        if r in ontologie_words :
            resault = True
    return resault


def filterWordsByOntologie(words_list):
    words_list_filterd = []
    ontologie_words = getOntologieDomainsWords()
    print(f"le nombre de mots avant le filtrage {len(words_list)}")
    for w in words_list:
        if isRelatedToOntologie(w,ontologie_words):
            words_list_filterd.append(w)

    
    print(f"le nombre de mots aprés le filtrage {len(words_list_filterd)}")
    print(words_list_filterd)
    return words_list_filterd


# Récupérer les mots lier a l'ontologie 
def creatOntologiWordsFiles(ontologie_words):

    for w in ontologie_words : 
        getTermesR0(w)


# récupérer le nombre de fois que un mot est lier au mots de l'ontologie 
def getWordScore(word):
    score = 0
    ontologie = getMyOntologie() 

    for ontologie_word in ontologie :
        # les relations sortontes
        words_list = getTermesR0(ontologie_word)
        if word in words_list :
            score +=1

    # print(f"le score du mot {word} est de {score}")
    return score        


# filtrer la liste des mots passer en paramétre en utilisant leurs score par rapport a la relation 0 et Lontologie 
def filterVocabulary(words_list):
    filterd_words = []
    for w in words_list : 
        score = getWordScore(w)
        if(score>0) : 
            filterd_words.append(w)
    print(f"1 ---nb de mots avant l'application du filtre{len(words_list)}")
    print(f"2 ---nb de mots aprés l'application du filtre{len(filterd_words)}")
    print(filterd_words)

    return(filterd_words)
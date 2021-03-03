import urllib.request
import pandas as pd
import re



# nettoyer le mot avant de le passer dans l'url
def encodeURLTerme(terme):

    url_encode_terme = terme.replace("%", "%25").replace(" ", "%20").replace('""', "%22").replace("#", "%23").replace("$", "%24").replace("&", "%26").replace("'", "%27").replace(
        "(", "%28").replace(")", "%29").replace("*", "%2A").replace("+", "%2B").replace(",", "%2C").replace(";", "%3B").replace("<", "%3C").replace("=", "%3D").replace(">", "%3E").replace("?", "%3F").replace("@", "%40").replace("[", "%5B").replace("]", "%5D").replace("^", "%5E").replace("`", "%60").replace("{", "%7B").replace("|", "%7C").replace("}", "%7D").replace("~", "%7E").replace("¢", "%A2").replace("£", "%A3").replace("¥", "%A5").replace("|", "%A6").replace("§", "%A7").replace("«", "%AB").replace("¬", "%AC").replace("¯", "%AD").replace("º", "%B0").replace("±", "%B1").replace("ª", "%B2").replace(",", "%B4").replace("µ", "%B5").replace("»", "%BB").replace("¼", "%BC").replace("½", "%BD").replace("¿", "%BF").replace("À", "%C0").replace("Á", "%C1").replace("Â", "%C2").replace("Ã", "%C3").replace("Ä", "%C4").replace("Å", "%C5").replace("Æ", "%C6").replace("Ç", "%C7").replace("È", "%C8").replace("É", "%C9").replace("Ê", "%CA").replace("Ë", "%CB").replace("Ì", "%CC").replace("Í", "%CD").replace("Î", "%CE").replace("Ï", "%CF").replace("Ð", "%D0").replace("Ñ", "%D1").replace("Ò", "%D2").replace("Ó", "%D3").replace("Ô", "%D4").replace("Õ", "%D5").replace("Ö", "%D6").replace("Ø", "%D8").replace("Ù", "%D9").replace("Ú", "%DA").replace("Û", "%DB").replace("Ü", "%DC").replace("Ý", "%DD").replace("Þ", "%DE").replace("ß", "%DF").replace("à", "%E0").replace("á", "%E1").replace("â", "%E2").replace("ã", "%E3").replace("ä", "%E4").replace("å", "%E5").replace("æ", "%E6").replace("ç", "%E7").replace("è", "%E8").replace("é", "%E9").replace("ê", "%EA").replace("ë", "%EB").replace("ì", "%EC").replace("í", "%ED").replace("î", "%EE").replace("ï", "%EF").replace("ð", "%F0").replace("ñ", "%F1").replace("ò", "%F2").replace("ó", "%F3").replace("ô", "%F4").replace("õ", "%F5").replace("ö", "%F6").replace("÷", "%F7").replace("ø", "%F8").replace("ù", "%F9").replace("ú", "%FA").replace("û", "%FB").replace("ü", "%FC").replace("ý", "%FD").replace("þ", "%FE").replace("ÿ", "%FF").replace("œ","%8c")
    return url_encode_terme


# verifier si le mots n'est pas déja enregistrer 
def cacheExists(filename):
        
    try :
        with open("jdm_cache/"+filename) as my_file:
            return my_file
    except :
        return False        


# récupérer une liste des mot avec un saut de ligne
def getWordsFromDict(words_dict):
    words_list=[]
    for word_dict_item  in words_dict:
        words_list.append("\n"+word_dict_item)
        # print(word_dict_item)
    
    return words_list

# pour un terme et une relation enregistrer dans un fichier les donnés retourner par la requet sur JDM
def saveWords(terme,numRel,words_dict):
    try :
        filename=terme+"_"+str(numRel)+".txt"
        # print(filename)
        words_list = getWordsFromDict(words_dict)
        # print(words_list)
        with open("jdm_cache/"+filename,mode='w') as my_file:
            my_file.writelines(words_list)
            # print (my_file)
            return my_file        
    except FileNotFoundError as err :
        raise err
        return False    
     
# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et une relation
def reseauxDump(terme, numRel):

    idDuTerme = -1
    filename=terme+"_"+str(numRel)+".txt"
    if (cacheExists(filename)):
        print("cache foound ")
        # je retourne les mots apartire du fichier en qst 
        try :
            with open("jdm_cache/"+filename) as my_file:
                # print (my_file.readlines())
                return formatResault(filterTermesAndRelations(my_file.readlines()))
               
        except :
            print ("pb")
        
    else :
        print("cache not found  ")
        # je lance la requete  j'ecrit le fichier et je retourn les mots 


        with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}".format(encodeURLTerme(terme), numRel)) as url:
            s = url.read().decode('ISO-8859-1')
            line = s.split("\n")

            words = filterTermesAndRelations(line)

            # print(formatResault(filterTermesAndRelations(line)))
            saveWords(terme,numRel,words)
            print(filterTermesAndRelations(line))
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


# Récupérer  seulement les terme apartire de chaque dictionaire pour la relation 0
def getTermesR0(word):
    words_list = []
    words_dict = reseauxDump(word, 0)
    for word in words_dict:
        words_list.append(word.get("t"))
    print(words_list)
    return words_list

# Récupérer les termes  des domaines relatifs au mot cible


def getTermesR3(word):
    words_list = []
    words_dict = reseauxDump(word, 3)
    for word in words_dict:
        words_list.append(word.get("t"))

    return words_list


# récupérer la liste les mots lies a une liste de mots
def getAllTermes(words_list):
    words = []
    for word in words_list:
        words.extend(getTermesR0(word))

    print(f"le nombre de mots retournés {len(words)}")
    return words

# recupérer la liste des vecteurs des commentaires


def getCommentsVecteurs(words_list):
    comments_list = getCommentes()
    vecteurs_list = []
    for c in comments_list:
        vecteurs_list.append(creatVecteur(words_list, c))

    print(vecteurs_list)
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
def creatUserVecteur(words_list):
    user_vecteur = []
    for w in words_list:
        user_vecteur.append(1)
    return user_vecteur


# avoire la list des scores des commentaires en fonction des mots de 'ljutilisateur
def getCommentsScore(words_list):

    liste_score = []
    score = 0
    commentaires = getCommentes()
    words_from_JDM = getAllTermes(words_list)
    user_vecteur = creatUserVecteur(words_from_JDM)
    comments_vecteurs = getCommentsVecteurs(words_from_JDM)

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

    print(liste_score)
    return liste_score


def getOntologieDomainsWords():

    ontologie = ["hotel", "chambre", "propreté", "literie", "matelas", "drap", "housse",
                 "salle de bain", "lavabo", "douche", "baignoire", "rangement", "décoration", "climatisation"]
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
    return words_list_filterd

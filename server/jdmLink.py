
import urllib.request
import pandas as pd
from operator import itemgetter
import re
import os
# nettoyer le mot avant de le passer dans l'url


   def encodeURLTerme(terme):

    url_encode_terme = terme.replace("%", "%25").replace(" ", "%20").replace('""', "%22").replace("#", "%23").replace("$", "%24").replace("&", "%26").replace("'", "%27").replace(
        "(", "%28").replace(")", "%29").replace("*", "%2A").replace("+", "%2B").replace(",", "%2C").replace(";", "%3B").replace("<", "%3C").replace("=", "%3D").replace(">", "%3E").replace("?", "%3F").replace("@", "%40").replace("[", "%5B").replace("]", "%5D").replace("^", "%5E").replace("`", "%60").replace("{", "%7B").replace("|", "%7C").replace("}", "%7D").replace("~", "%7E").replace("¢", "%A2").replace("£", "%A3").replace("¥", "%A5").replace("|", "%A6").replace("§", "%A7").replace("«", "%AB").replace("¬", "%AC").replace("¯", "%AD").replace("º", "%B0").replace("±", "%B1").replace("ª", "%B2").replace(",", "%B4").replace("µ", "%B5").replace("»", "%BB").replace("¼", "%BC").replace("½", "%BD").replace("¿", "%BF").replace("À", "%C0").replace("Á", "%C1").replace("Â", "%C2").replace("Ã", "%C3").replace("Ä", "%C4").replace("Å", "%C5").replace("Æ", "%C6").replace("Ç", "%C7").replace("È", "%C8").replace("É", "%C9").replace("Ê", "%CA").replace("Ë", "%CB").replace("Ì", "%CC").replace("Í", "%CD").replace("Î", "%CE").replace("Ï", "%CF").replace("Ð", "%D0").replace("Ñ", "%D1").replace("Ò", "%D2").replace("Ó", "%D3").replace("Ô", "%D4").replace("Õ", "%D5").replace("Ö", "%D6").replace("Ø", "%D8").replace("Ù", "%D9").replace("Ú", "%DA").replace("Û", "%DB").replace("Ü", "%DC").replace("Ý", "%DD").replace("Þ", "%DE").replace("ß", "%DF").replace("à", "%E0").replace("á", "%E1").replace("â", "%E2").replace("ã", "%E3").replace("ä", "%E4").replace("å", "%E5").replace("æ", "%E6").replace("ç", "%E7").replace("è", "%E8").replace("é", "%E9").replace("ê", "%EA").replace("ë", "%EB").replace("ì", "%EC").replace("í", "%ED").replace("î", "%EE").replace("ï", "%EF").replace("ð", "%F0").replace("ñ", "%F1").replace("ò", "%F2").replace("ó", "%F3").replace("ô", "%F4").replace("õ", "%F5").replace("ö", "%F6").replace("÷", "%F7").replace("ø", "%F8").replace("ù", "%F9").replace("ú", "%FA").replace("û", "%FB").replace("ü", "%FC").replace("ý", "%FD").replace("þ", "%FE").replace("ÿ", "%FF").replace(u"\x9c", "oe").replace(u"\xb0","&deg;")
    return url_encode_terme


# verifier si le mots n'est pas déja enregistrer
def cacheExists(filename):

    try:
        with open("jdm_cache/"+filename) as my_file:
            return my_file
    except:
        return False


# pour un terme et une relation enregistrer dans un fichier les donnés retourner par la requet sur JDM
def saveWords(terme, numRel, words_dict):
    try:
        filename = terme+"_"+str(numRel)+".txt"
        # print(filename)
        words_list = getWordsFromDict(words_dict)
        # print(words_list)
        if(os.path.exists('./jdm_cache')==False):
            os.mkdir("./jdm_cache")
        with open("jdm_cache/"+filename, mode='w', encoding="utf-8") as my_file:
            my_file.writelines(words_list)
            # print (my_file)
            return my_file
    except FileNotFoundError as err:
        raise err
        return False


# récupérer une liste des mot avec un saut de ligne
def getWordsFromDict(words_dict):
    words_list = []
    for word_dict_item in words_dict:
        words_list.append("\n"+word_dict_item)
        # print(word_dict_item)

    return words_list


# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et une relation
def reseauxDump(terme, numRel):
    # print(terme+" "+str(numRel))

    idDuTerme = -1
    filename = terme+"_"+str(numRel)+".txt"
    if (cacheExists(filename)):
        # print("cache exists ")
        # je retourne les mots apartire du fichier en qst
        try:
            with open("jdm_cache/"+filename, encoding="utf-8") as my_file:
                # print (my_file.readlines())
                return formatResault(filterTermesAndRelations(my_file.readlines()))

        except:
            print("problem while oppening file ")

    else:
        print("cache not found  ")
        # je lance la requete  j'ecrit le fichier et je retourn les mots

        with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}".format(encodeURLTerme(terme), numRel)) as url:
            s = url.read().decode('ISO-8859-1')
            line = s.split("\n")

            words = filterTermesAndRelations(line)

            # print(formatResault(filterTermesAndRelations(line)))
            saveWords(terme, numRel, words)
            # print(filterTermesAndRelations(line))

            return formatResault(filterTermesAndRelations(line))


# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et
# une relation (seulment les relations sortantes sont prises en comptes )
def reseauxDumpByRelation4(terme):
    print(terme)
    idDuTerme = -1
    filename = terme+"_"+str(4)+".txt"
    if (cacheExists(filename)):
        # print("cache exists ")
        # je retourne les mots apartire du fichier en qst
        try:
            with open("jdm_cache/"+filename, encoding="utf-8") as my_file:
                # print (my_file.readlines())
                return formatResaultByRelation4(filterTermesAndRelations(my_file.readlines()))

        except:
            print("problem while oppening file ")

    else:
        print("cache not found  ")
        # je lance la requete  j'ecrit le fichier et je retourn les mots

        with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}".format(encodeURLTerme(terme), 4)) as url:
            s = url.read().decode('ISO-8859-1')
            line = s.split("\n")

            words = filterTermesAndRelations(line)

            # print(formatResault(filterTermesAndRelations(line)))
            saveWords(terme, 4, words)
            # print(filterTermesAndRelations(line))

            return formatResaultByRelation4(filterTermesAndRelations(line))


def reseauxDumpByRelations(terme, numRel):

    idDuTerme = -1
    filename = terme+"_"+str(numRel)+".txt"
    # print(filename)
    if (cacheExists(filename)):
        # print("cache exists ")
        # je retourne les mots apartire du fichier en qst
        try:
            with open("jdm_cache/"+filename, encoding="utf-8") as my_file:
                # print (my_file.readlines())
                return formatResaultByRelation(filterTermesAndRelations(my_file.readlines()))

        except:
            print("problem while oppening file ")

    else:
        print("cache not found  ")
        # je lance la requete  j'ecrit le fichier et je retourn les mots

        with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}".format(encodeURLTerme(terme), numRel)) as url:
            s = url.read().decode('ISO-8859-1')
            line = s.split("\n")

            words = filterTermesAndRelations(line)
            # print(words)
            # print(formatResault(filterTermesAndRelations(line)))
            saveWords(terme, numRel, words)
            # print(filterTermesAndRelations(line))

            return formatResaultByRelation(filterTermesAndRelations(line))


# flitres les liens de la page Html recupérer auprés de Reseaux Dump en
# ne retournant que les lignes de type termes et relation
def filterTermesAndRelations(lines):
    words = []
    en = "en:"
    sup = ">"
    inf = "<"
    regx = "((e;[0-9]+;.*)|(r;[0-9]+;.*))"
    for item in lines:

        x = re.search("((e;[0-9]+;.*)|(r;[0-9]+;.*))", item)
        if x != None and not en in x.group() and not sup in x.group() and not "_COM"in x.group():
        
            # print(x.group())
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
    p2 = ":"
    for line in lines:
        casesTermes = line.split(";")
        # on filtre les lignes des relations ainsi que les termes en anglais
        if (not casesTermes[0] == "r" and not en in casesTermes[2] and not sup in casesTermes[2] and not inf in casesTermes[2] and not "_COM" in casesTermes[2] and not p2 in casesTermes[2]):

            if(len(casesTermes) == 6):

                terme1 = casesTermes[2]
                word_dict1 = {"id": int(casesTermes[1]), "t": terme1[1:len(
                    terme1)-1], "nt": casesTermes[3], "w": float(casesTermes[4]), "ft": casesTermes[5]}

                words.append(word_dict1)
            elif (len(casesTermes) == 5):

                terme2 = casesTermes[2]
                word_dict2 = {"id": int(casesTermes[1]), "t": terme2[1:len(
                    terme2)-1], "nt": casesTermes[3], "w": float(casesTermes[4])}
                # print(word_dict)

                words.append(word_dict2)

    # for item in words:
    #     print(item)
    return words


# crreation d'une liste de dictionaire des mots retourné par les relations
def formatResaultByRelation4(lines):
    words = []
    # e;eid;'name';type;w;'formated name'
    # les termes contentant cest carachtéres doivent etre filtrer
    en = "en:"
    sup = ">"
    inf = "<"
    for line in lines:
        casesTermes = line.split(";")
        # on filtre les lignes des relations ainsi que les termes en anglais
        if (not casesTermes[0] == "r" and not en in casesTermes[2] and not sup in casesTermes[2] and not inf in casesTermes[2] and not "_COM" in casesTermes[2]):
            if(len(casesTermes) == 6):
                terme1 = casesTermes[2]
                word_dict1 = {"id": int(casesTermes[1]), "t": terme1[1:len(
                    terme1)-1], "nt": casesTermes[3], "w": float(casesTermes[4]), "ft": casesTermes[5]}

                words.append(word_dict1)
            elif (len(casesTermes) == 5):
                terme2 = casesTermes[2]
                word_dict2 = {"id": int(casesTermes[1]), "t": terme2[1:len(
                    terme2)-1], "nt": casesTermes[3], "w": float(casesTermes[4])}
                # print(word_dict)
                words.append(word_dict2)
    returned_words_dict = []
    searched_word = {"id": words[0].get(
        "id"), "t": words[0].get("t"), "rw": float(999)}
    # print(f"searched word {searched_word}")
    for line1 in lines:
        splitedTermes = line1.split(";")
        # on filtre les relations sortoantes et on produits la liste des mot qui sont lier au mot concérner
        if (splitedTermes[0] == "r" and int(splitedTermes[2]) == words[0].get("id") and len(splitedTermes) == 6 and int(splitedTermes[3]) != 239128):
            id_terme1 = int(splitedTermes[2])
            id_terme2 = int(splitedTermes[3])
            if(splitedTermes[5] != "w"):
                weight = float(splitedTermes[5])
            else:
                weight = 0
            # relation terme1---------> terme2
            relation_dict = {"id": id_terme2, "t": getTermeById(
                id_terme2, words), "rw": weight}
            returned_words_dict.append(relation_dict)
        # supprimer les temres non retrouver
    res = list(filter(lambda i: i['t'] != None, returned_words_dict))
    res.append(searched_word)
    # print (res)
    # print(len(res))
    return res


def formatResaultByRelation(lines):

    words = []
    # e;eid;'name';type;w;'formated name'
    # les termes contentant cest carachtéres doivent etre filtrer
    en = "en:"
    p2 = ":"
    sup = ">"
    inf = "<"
    for line in lines:
        casesTermes = line.split(";")
        # on filtre les lignes des relations ainsi que les termes en anglais
        if (not casesTermes[0] == "r" and not en in casesTermes[2] and not sup in casesTermes[2] and not inf in casesTermes[2] and not "_COM" in casesTermes[2] and not p2 in casesTermes[2]):

            if(len(casesTermes) == 6):

                terme1 = casesTermes[2]
                word_dict1 = {"id": int(casesTermes[1]), "t": terme1[1:len(
                    terme1)-1], "nt": casesTermes[3], "w": float(casesTermes[4]), "ft": casesTermes[5]}

                words.append(word_dict1)
            elif (len(casesTermes) == 5):

                terme2 = casesTermes[2]
                word_dict2 = {"id": int(casesTermes[1]), "t": terme2[1:len(
                    terme2)-1], "nt": casesTermes[3], "w": float(casesTermes[4])}
                # print(word_dict)
                words.append(word_dict2)

    # print(words)
    if words:
        returned_words_dict = []

        searched_word = {"id": words[0].get(
            "id"), "t": words[0].get("t"), "rw": float(999)}
        # print(f"searched word {searched_word}")
        for line1 in lines:
            splitedTermes = line1.split(";")

            # on filtre les relations sortoantes et on produits la liste des mot qui sont lier au mot concérner
            if (splitedTermes[0] == "r" and int(splitedTermes[2]) == words[0].get("id") and len(splitedTermes) == 6 and int(splitedTermes[3]) != 239128):
                id_terme1 = int(splitedTermes[2])
                id_terme2 = int(splitedTermes[3])
                if(splitedTermes[5] != "w"):
                    weight = float(splitedTermes[5])
                else:
                    weight = 0
                # relation terme1---------> terme2

                relation_dict = {"id": id_terme2, "t": getTermeById(
                    id_terme2, words), "rw": weight}
                returned_words_dict.append(relation_dict)
                # print(relation_dict)

            # supprimer les temres non retrouver
        res = list(filter(lambda i: i['t'] != None, returned_words_dict))
        res.append(searched_word)
        # print (res)
        # print(len(res))

        return res
    return []

def getTermeById(id, words):
    for w in words:
        if (id == w["id"]):
            return w["t"]
            break


# récupérer la liste les mots lies a une liste de mots
def getAllTermesR0(words_list):
    words = []
    for word in words_list:
        # words.extend(getTermesR0(word))
        words.extend(getTermesR0(word))

    print(f"le nombre de mots retournés {len(words)}")
    return words


def getAllTermesR0Sortant(words_list):
    words = []
    for word in words_list:
        # words.extend(getTermesR0(word))
        words.extend(getTermesR0(word))
    print(f"le nombre de mots retournés {len(words)}")
    return words

def getAllTermesR5(words_list):
    words = []
    for word in words_list:
        # words.extend(getTermesR0(word))
        words.extend(getTermesR5(word))
    return words

# Récupérer  seulement les terme apartire de chaque dictionaire pour la relation 0
def getTermesR0(word):
    words_list = []
    words_dict = reseauxDump(word, 0)
    for w in words_dict:
        if (w["t"] != word):
            words_list.append(w.get("t"))
    # print(words_list)
    return words_list


# Récupérer  seulement les terme sortant  apartire de chaque dictionaire pour la relation 0
def getTermesR0Sortants(word):
    words_list = []
    words_dict = reseauxDumpByRelations(word, 0)

    # print (words_dict)
  
    for word in words_dict:
        words_list.append(word.get("t"))
        #print(word)
    return words_list

def getTermesR5Sortants(word):
    words_list = []
    words_dict = reseauxDumpByRelations(word, 5)

    #print (words_dict)
  
    for word in words_dict:
        words_list.append(word.get("t"))
        #print(word)
    return words_list
# Récupérer les termes  des domaines relatifs au mot cible
def getTermesR3(word):
    words_list = []
    words_dict = reseauxDump(word, 3)
    for word in words_dict:
        words_list.append(word.get("t"))

    return words_list


def getTermesR5(word):
    words_list = []
    words_dict = reseauxDump(word, 5)
    for w in words_dict:
        if (w["t"] != word):
            words_list.append(w.get("t"))
    # print(words_list)
    return words_list


def getTermesR6(word):
    words_list = []
    words_dict = reseauxDump(word, 6)
    for w in words_dict:
        if (w["t"] != word):
            words_list.append(w.get("t"))
    # print(words_list)
    return words_list


def getTermesR9(word):
    words_list = []
    words_dict = reseauxDump(word, 9)
    for w in words_dict:
        if (w["t"] != word):
            words_list.append(w.get("t"))
    # print(words_list)
    return words_list


def getTermesR36(word):
    words_list = []
    words_dict = reseauxDumpByRelations(word, 36)
    neg = ["_POL-NEG_PC", "_POL-NEG"]
    pos = ["_POL-POS_PC", "_POL-POS"]
    neutre = ["_POL-NEUTRE_PC", "_POL-NEUTRE"]
    max = 0
    _word = ""
    for word_dict in words_dict:
        if word_dict["rw"] > max and word_dict["t"] != word:
            max = word_dict["rw"]
            _word = word_dict["t"]

    if(_word in neg):
        return "_POL-NEG"
    elif _word in pos:
        return "_POL-POS"
    else:
        return "_POL-NEUTRE"
    return _word


def getTermesR19(word):
    words_list = []
    words_dict = reseauxDumpByRelations(word, 19)
    max = 0
    _word = ""
    for word_dict in words_dict:
        if word_dict["rw"] > max and word_dict["t"] != word:
            max = word_dict["rw"]
            _word = word_dict["t"]

    if not _word:
        return word
    return _word


def getTermesR4(word):
    if word == "":
        return 
    # cette fonction retourne la POS d'un mot grace a la relation 4  Exemple soin -> Nom
    words_dict = reseauxDumpByRelation4(word)
    Ver = ["VerInf", "VerConjug", "VerPPas", "VerIImp+SG+P3"]
    Nom = ["NomFem+SG", "GNDET", "GN", "NomMas+SG"]
    Det = ["ProPersCOI", "AdjPos", "DetInvGen+PL"]
    Pro = ["Unit", "ProPers", "ProPersSUJ", "ProSG+P1"]
    Adj = ["AdjInvGen+SG", "AdjFem+SG"]

    notInteressed = ["Number:Sing", "Gender:Fem", "Ukn:"]
    max = 0
    _word = ""
    
    for word_dict in words_dict:
        # print(words_dict)
        if word_dict["rw"] >= max and word_dict["t"] != word and word_dict["t"] not in notInteressed:
            max = word_dict["rw"]
            _word = word_dict["t"].replace(':', '')
            if _word in Ver:
                _word = "Ver"
            elif _word in Nom:
                _word = "Nom"
            elif _word in Det:
                _word = "Det"
            elif _word in Pro:
                _word = "Pro"
            elif _word in Adj:
                _word = "Adj"
    return _word

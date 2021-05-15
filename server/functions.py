import urllib.request
import pandas as pd
from operator import itemgetter
from jdmLink import *
import re
import json
import time
import stanza
import deplacy





def createVectors(Comments):
    Vector = []
    
    return Vector

# recupérer la liste des vecteurs des commentaires
def getCommentsVecteurs(words_list):
    comments_list = getCommentes()
    Comment = []
    print(comments_list)
    for comment in comments_list :
        Comment.append(comment.split(";")[1])
    vecteurs_list = []
    for c in Comment:
        # print(c)
        vecteurs_list.append(creatVecteur(words_list, c))
    # print(vecteurs_list)
    return vecteurs_list


# récupérer tous les commentaires du fichier
def getCommentes():
    comments_file = pd.read_csv('./src/comments.txt', encoding="utf-8", header=None,delimiter = "\n")
    commentaires = comments_file[0]
    # liste des commentaires
    comments_list = []
    # tableau d'existance
    comments_existence = []
    for c in commentaires:
        comments_list.append(c.lower())
    # print(comments_list)
    return comments_list

def getHotels():
    hotels_file = pd.read_csv('./src/hotels.txt', encoding="utf-8", header=None)
    hotels = hotels_file[0]
    # liste des commentaires
    hotels_list = []
    # tableau d'existance
    hotels_existence = []
    for c in hotels:
        hotels_list.append(c)
    # print(comments_list)
    return hotels_list

def getCommentById(id):
    Comments = getCommentes()
    for comment in Comments:
        CommentId = comment.split(";")[0]
        if str(CommentId)==str(id):
            return comment
        

# retrourner un vecteur d'existance des mot dans le commentaire
def creatVecteur(words_list, comment):
    vecteur = []
    # print(comment)
    comments_words_list = comment.split(" ")
    for w in words_list:
        found = False
        for c_w in comments_words_list:
            # print(f" {w['t']}========{c_w} ")
            if w["t"] == c_w:
                found = True
        if(found):
            vecteur.append(1)
        else:
            vecteur.append(0)

    # print(f"word list len  {len(vecteur)}")
    return vecteur


# creer un vecteur pour les mots de l'utilisateur
def creatUserVecteur(words_list, user_words_list):
    user_vecteur = []
    for w in words_list:
        if w['t'] in user_words_list:
            user_vecteur.append(14)
        else:
            user_vecteur.append(w["score"])
    return user_vecteur


# avoire la list des scores des commentaires en fonction des mots de 'ljutilisateur
def getCommentsScore(user_words_list,selectors):
    liste_score = []
    score = 0
    commentaires = getCommentes()
    
    # words_from_JDM = getAllTermes(user_words_list)
    words_from_JDM = getAllTermesR0(user_words_list)
    # print(f"1_______________words from jdm {words_from_JDM}")
    
    filtered_words = filterVocabulary(words_from_JDM)
    # print(len(filtered_words))
    user_words_list.extend(selectors)
    all_words = addUserWords(filtered_words, user_words_list)
    
 
    # print(len(all_words))
    # print(all_words)
    # print(filtered_words)
    # print(f"2_______________words filtered  from jdm {filtered_words}")
    user_vecteur = creatUserVecteur(all_words, user_words_list)
    # print(len(user_vecteur))
    comments_vecteurs = getCommentsVecteurs(all_words)
    # print (len(comments_vecteurs[0]))
    # print(user_vecteur)
    for i in range(len(comments_vecteurs)):

        for j in range(len(user_vecteur)):

            # print(comments_vecteurs[i][j])
            # print(user_vecteur[j])
            score += comments_vecteurs[i][j] * user_vecteur[j]
            # print(f"socre ={score}")
        comment_dict = {"comment": getCommentById(i+1), "score": score}
        # ne pas rettourner les commentaires ayant un scor null
        if comment_dict.get("score") != 0:
            liste_score.append(comment_dict)
        score = 0
    # newlist = sorted(liste_score, key=itemgetter('score'))
    newlist = sorted(liste_score, key=itemgetter('score'), reverse=True)

    # print(liste_score)
    # print("after sorting ")
    print(newlist)
    return liste_score


def getCommentsScoreSortant(user_words_list):

    liste_score = []
    score = 0
    commentaires = getCommentes()

    # words_from_JDM = getAllTermes(user_words_list)
    words_from_JDM = getAllTermesR0(user_words_list)
    # print(f"1_______________words from jdm {words_from_JDM}")
    filtered_words = filterVocabulary(words_from_JDM)
    # print(len(filtered_words))
    all_words = addUserWords(filtered_words, user_words_list)
    # print(len(all_words))
    # print(all_words)
    # print(filtered_words)
    # print(f"2_______________words filtered  from jdm {filtered_words}")
    user_vecteur = creatUserVecteur(all_words, user_words_list)
    # print(len(user_vecteur))
    comments_vecteurs = getCommentsVecteurs(all_words)
    # print (len(comments_vecteurs[0]))
    # print(user_vecteur)
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

    # print(liste_score)
    # print("after sorting ")
    print(newlist)
    return liste_score


def addUserWords(filtered_words, user_words_list):
    compteur = 0
    for word in user_words_list:
        filtered_words.insert(compteur, {"t": word, "score": 100})
        compteur += 1
    return filtered_words


def getMyOntologie():
    ontologie = ["hôtel", "chambre", "propreté", "literie", "matelas", "drap", "housse", "taie",
                 "salle de bain", "lavabo", "douche", "baignoire", "rangement", "décoration",
                 "climatisation", "sommier", "lit bébé", "bidet", "glace", "serviette", "toilettes",
                 "télévision", "coffre", "bar", "décoration", "terrasse", "ménage", "restauration",
                 "petit déjeuner", "café", "thé", "chocolat", "viennoiserie", "repas", "buffet",
                 "demi pension", "pension complète", "boisson", "cuisinier", "service", "serveur", "spa",
                 "sauna", "jacuzzi", "salle de sport", "internet", "escalier", "ascenseur", "accueil",
                 "disponibilité", "animation", "soirée", "excursion", "accès", "accès handicapé", "parking",
                 "cadre", "jardin", "piscine", "plage", "bruit"]
    # ontologie = ["chambre", "matelas"]
    return ontologie


def getOntologieDomainsWords():

    ontologie = getMyOntologie()
    domain_words_list = []
    for w in ontologie:
        domain_words_list.extend(getTermesR3(w))

    # print(domain_words_list)
    return domain_words_list


def isRelatedToOntologie(word, ontologie_words):
    resault = False
    related_domains = getTermesR0(word)

    for r in related_domains:
        if r in ontologie_words:
            resault = True
    return resault


def filterWordsByOntologie(words_list):
    words_list_filterd = []
    ontologie_words = getOntologieDomainsWords()
    print(f"le nombre de mots avant le filtrage {len(words_list)}")
    for w in words_list:
        if isRelatedToOntologie(w, ontologie_words):
            words_list_filterd.append(w)

    print(f"le nombre de mots aprés le filtrage {len(words_list_filterd)}")
    # print(words_list_filterd)
    return words_list_filterd


# Récupérer les mots lier a l'ontologie
def creatOntologiWordsFiles(ontologie_words):

    for w in ontologie_words:
        getTermesR5(w)


# récupérer le nombre de fois que un mot est lier au mots de l'ontologie
def getWordScore(word):
    score = 0
    ontologie = getMyOntologie()

    for ontologie_word in ontologie:
        # les relations sortontes
        words_list = getTermesR0Sortants(ontologie_word)
        if(len(words_list)!=0):
            if word in words_list:
                score += 1

    # print(f"le score du mot {word} est de {score}")
    return score


# filtrer la liste des mots passer en paramétre en utilisant leurs score par rapport a la relation 0 et Lontologie
def filterVocabulary(words_list):
    filterd_words = []
    if len(words_list)!=0:
        
        the_word = words_list[0]
        for w in words_list:

            score = getWordScore(w)
            if(score > 0):
                word_dict = {"t": w, "score": score}
                filterd_words.append(word_dict)

        print(f" the worde him self {the_word}")
        print(f"1 ---nb de mots avant l'application du filtre{len(words_list)}")
        print(f"2 ---nb de mots aprés l'application du filtre{len(filterd_words)}")
        # print(filterd_words)
        # print(filterd_words)

        return(filterd_words)
    return []

# creaion du fichier json de l'ontologie
def creatOntologieJson():
    onto_words = getMyOntologie()
    onto_list = []

    for o_word in onto_words:

        o_dict = {"t": o_word, "syno": getTermesR5(o_word), "r_isa": getTermesR6(
            o_word), "has_part": getTermesR9(o_word), "score": 0}
        onto_list.append(o_dict)

    try:
        filename = "./src/hotel_ontologie.json"

        # print(words_list)
        with open(filename, mode='w', encoding="utf-8") as my_file:

            json.dump(onto_list, my_file, indent=4)
            return my_file
    except FileNotFoundError as err:
        raise err
        return False



def gets_rid_of_empty_quotes(lst):
    while len(lst)-1 >= 0 and lst[len(lst)-1] == '':
        lst = lst[:len(lst)-1]
    while len(lst)-1 >= 0 and lst[0] == '':
        lst = lst[1:]
    browser = 1
    while '' in lst and browser < len(lst):
        while lst[browser] == '':
            if browser-1 == 0:
                c = [lst[0]]
            else:
                c = lst[:browser]
            lst = c + lst[browser+1:]
        browser += 1
    return lst


# lst contains words
def clean_expr_from_additionals(expression):
    strings = re.split(
        '[\\\\\n\t\b\"`\a\f\r²~\"#\'"{"" ""("")""}"@!§"|"_"+""*""/""=";,?.:µ\[\]]{1}', expression)
    strings = gets_rid_of_empty_quotes(strings)

    return strings
#


def gets_rid_of_dashes(lst):
    browser = 0
    l = []
    for word in lst:
        
        if re.search('^-\'+[a-z]*-*$|^-*[a-z]*-+$', word):
            word = re.split('-', word)
            l = l + word
        else:
            l = l + [word]
        browser += 1
    l = gets_rid_of_empty_quotes(l)
    return l


def cleanSpecialChar(str):
    regex = r"([^\wÀ-úÀ-ÿ][^\wÀ-úÀ-ÿ]+)|[\/:-@\[-\`{-~$]"
    res = re.sub(regex, " ", str, 0, re.MULTILINE)
    return res


def list_to_string(lst):
    return " ".join(lst)

# all composed words are detected


def composed_words(expression):
    expression = clean_expr_from_additionals(expression)
    lst = gets_rid_of_dashes(expression)
    resulting_list = []
    browser = 0
    len_longest_composed_word = -1
    index_of_latest_cw = -1
    counter = 0
    skip = -1
    leave = 0
    b = 0
    i = ii = iii = 0
    while browser < len(lst):
        if skip != -1 and browser > skip:
            skip = -1
            leave = len(resulting_list)
        related_composed_words = reseauxDump(lst[browser], 11)
        rcw_browser = 1
        if related_composed_words != None:
            rcw_len = len(related_composed_words)
            len_rl_before = len(resulting_list)
            while rcw_browser < rcw_len:
                composed_word = related_composed_words[rcw_browser]['t']
                cleaned_composed_word = clean_expr_from_additionals(
                    composed_word)
                cw_len = len(cleaned_composed_word)
                if cleaned_composed_word != [] and (lst[browser:cw_len+browser] == cleaned_composed_word):
                    index_of_latest_cw = len(resulting_list)
                    if (composed_word not in resulting_list[leave:len(resulting_list)]) or skip == -1:
                        resulting_list += [composed_word]
                        if skip == -1 or browser < skip:
                            var = browser
                        else:
                            var = skip

                        skip = max(
                            skip, len(cleaned_composed_word)+var-1)  # -1
                    else:
                        if skip == -1 or browser > skip:
                            resulting_list += [composed_word]

                    len_longest_composed_word = max(
                        len_longest_composed_word, browser+len(cleaned_composed_word))
                if browser != 0:
                    if lst[browser] in cleaned_composed_word:
                        i = cleaned_composed_word.index(lst[browser])
                        ii = len(cleaned_composed_word[:i])
                        iii = len(cleaned_composed_word[i:])
                    if (cleaned_composed_word != [] and ((lst[browser-ii:browser+iii]) == cleaned_composed_word)):
                        if (composed_word not in resulting_list[leave:len(resulting_list)]) or skip == -1:
                            resulting_list += [composed_word]
                            if skip == -1 or browser <= skip:
                                var = browser-ii
                            else:
                                var = skip

                            if skip == -1:
                                b = browser
                            skip = max(
                                skip, len(cleaned_composed_word)+var-1)  # -1
                        else:
                            if skip == -1 or browser > skip:
                                resulting_list += [composed_word]
                        while len(resulting_list[len(resulting_list)-2].split(" ")) == 1 and resulting_list[len(resulting_list)-2].split(" ")[0] in resulting_list[len(resulting_list)-1].split(" "):
                            resulting_list = resulting_list[:len(
                                resulting_list)-2]+resulting_list[len(resulting_list)-1:]
                        index_of_latest_cw = len(resulting_list)-1
                        len_longest_composed_word = max(
                            len_longest_composed_word, browser-ii+len(cleaned_composed_word))
                rcw_browser += 1
            if len_rl_before == len(resulting_list) and browser >= len_longest_composed_word:
                resulting_list += [lst[browser]]
                last_added_is_a_cw = False
        browser += 1
    return resulting_list


# the composed words that are in a bigger composed word are deleted
def composed_words_cleaner_version(expression):
    expression = clean_expr_from_additionals(expression)
    lst = gets_rid_of_dashes(expression)
    resulting_list = []
    browser = 0
    len_longest_composed_word = -1
    index_of_latest_cw = -1
    counter = 0
    skip = -1
    leave = 0
    i = ii = iii = 0
    b = 0
    while browser < len(lst):
        if skip != -1 and browser > skip:
            skip = -1
            leave = len(resulting_list)
        related_composed_words = reseauxDump(lst[browser], 11)
        rcw_browser = 1
        if related_composed_words != None:
            rcw_len = len(related_composed_words)
            len_rl_before = len(resulting_list)
            while rcw_browser < rcw_len:
                composed_word = related_composed_words[rcw_browser]['t']
                cleaned_composed_word = clean_expr_from_additionals(
                    composed_word)
                cw_len = len(cleaned_composed_word)
                if cleaned_composed_word != [] and (lst[browser:cw_len+browser] == cleaned_composed_word):
                    index_of_latest_cw = len(resulting_list)
                    if (composed_word not in resulting_list[leave:len(resulting_list)]) or skip == -1:
                        l = len(resulting_list[leave:len(resulting_list)])
                        if l == 0 and len(resulting_list) == 0:
                            resulting_list += [composed_word]
                        else:
                            if (len(resulting_list) != 0 and (composed_word != resulting_list[len(resulting_list)-1]) and
                                    composed_word not in resulting_list[len(resulting_list)-1]):
                                if resulting_list[len(resulting_list)-1] in composed_word:
                                    resulting_list[len(
                                        resulting_list)-1] = composed_word
                                else:
                                    resulting_list += [composed_word]
                        if skip == -1 or browser < skip:
                            var = browser
                        else:
                            var = skip
                        skip = max(
                            skip, len(cleaned_composed_word)+var-1)  # -1
                    else:
                        if skip == -1 or browser > skip:
                            l = len(resulting_list[leave:len(resulting_list)])
                            if l == 0:
                                resulting_list += [composed_word]
                            else:
                                if (len(resulting_list) != 0 and (composed_word != resulting_list[len(resulting_list)-1]) and
                                        composed_word not in resulting_list[len(resulting_list)-1]):
                                    if resulting_list[len(resulting_list)-1] in composed_word:
                                        resulting_list[len(
                                            resulting_list)-1] = composed_word
                                    else:
                                        resulting_list += [composed_word]
                    len_longest_composed_word = max(
                        len_longest_composed_word, browser+len(cleaned_composed_word))
                if browser != 0:
                    if lst[browser] in cleaned_composed_word:
                        i = cleaned_composed_word.index(lst[browser])
                        ii = len(cleaned_composed_word[:i])
                        iii = len(cleaned_composed_word[i:])
                    if (cleaned_composed_word != [] and ((lst[browser-ii:browser+iii]) == cleaned_composed_word)):
                        if (composed_word not in resulting_list[leave:len(resulting_list)]) or skip == -1:
                            l = len(resulting_list[leave:len(resulting_list)])
                            if len(resulting_list) != 0 and composed_word not in resulting_list[len(resulting_list)-1]:
                                if l == 0 or len(resulting_list) == 0:
                                    resulting_list += [composed_word]
                                else:
                                    if (len(resulting_list) != 0 and (composed_word != resulting_list[len(resulting_list)-1]) and
                                            composed_word not in resulting_list[len(resulting_list)-1]):
                                        if resulting_list[len(resulting_list)-1] in composed_word:
                                            resulting_list[len(
                                                resulting_list)-1] = composed_word
                                        else:
                                            resulting_list += [composed_word]
                            if skip == -1 or browser <= skip:
                                var = browser-ii
                            else:
                                var = skip

                            if skip == -1:
                                b = browser
                            skip = max(
                                skip, len(cleaned_composed_word)+var-1)  # -1
                        else:
                            if skip == -1 or browser > skip:
                                l = len(
                                    resulting_list[leave:len(resulting_list)])
                                if l == 0:
                                    resulting_list += [composed_word]
                                else:
                                    if (len(resulting_list) != 0 and (composed_word != resulting_list[len(resulting_list)-1]) and
                                            composed_word not in resulting_list[len(resulting_list)-1]):
                                        if resulting_list[len(resulting_list)-1] in composed_word:
                                            resulting_list[len(
                                                resulting_list)-1] = composed_word
                                        else:
                                            resulting_list += [composed_word]
                        if (len(resulting_list) >= 2):
                            while (len(resulting_list[len(resulting_list)-2].split(" ")) == 1
                                   and resulting_list[len(resulting_list)-2].split(" ")[0] in resulting_list[len(resulting_list)-1].split(" ")
                                   and skip != -1):
                                resulting_list = resulting_list[:len(
                                    resulting_list)-2]+resulting_list[len(resulting_list)-1:]
                        index_of_latest_cw = len(resulting_list)-1
                        len_longest_composed_word = max(
                            len_longest_composed_word, browser-ii+len(cleaned_composed_word))
                rcw_browser += 1
            if len_rl_before == len(resulting_list) and browser >= len_longest_composed_word:
                resulting_list += [lst[browser]]
                last_added_is_a_cw = False
        browser += 1
    return resulting_list



def posTagging(sentence):
    if sentence == "":
        return []
    expression = clean_expr_from_additionals(sentence)
    phrases = gets_rid_of_dashes(expression)
    print(phrases)
    #phrases = re.split("\.|,", sentence)  # re => Regular Expression
    # print(phrases)
    array = []
    for phrase in phrases:
        
        tokens = phrase.split(" ")
        arrayPos = []
        for token in tokens:
            dictio = '{"'+token+'":"'
            posT = "Ukn"
            
            pos = getTermesR4(token)

            if pos is not None:
                posT=pos
            dictio += posT+'"}'
            obj = json.loads(dictio)
            arrayPos.append(obj)

        array.append(arrayPos)

    return array
nlp = stanza.Pipeline(lang="fr",verbose=False) 
Hotel = ["hotel","hôtel","établissement","auberge","motel","gite","palace"]
Personnel = ["personnel","accueil","réception","equipe","staff","emploté"]
Chambre = ["chambre","litterie","drap","couette","oreillers","rideau","meuble","lit","matelas","sommier","couchage","piéce","dortoir","salle","suite"]
Restauration=["restauration","déjeuner","restaurant","plat","repas","petit déjeuner","produit","petit dej","table","petit déjeuner","buffet"]
Menage = ["ménage","état","propreté","odeur","nettoyage","propre","sale","saleté","nets","poussière","balai","aspirateur"]
Equipement =["équipement","cuisine","salle de bain","évier","lavabo","douche","baignoire","bidet","miroir","décoration","wifi","climatisation","piscine","spa","connexion","parking","chauffage","garage","spa","tv","sport","WC","toilette","zapette","télé","rangement","commode","décorer","clim","climatiseur","terasse","balcon","jardin","espace vert","mer","plage","côte"]
Vue=["vue"]

Lexique = []
Lexique.append(Hotel)
Lexique.append(Personnel)
Lexique.append(Chambre)
Lexique.append(Restauration)
Lexique.append(Menage)
Lexique.append(Equipement)
Lexique.append(Vue)

def stanzaPosTagging(sentence,Catégorie):
    phrases = re.split("\.|,", sentence)  # re => Regular Expression
    # print(phrases)
    Dict = []
    inCat = False
    for phrase in phrases:
        Noms = getNom(phrase)
        Cat = getCategories(Noms)
        print("test on")
        print(phrase)
        print(Noms)
        print(Cat)
        print("-------------------------")
        for c in Catégorie:
            for ct in Cat:
                if c in ct: 
                    inCat = True
                    
            
        
    if inCat == False:
        return []

    for phrase in phrases:
       
        # print(phrase)
        # print(inCat)
        
        doc = nlp(phrase)
        for i, sent in enumerate(doc.sentences):
        #   print(*[f'word: {word.text+" "}\tpos: {word.pos}' for word in sent.words], sep='\n')
            Dictt = []
            for word in sent.words:
                if  "'" in word.text:
                    w = word.text
                    w=w[:-1]
                    word.text = w+"e"
                dict_ = json.loads('{"'+word.text+'":"'+word.pos+'"}')
                Dictt.append(dict_)
            Dict.append(Dictt)

    return Dict



def NomAdj(tokens):
    max_len = len(tokens)
    nomAdj = []
    pos = 0
    for token in tokens:
       
        if pos != max_len-1 and max_len >= 1:
            pos = pos+1
            # print(pos)
            

            if ("ADJ" in token.values() and "aucun" not in token.keys() and "NOUN" in tokens[pos].values() or "NOUN" in token.values() and "ADJ" in tokens[pos].values()):
                #print(pos)
                composition2mot = []
                if "ADJ" in token.values():
                    composition2mot.append(pos-1) #La position de l'adjectif 
                    composition2mot.append(token) #Adj
                    composition2mot.append(tokens[pos]) #Nom
                    
                elif "ADJ" in tokens[pos].values(): 
                    composition2mot.append(pos)
                    composition2mot.append(tokens[pos]) #Adj
                    composition2mot.append(token)   #Nom
                
                
                if "aucun" in token.keys():
                    composition2mot.append(json.loads('{"negation":"true"}'))
                else:
                    composition2mot.append(json.loads('{"negation":"false"}'))

                nomAdj.append(composition2mot)

    position = 0
    for token in tokens:
        
        if position != max_len-2 and max_len >= 2:
            position = position+1
            # print(pos)
            if ("NOUN" in token.values() and "VERB" in tokens[position].values() and "ADJ" in tokens[position+1].values()):
                composition2mot = []
                composition2mot.append(int(position+1))
                composition2mot.append(tokens[position+1]) #Adj
                composition2mot.append(token) #Nom
               
                composition2mot.append(json.loads('{"negation":"false"}'))
                nomAdj.append(composition2mot)

    position = 0
    for token in tokens:
        
        if position != max_len-3 and max_len >= 3:
            position = position+1
            # print(pos)
           
            if ("NOUN" in token.values()
                and "VERB" in tokens[position].values()
                and ("pas" in tokens[position+1].keys())
                    and "ADJ" in tokens[position+2].values()):
                composition2mot = []
                composition2mot.append(position+2)
                composition2mot.append(tokens[position+2]) #Adj
                composition2mot.append(token) #Nom
               
                composition2mot.append(json.loads('{"negation":"true"}'))

                nomAdj.append(composition2mot)
    position = 0
    for token in tokens:
        if position != max_len-4 and max_len >= 4:
            position = position+1
            # print(pos)

            if ("NOUN" in token.values()
                and ("n" in tokens[position].keys() or "ne" in tokens[position].keys())
                and "VERB" in tokens[position+1].values()
                and ("pas" in tokens[position+2].keys())
                    and "ADJ" in tokens[position+3].values()):
                # print(position)
                composition2mot = []
                composition2mot.append(position+3)
                composition2mot.append(tokens[position+3])
                composition2mot.append(token)
                
                composition2mot.append(json.loads('{"negation":"true"}'))

                nomAdj.append(composition2mot)
    return nomAdj


def matchNegationVerb(tokens):
    max_len = len(tokens)
    pos = 0
    neg = []
    for token in tokens:  # exemple : je n'est pas aimer
        if pos != max_len-3 and max_len >= 3:
            pos += 1
            if (("n" in token.keys() or "ne" in token.keys())
                and ("VERB" in tokens[pos].values() or "AUX" in tokens[pos].values())
                and "pas" in tokens[pos+1].keys()
                    and "VERB" in tokens[pos+2].values()):
                mot = []
                mot.append(pos+2)
                mot.append(tokens[pos+2])
                neg.append(mot)
    pos = 0
    for token in tokens:  # exemple j'ai jamais amier, rien aimer pas aimer
        if pos != max_len-1 and max_len >= 1:
            pos += 1
            if ((("pas" in token.keys() or "jamais" in token.keys() or "rien" in token.keys())
                     and "VERB" in tokens[pos].values())
                    ):
                if(len(neg) != 0):
                    for negation in neg:
                        if tokens[pos].keys() not in negation and pos != negation[0]:
                            mot = []
                            mot.append(pos)
                            mot.append(tokens[pos])
                            neg.append(mot)
                else :
                            mot = []
                            mot.append(pos)
                            mot.append(tokens[pos])
                            neg.append(mot)

    pos = 0
    for token in tokens:  # exemple j'ai aimer vraiment aucun service
        if pos != max_len-2 and max_len >= 2:
            pos += 1
            if ((("VERB" in token.values())
                     and "ADV" in tokens[pos].values() and ("aucun" in str(tokens[pos+1].keys()) ))
                    ):
                if(len(neg) != 0):
                    for negation in neg:
                        if (tokens[pos-1].keys() not in negation and pos-1 != negation[0]):
                            mot = []
                            mot.append(pos-1)
                            mot.append(tokens[pos-1])
                            neg.append(mot)
                else:
                    mot = []
                    mot.append(pos-1)
                    mot.append(tokens[pos-1])
                    neg.append(mot)
    pos = 0
    for token in tokens:  # exemple j'ai aimer aucun service
        if pos != max_len-1 and max_len >= 1:
            pos += 1
            if ((("VERB" in token.values())
                     and ("aucun" in str(tokens[pos].keys()) ))
                    ):
                if(len(neg) != 0):
                    for negation in neg:
                        if (tokens[pos-1].keys() not in negation and pos-1 != negation[0]):
                            mot = []
                            mot.append(pos-1)
                            mot.append(tokens[pos-1])
                            neg.append(mot)
                else:
                    mot = []
                    mot.append(pos-1)
                    mot.append(tokens[pos-1])
                    neg.append(mot)
    return neg

def getNom(sentence):
    Nom =[]
    posJDM = posTagging(sentence)
    for phrase in posJDM:
        for mot in phrase:
            if "Nom" in mot.values():
                for nom in mot.keys():
                    if nom not in Nom:
                        Nom.append(nom)
    return Nom          


def getVerb(tokens):
    pos = 0
    verbs = []
    for token in tokens:
        if "VERB" in token.values():
            indexV = []
            index = pos
            verb = token
            indexV.append(index)
            indexV.append(verb)
            verbs.append(indexV)
        pos += 1

    return verbs


def getAdvConnu():
    AdverbConnu =[]
    dataAdv = pd.read_csv("./src/lexique_intensifieurs",
                          encoding="utf-8", header=None)
    Adverbs = dataAdv[0]
    for ad in Adverbs:
                adv = ad.split(":")[0]
                AdverbConnu.append(adv)
    return AdverbConnu


def getAdverb(tokens):
    AdvConnu = getAdvConnu()
    pos=0
    adv=[]
    for token in tokens:

        if token.keys() in AdvConnu or "ADV" in token.values():
            compo=[]
            compo.append(pos)
            compo.append(token)
            adv.append(compo)
        pos+=1
    return adv


def isNegated(verb, ListTermsNegatif):
    # print(verb)
    posVerb = verb[0]
    ver = ""
    for term in verb[1]:
        ver = term
    for verbe in ListTermsNegatif:
        VerNegated = ""
        for term in verbe[1]:
            VerNegated = term

        posVerNegated = verbe[0]
        if VerNegated in ver and posVerb == posVerNegated:
            return "true"

    return "false"

def isPP(word):
    words_dict = reseauxDumpByRelation4(word)
    for word_dict in words_dict:
        word=word_dict["t"]
        if "Ver:PPas" in word:
            return True

    return False    
def getMotRel(token, pos):

    mot1 = ""
    mot2 = ""
    posi = pos
    while(posi != len(token)):  # Parcours a droite de la phrase chercher le mot le plus proche
        if "NOUN" in token[posi].values():
            for term in token[posi].keys():
                mot1 = term
            break
        posi += 1

    position = 0
    for term in token:  # Parcours dés le début de la phrase
        if "NOUN" in term.values():
            for t in term.keys():
                mot2 = t

            break
        position += 1
    # print(posi)
    # print(posi-pos+1)
    # print(Ver)
    # print(position)
    # print(position+pos)
    # pour le moment je cherche le nom le plus loin du mot
    if(posi-pos+1 > position+pos and mot1 != ""):
        return mot1
    elif mot2 != "":
        return mot2

    return "null"



def AdvAdj(tokens):
    max_len = len(tokens)
    advAdj = []
    pos = 0
    for token in tokens:
        composition2mot = []
        if pos != max_len-1 and max_len >= 1:
            pos = pos+1
            # print(pos)
            composition2mot = []

            if ("ADV" in token.values() and "ADJ" in tokens[pos].values()):

                composition2mot.append(pos)
                composition2mot.append(token)
                composition2mot.append(tokens[pos])

                advAdj.append(composition2mot)

    return advAdj


def polarisation(sentence,Catégorie):
    dataAdv = pd.read_csv("./src/lexique_intensifieurs",
                          encoding="utf-8", header=None)
    Adverbs = dataAdv[0]
    positif = "_POL-POS"
    neutre = "_POL-NEUTRE"
    negatif = "_POL-NEG"
    score = 0
    denominator = 0
    # je retourne les phrases tokenizer par les mots + valeur de leurs pos
    Tokens = ambiguiter(sentence,Catégorie)
    print("coms")
    print(Tokens)
    # print(Tokens)
    for token in Tokens:

        # je retourne une liste des mots Adj Nom ou Nom Adj
        nomAdj = NomAdj(token)
        # traiter les nomAdj
        for term in nomAdj:
            # print(term)
            adj = ""
            mot = ""
            neg = ""
            pos= term[0]

            for Adj in term[1]:
                    adj = Adj

            for Nom in term[2] :
                    mot = Nom   

            for Neg in term[3].values() :
                    neg = Neg
            pol = getTermesR36(adj)
            if pol in positif and neg in "true":
                pol = negatif
            mot2 = getMotRel(token,pos)
            print(adj + " Negation ? "+neg + " => " + pol + ", Qui ?? : "+mot2 if mot2 == mot 
                else adj + " Negation ? "+neg + " => " + pol + ", Qui ?? : "+mot2 +" <- "+mot)
            if pol == positif:
                score += 1
            elif pol == negatif:
                score -= 1

        # traiter les verbes
        negation = matchNegationVerb(token)
        verbes = getVerb(token)
        for verb in verbes:
            # print(verb)
            pos = verb[0]
            Ver = ""
            for term in verb[1]:
                Ver = term

            lemma = getTermesR19(Ver)
         
            pol = getTermesR36(lemma)
            if isNegated(verb, negation) in "true" and pol in positif:
                
                pol = negatif

            if(pol in negatif or pol in positif):
                
                if pol == negatif:
                    score -= 1
                else:
                    score += 1

                mot = getMotRel(token, pos)
                print(Ver + " Negation ? "+"true => " + pol + " Qui?? : " + mot if(verb in negation)
                      else Ver + " Negation ? "+"false => " + pol + " Qui?? : " + mot)

        # traiter les Adverbe
            # Adverb suivie par Adjectif
            AdverbConnu = getAdvConnu()  # adverb lexique_intensifieurs

            AdverbTraiter=[]
            AdvAdjectif = AdvAdj(token)
            for array in AdvAdjectif:
                print(array)
                pos = array[0]
                adv = ""
                adj = ""
                for term in array[1]:
                    adv = term
                for term in array[2]:
                    adj = term
                aTraiter =[]
                aTraiter.append(pos-1) #position de l'adverbe
                aTraiter.append(adv)
                AdverbTraiter.append(aTraiter)
                pol = ""
                advScore = 0

                if(adv not in AdverbConnu):
                    
                    pol = getTermesR36(adv)
                    if pol == positif:

                        advScore += 1
                    elif pol == negatif:

                        advScore -= 1
                else:

                    for ad in Adverbs:
                        if ad.split(":")[0] == adv:
                            advScore = ad.split(":")[1]

                adjPol = getTermesR36(adj)
                if adjPol == positif:
                    score += int(advScore)+1
                elif adjPol == negatif:
                    if advScore > 0:
                        score -= -advScore - 1
                    else:
                        score -= advScore-1
                else:
                    score += int(advScore)
                mot = getMotRel(token, int(pos))
                print(adv+" "+adj+" Negation ? "+"true =>  Qui?? : " + mot if(pol in negatif or adjPol in negatif)
                      else adv+" "+adj + " Negation ? "+"false => Qui?? : " + mot)

            # Adverb
            Advs = getAdverb(token)
           
            for array in Advs:
                # print(array)
                pos = int(array[0])
                adv = ""
                for term in array[1]:
                        adv = term
                skip =0 #je met un flag comme quoi l adverbe n'a été jamais traiter
                for dejaTraiter in AdverbTraiter:
                    if dejaTraiter[0] == pos and dejaTraiter[1] == adv:
                        skip=1 #je met le flag a 1 si l'adverbe a été déja traiter
                if(skip == 1):
                    #print("Deja traiter")
                    break
                pol = ""
                if adv in AdverbConnu:
                    for ad in Adverbs:
                        if ad.split(":")[0] == adv:
                            score=score*int(ad.split(":")[1])

                else :
                    pol = getTermesR36(adv)
                    if(pol == positif):
                        score+=1
                    elif pol == negatif:
                        score-=1
                    
    return score



def ambiguiter(sentence,Catégorie):
    stanzaPos = stanzaPosTagging(sentence,Catégorie)
    
    # print(stanzaPos)
    AuxDetected = -1
    maxLen = len(stanzaPos)
    if maxLen == 0:
        return []
    pos =0
    for phrase in stanzaPos:
        for mot in phrase:
            if pos != maxLen-1 :
                pos+=1
            for Def in mot.values():
                if Def == "AUX" :
                  AuxDetected=1
                  targeted = phrase[pos]
                  for target in targeted.keys():
                    if(isPP(target)):
                        AuxDetected=0
            for Def in mot.values():
                if Def == "VERB":
                    for target in mot.keys():
                        if((isPP(target) and AuxDetected>0)
                        or (isPP(target) and AuxDetected==-1)
                        ):
                            Dict = '{"'+target+'":"ADJ"}'
                            phrase[pos-1]=json.loads(Dict)
                       
                       
    return stanzaPos                    

def getCommentsbyHotels(Id,Coms):
    Commentaires = []
    for comment in Coms:
        # print(comment)
        HotelId = comment.split(";")[2]
        if str(HotelId) in Id :
            Commentaires.append(comment.split(";")[1])

    return Commentaires

def getHotelName(Id):
    hotels = getHotels()
    for hotel in hotels:
        hotelId = hotel.split(";")[0]
        if str(hotelId)==str(Id):
            return hotel.split(";")[1]

def Val(Dict):
    # print(Dict)
    for v in Dict.values():
        return v

def sortHotels(L):
    N = len(L)
    for n in range(1,N):
        cle = L[n]
        j = n-1
        while j>=0 and int(Val(L[j])) < int(Val(cle)):
            L[j+1] = L[j] # decalage
            j = j-1
        L[j+1] = cle
    
    return L

def getCategories(Nom):
    Categories = []
    lemmatizedWords = []
    for word in Nom :
        lemma =  getTermesR19(word)
        lemmatizedWords.append(lemma)
    for categorie in Lexique:
        for mot in lemmatizedWords:
            if mot in categorie:
                Categories.append(categorie[0])
    return Categories
                

def CommentsPolarisation(Comments,Nom): #comments is a dict 
    Hotels = []
    Coms = []
    Catégories=getCategories(Nom)
    print("La catégorie du souhait de l'utilisateur est : ")
    print(Catégories)
    for Dictcomment in Comments:
        comD = Dictcomment['comment']
        # print(comD)
        comment = comD.split(";")
        textComment = comment[1]
        # print(textComment)
        Coms.append(str(comD))
        idHotel = comment[2]
        if str(idHotel) not in Hotels :
            Hotels.append(str(idHotel))
    HotelComment = []
    HotelDict = []
    for Id in Hotels:
        score = 0
        # print(str(Id))
        # hotelComments = getCommentsbyHotels(Id,Coms)
        for comment in Coms:
            com =comment.split(";")[1]
            hId = comment.split(";")[2]
            if(str(hId) == str(Id)):
                score += int(polarisation(com,Catégories))   
                # print(com)
        hotelName = getHotelName(Id)
        Dict ='{"'+str(hotelName)+'":"'+str(score)+'"}'
        HotelDict.append(json.loads(Dict))
    sortHotels(HotelDict)
    return HotelDict
    
def formatJson(Hotels):
    Format = []
    for Hotel in Hotels:
        Nom = ""
        Score = ""
        for nom in Hotel.keys():
            Nom =nom
        for score in Hotel.values():
            Score = score
        Dict ='{"nom":"'+str(Nom)+'" , "score":"'+str(Score)+'"}'
        Format.append(json.loads(Dict))    
    # print(Format)
    return Format
# print(polarisation("La piscine c'était super agréable et a bonne température. Le personnel était vraiment à l'écoute surtout au bar et a la piscine. La salle de sport dispose de machine très sympa. Le confort de la literie. L accessibilité du parking"))
def json_extract(obj, key):
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

# print(polarisation("Dommage pas de parking"))

print(composed_words_cleaner_version("une très belle vue sur la mer"))

# Comments = getCommentes()
# CommentsVector = createVectors(Comments)
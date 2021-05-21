import urllib.request
import pandas as pd
from operator import itemgetter
from jdmLink import *
import re
import json
import time
import stanza
import deplacy
import math


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
    comments_file = pd.read_csv('./src/comments', encoding="utf-8", header=None,delimiter = "\n")
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
    hotels_file = pd.read_csv('./src/hotels', encoding="utf-8", header=None)
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
def cleanComments():
    tokenized_commentes = []
    comments_list = getCommentes()
 
    for comment in comments_list : 
        comment_tokens = []
        comment = comment.lower()
        # récupération de lid du commentaitere
        c_id = comment.split(";")[0]
        # print(c_id)
        # tokenisation
        comment_tokens=clean_expr_from_additionals(comment)
        # suppression des nombrs ainsi que des chaines de longeurs <= a 2
        comment_tokens = [ elem for elem in comment_tokens if not elem.isdigit() and len(elem)>2]
        # déduction des mots composées 
        com_words =composed_words_cleaner_version(comment)
        # suppression des nombrs ainsi que des chaines de longeurs <= a 2
        com_words = [ elem for elem in com_words if not elem.isdigit() and len(elem)>2]
        # fusion sans duplication des deux listes 
        comment_tokens = comment_tokens + list(set(com_words) - set(comment_tokens))
        comment_dict = {"comment":comment ,"comment_tokens":comment_tokens,"score":0}
       
        tokenized_commentes.append(comment_dict)

    # print(tokenized_commentes[3])
    # retourne une liste de dictionnaire de commentaitre prétraités
    return tokenized_commentes
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



def posTagging(sentence,status):
    if sentence =="":
        return []
    phrases = re.split("\.|,", sentence)  # re => Regular Expression
    # print(phrases)
    array = []
    for phrase in phrases:
        if status:
            tokens = composed_words_cleaner_version(phrase)
        else :
            tokens = phrase.split(" ")
        arrayPos = []
        for token in tokens:
            dictio = '{"'+token+'":"'
            pos = getTermesR4(token)
            dictio += pos+'"}'
            obj = json.loads(dictio)
            arrayPos.append(obj)

        array.append(arrayPos)

    return array
nlp = stanza.Pipeline(lang="fr",verbose=False) 



def stanzaPosTagging(sentence):
    phrases = re.split("\.|,", sentence)  # re => Regular Expression
    # print(phrases)
    Dict = []
    for phrase in phrases:
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
            if ("NOUN" in token.values() and ("VERB" in tokens[position].values() or "AUX" in tokens[position].values()) and "ADJ" in tokens[position+1].values()):
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
                and "AUX" in tokens[position].values()
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
                and "AUX" in tokens[position+1].values()
                and ("pas" in tokens[position+2].keys())
                    and "ADJ" in tokens[position+3].values()):
                print(position)
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
                     and ("aucun" in str(tokens[pos].keys()) or "pas" in str(tokens[pos].keys()) ))
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
    for token in tokens:  # exemple j'ai pas vraiment aimer le service
        if pos != max_len-3 and max_len >= 3:
            pos += 1
            if ((("pas" in token.keys())
                     and ("ADV" in str(tokens[pos].values()) )
                     and ("VERB" in str(tokens[pos+1].values()))
                     
                     )
                    ):
                if(len(neg) != 0):
                    for negation in neg:
                        if (tokens[pos-1].keys() not in negation and pos-1 != negation[0]):
                            mot = []
                            mot.append(pos+1)
                            mot.append(tokens[pos+1])
                            neg.append(mot)
                else:
                    mot = []
                    mot.append(pos+1)
                    mot.append(tokens[pos+1])
                    neg.append(mot)
    return neg

def getNom(sentence):
    if sentence == "":
        return []
    Nom =[]
    posJDM = posTagging(sentence,True)
    # print(posJDM)
    for phrase in posJDM:
        for mot in phrase:
            if "Nom" in mot.values():
                for nom in mot.keys():
                    if nom not in Nom:
                        Nom.append(nom)
    stanzaNom = []
    pos = posTagging(sentence,False)
    for phrase in pos:
        for mot in phrase:
            if "Nom" in mot.values():
                nom = ""
                # print(mot)
                for n in mot.keys():
                  nom = n
                  if nom not in stanzaNom:
                     stanzaNom.append(nom)
    Nom = list(set(stanzaNom) | set(Nom))
    Nom.sort(key=lambda x: x.count(' '), reverse=True)
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

        if (token.keys() in AdvConnu or ("ADV" in token.values() and "pas" not in token.keys())) and "ne" not in token.keys():

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
        # print(token)
        composition2mot = []
        if pos != max_len-1 and max_len >= 1:
            pos = pos+1
            # print(pos)
            composition2mot = []

            if ("ADV" in token.values() and "ADJ" in tokens[pos].values() and "pas" not in token.keys()):

                composition2mot.append(pos)
                composition2mot.append(token)
                composition2mot.append(tokens[pos])

                advAdj.append(composition2mot)

    return advAdj





def inUserCategories(Categorie):

    for categorie in userSearch:
        if str(categorie) == str(Categorie):
            return True
    
    return False

def polarisation(sentence):
    dataAdv = pd.read_csv("./src/lexique_intensifieurs",
                          encoding="utf-8", header=None)
    Adverbs = dataAdv[0]
    positif = "_POL-POS"
    neutre = "_POL-NEUTRE"
    negatif = "_POL-NEG"
    score = 0
    # je retourne les phrases tokenizer par les mots + valeur de leurs pos
    Tokens = ambiguiter(sentence)
    # print(Tokens)
    for token in Tokens:
        
        # je retourne une liste des mots Adj Nom ou Nom Adj
        nomAdj = NomAdj(token)
        # traiter les nomAdj
        for term in nomAdj:
            # print(term)
            scoreAdj =0
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
            # print(adj + " Negation ? "+neg + " => " + pol + ", Qui ?? : "+mot2 if mot2 == mot 
            #     else adj + " Negation ? "+neg + " => " + pol + ", Qui ?? : "+mot2 +" <- "+mot)
            if pol == negatif and mot != "null" and mot != "" and inUserCategories(mot):
                score -= int(math.exp(scoreAdj+1))
            elif pol == positif :
                score+=1
            elif pol == negatif :
                score-=1

        # traiter les verbes
        negation = matchNegationVerb(token)
        verbes = getVerb(token)
        for verb in verbes:
            # print(verb)
            pos = verb[0]
            Ver = ""
            mot =""
            scoreVerb=0
            for term in verb[1]:
                Ver = term

            lemma = getTermesR19(Ver)
         
            pol = getTermesR36(lemma)
            if isNegated(verb, negation) in "true" and pol in positif:
                pol = negatif
            elif isNegated(verb, negation) in "true" and pol in neutre:
                score-=1
            mot = getMotRel(token, pos)
            # print(Ver + " Negation ? "+"true => " + pol + " Qui?? : " + mot if(verb in negation)
            #       else Ver + " Negation ? "+"false => " + pol + " Qui?? : " + mot)

            if pol == negatif and mot != "null" and mot != "" and inUserCategories(mot):
                score -= int(math.exp(1))
            elif pol == positif :
                score+=1
            elif pol == negatif :
                score-=1

        # traiter les Adverbe
            # Adverb suivie par Adjectif
        AdverbConnu = getAdvConnu()  # adverb lexique_intensifieurs
        AdverbTraiter=[]
        AdvAdjectif = AdvAdj(token)
        for array in AdvAdjectif:
            pos = array[0]
            adv = ""
            mot = ""
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
            mot = getMotRel(token, int(pos))
            # mot = getNom(token)
            adjPol = getTermesR36(adj)
            scoreAdj =0
            # print(adjPol)
            # print(mot)
            if int(advScore)>0 and adjPol == positif :
                # print(" mot != "null" and mot != "" and inUserCategories(mot)")
                score += int(advScore)*1
            elif ( 
                (int(advScore)<0  and mot != "null" and mot != "" and inUserCategories(mot))
                or
                (adjPol == negatif and mot != "null" and mot != "" and inUserCategories(mot))
                ):
                score -= abs(int(advScore)*int(math.exp(1)))
                # print("b "+str(scoreAdj))
                
            elif adjPol == positif :
                score+=int(advScore)*1
            elif adjPol == negatif :
                score-=int(advScore)*(1)


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
                
    return int(score)



def ambiguiter(sentence):
    stanzaPos = stanzaPosTagging(sentence)
    AuxDetected = -1
    pos =0
    for phrase in stanzaPos:
        pos=0
        AuxDetected = -1
        for mot in phrase:
            pos+=1
            for adv in mot.keys():
                 if str(adv).lower() == "aucun" or str(adv).lower() == "aucune":
                    Dict = '{"'+adv+'":"ADV"}'
                    phrase[pos-1]=json.loads(Dict)
            
            for Def in mot.values():
               
                if Def == "AUX":
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
            for adj in mot.keys():
                 if str(adj).lower() == "eu":
                  
                    Dict = '{"'+adj+'":"VERB"}'
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
    return int(Dict["score"])
   

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

def Pol(Dict):
    return int(Dict["polarisation"])
def sortComments(L):
    N = len(L)
    for n in range(1,N):
        cle = L[n]
        j = n-1
        while j>=0 and int(Pol(L[j])) < int(Pol(cle)):
            L[j+1] = L[j] # decalage
            j = j-1
        L[j+1] = cle
    
    return L                
userSearch=[]
def CommentsPolarisation(Comments,Nom): #comments is a dict 
    print("polarisation ...")
    Hotels = []
    Coms = []
    userSearch=Nom
    print("Le souhait de l'utilisateur est : ")
    print(userSearch)
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
    
    HotelDict = agregation(Hotels,Coms)
    return HotelDict

def getNombreCommentaireHotel(id):
    comments = getCommentes()
    size = 0
    for comment in comments:
        if str(comment.split(";")[2]) == str(id):
            size+=1
    
    return size

def agregation(Hotels,Coms):
    HotelDict = []
    for Id in Hotels:
        HotelComment = []
        score = 0
        scoreRatio = 0
        for comment in Coms:
            cId =comment.split(";")[0]
            com =comment.split(";")[1]
            hId = comment.split(";")[2]
            if(str(hId) == str(Id)):
                
                pol = int(polarisation(com))
                if(pol > 0):
                    scoreRatio+=1
                score += pol
                D = {"id":cId,"comment":com,"polarisation":pol}
                
                HotelComment.append(D)               
        hotelName = getHotelName(Id)
        sortComments(HotelComment)
        Dict2 = {"id":Id,"nom":hotelName,"score":score,"comments":HotelComment,"status":False}
        HotelDict.append(Dict2)
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

def RegexCreator(terms):
    return ''.join([r'(?=.*?\b%s\b)' % (term) for term in terms])

def getRelatedComments(user_words_list,selectors):

    print(user_words_list)
    print("Matching regEx")
    CommentsRelated = []
    words_from_JDM = getAllTermesR5Sortant(user_words_list)
    
    filtred_word = []
    words_from_JDM.extend(user_words_list)
    for word in words_from_JDM:
        if find(word) == True:
            filtred_word.append(word)
        # else:
            # print("No")

    filtred_word.extend(selectors)
    # print(filtred_word)
    regex1 = re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(filtred_word)))
    print(regex1)

    for Comment in Comments :
        comment = Comment.split(";")[1]
        Id = Comment.split(";")[0]
        score =0
        if regex1.search(comment.lower()) :
            matched=regex1.search(comment).group()
            timesMatched=len(re.findall(regex1, comment.lower()))
            if comment not in CommentsRelated :
                if matched in user_words_list:
                    # print(matched)
                    score+=int(2*timesMatched)         #si le mot retrouver est dans la liste du souhait de l'utilisateur
                    if len(matched.split(" ")) > 1:
                        # print(matched)
                        score+=int(10*score) #si c un mot composer
                else :
                    score+=int(timesMatched) #si c un mot relationnel
                comment_dict = {"comment": Comment, "score": score}
                CommentsRelated.append(comment_dict)
    CommentsRelated = sorted(CommentsRelated, key=itemgetter('score'), reverse=True)
    return CommentsRelated
        

def getOntologieWordsFromJson():
    with open('src/ontologie_words.json') as json_file:
        data = json.load(json_file)
        #print(data)
        return data
def getOntologieWordsFromJson5():
    with open('src/ontologie_words5.json') as json_file:
        data = json.load(json_file)
        return data

def getCommentaire():
    com = []
    for comment in Comments:
        com.append(comment.split(";")[1])
    return com

def find(target):
    start = 0
    end = LongueurOntologie - 1
    while start <= end:
        middle = (start + end)// 2
        midpoint = Ontologie[middle]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return True

    return False
    

def creatOntologieFile() :
    ontologie = getMyOntologie()
    words_list=[]
    for ontologie_word in ontologie:
        words_list.append(getTermesR5Sortants(ontologie_word))
    words = []
    for l in words_list : 
        for w in l :
            words.append(w.lower())
    words_cleaed = list(set(words))
    words_cleaed =sorted(words_cleaed)
    try:
        filename = "./src/ontologie_words5.json"
        # print(words_list)
        with open(filename, mode='w', encoding="utf-8") as my_file:

            json.dump(words_cleaed, my_file, indent=4)
            return my_file
    except FileNotFoundError as err:
        raise err
        return False


def formatUserReqByR0(user_sentence,selectors): 
    nouns= getNom(user_sentence)
    user_tokens = clean_expr_from_additionals(user_sentence)
    user_req=[]
    
    # tous les nom ont un score de 2
    for n in nouns :
        word_dict = {"t":n , "score":2}
        user_req.append(word_dict)
    # on ajoute les mot composé avec un score de 3 
    composed_words_list = composed_words_cleaner_version(user_sentence)
    # suppression des nombrs ainsi que des chaines de longeurs <= a 2
    composed_words_list = [ elem for elem in composed_words_list if not elem.isdigit() and len(elem)>2]
    # on filtre les termes en doubles 
    for word in user_tokens : 
        for com_word in composed_words_list :
            if word == com_word : 
                composed_words_list.remove(com_word)
    # ajouts des mots composé dans la requete avec un score de 3 
    for com_word in composed_words_list : 
        word_dict = {"t":com_word , "score":3}
        user_req.append(word_dict)
    
    # ajouts des mots issu de JDM avec un score de 1 
    to_filter_words= getAllTermesR0(nouns)
    filtered_list= filterVocabularyByFile(to_filter_words)
    for filterd_word in filtered_list:
        word_dict = {"t":filterd_word , "score":1}
        user_req.append(word_dict)
    
    for selector in selectors:
        word_dict = {"t":selector , "score":2}
        user_req.append(word_dict)

    return user_req


def formatUserReqByR5(user_sentence,selectors): 
    nouns= getNom(user_sentence)
    print(nouns)
    user_tokens = clean_expr_from_additionals(user_sentence)
    user_req=[]
    # tous les nom ont un score de 2
    for n in nouns :
        word_dict = {"t":n , "score":2}
        user_req.append(word_dict)
    # on ajoute les mot composé avec un score de 3 
    composed_words_list = composed_words_cleaner_version(user_sentence)
    # print(composed_words_list)
    # suppression des nombrs ainsi que des chaines de longeurs <= a 2
    composed_words_list = [ elem for elem in composed_words_list if not elem.isdigit() and len(elem)>2]
    # on filtre les termes en doubles 
    for word in user_tokens : 
        for com_word in composed_words_list :
            if word == com_word : 
                composed_words_list.remove(com_word)

    # ajouts des mots composé dans la requete avec un score de 3 
    # print(composed_words_list)
    for com_word in composed_words_list : 
        word_dict = {"t":com_word , "score":3}
        user_req.append(word_dict)

    # ajouts des mots issu de JDM avec un score de 1 
    synonymes_liste= getAllTermesR5(nouns)

    for syno in synonymes_liste:
        word_dict = {"t":syno , "score":1}
        user_req.append(word_dict)

    for selector in selectors:
        word_dict = {"t":selector , "score":2}
        user_req.append(word_dict)

    return user_req


def BinarySearch(lys, val):
    first = 0
    last = len(lys)-1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first+last)//2
        if lys[mid] == val:
            index = mid
        else:
            if val<lys[mid]:
                last = mid -1
            else:
                first = mid +1
    return index

def isWordRelatedToOntologie(word):
    return find(word)
    

def filterVocabularyByFile(words_list):
    filtered_words = []
    for w in words_list : 
        if isWordRelatedToOntologie(w) :
            filtered_words.append(w)
            
    return filtered_words

    

def getCommentsScoreByVect(user_req):
    concerned_commentes = []
    
    for comment_dict in cleaned_comments_list :
        for w_dict in user_req:
            if w_dict["t"] in comment_dict["comment_tokens"] : 
                comment_dict["score"]+=w_dict["score"]
        
        if comment_dict["score"] > 0 : 
            concerned_commentes.append(comment_dict)
    
    # trier la liste
    concerned_commentes = sorted(concerned_commentes, key=lambda k: k['score'],reverse=True) 
    return concerned_commentes



cleaned_comments_list = cleanComments()
Ontologie=getOntologieWordsFromJson()
LongueurOntologie= len(Ontologie)


# # test Data
# souhait = ""
# # userSearch=["piscine"]
# selectors=["wifi"]
# Nom = []
# user_req = formatUserReqByR5(souhait,selectors)
# comments = getCommentsScoreByVect(user_req)
# Hotels = CommentsPolarisation(comments,Nom)
# # print(polarisation("belle piscine chauffée qui fonctionne même en hiver.".lower())) 
# print(Hotels)
# # print(Val({"nom":"Zénia Hôtel & Spa","score":"10"}))

# print(polarisation("Je n'ai pas aimer la wifi. La connexion ne marchait pas"))
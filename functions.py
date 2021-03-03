import urllib.request
import re
import sys

# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et une relation


def reseauxDump_norelin(terme, numRel):

    idDuTerme = -1
    termeURL = terme.replace("é", "%E9").replace("è", "%E8").replace("ê", "%EA").replace(
        "à", "%E0").replace("ç", "%E7").replace("û", "%FB").replace(" ", "+")

    with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}&relin=norelin".format(termeURL, numRel)) as url:
        s = url.read().decode('ISO-8859-1')
        line = s.split("\n")

        # words = filterTermesAndRelations(line)

        return formatResault(filterTermesAndRelations(line))

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
    words_dict = reseauxDump(word,0)
    for word in words_dict:
        words_list.append(word.get("t"))
    
    return words_list


#----------------------------------my part
import pandas as pd
import nltk
from nltk.corpus import stopwords
import spacy
#import pprint # for proper print of sequences
#import treetaggerwrapper as ttpw

stopwords_list = stopwords.words('french')
#nlp = spacy.load('fr_core_news_md')
#tagger = ttpw.TreeTagger(TAGLANG='fr', TAGOPT="-prob -threshold 0.7 -token -lemma -sgml -quiet")
#tags = tagger.tag_text('Voici un petit test de TreeTagger pour voir.')

# uncomment the line below to see all the stop words 
# print(stopwords_list)
#pprint.pprint(tags)

# retrieving comments from thhe text file
com = pd.read_csv('commentaires.txt', header = None)
comments = com[0]


# in case a typed research ends with multipule spaces this function gets
# rid of them

def gets_rid_of_empty_quotes(lst):
    while lst[-1] == '':
        lst = lst[:-1]
    while lst[0] == '' :
        lst = lst[1:]
    browser = 1
    while '' in lst and browser < len(lst):
        while lst[browser]=='' :
            if browser-1==0: 
                c = [lst[0]]
            else : 
                c = lst[:browser]
            lst =  c + lst[browser+1:]
        browser+=1
    return lst


# lst contains words
def clean_expr_from_additionals(expression) :
    strings = re.split('[\\\\\n\t\b\"`\a\f\r²~\"#\'"{"" ""("")""}"@!§"|"_"+""*""/""=";,?.:µ\[\]]{1}',expression)
    strings = gets_rid_of_empty_quotes(strings)

    return strings
#
def gets_rid_of_dashes(lst):
    browser = 0;
    l = []
    for word in lst :
        if re.search('^-+[a-z]*-*$|^-*[a-z]*-+$',word):
            word = re.split('-',word)
            l = l + word
        else : 
            l = l + [word]
        browser+=1
    l = gets_rid_of_empty_quotes(l)
    return l


def cleanSpecialChar(str) :
    regex = r"([^\wÀ-úÀ-ÿ][^\wÀ-úÀ-ÿ]+)|[\/:-@\[-\`{-~$]"
    res= re.sub(regex, " ", str, 0, re.MULTILINE)
    return res

def list_to_string(lst):
    return " ".join(lst)

def composed_words_detecting(lst):
    resulting_list = []
    browser = 0
    len_longest_composed_word = -1
    index_of_latest_cw = -1
    last_added_is_a_cw = False
    i_min = len(lst) + 1
    i_max = 0
    passage = False
    side = {}
    remove_from_side = {}
    never_in_inter = True
    while browser < len(lst):
        related_composed_words = reseauxDump(lst[browser],11)
        rcw_browser = 1
        rcw_len = len(related_composed_words)
        len_rl_before = len(resulting_list)
        while rcw_browser < rcw_len :
            composed_word = related_composed_words[rcw_browser]['t']
            cleaned_composed_word = clean_expr_from_additionals(composed_word)
            cw_len = len(cleaned_composed_word)
            if ((lst[browser:cw_len+browser]) == cleaned_composed_word and 
                (len(resulting_list) == 0 or composed_word != resulting_list[len(resulting_list)-1]) and composed_word not in resulting_list):
                index_of_latest_cw = len(resulting_list)
                resulting_list+=[composed_word]
                last_added_is_a_cw = True
                len_longest_composed_word = max(len_longest_composed_word,browser+len(cleaned_composed_word))
                if browser <= i_max:
                    i_min = min(i_min,browser)
                else : 
                    i_min = browser
                i_max = max(i_max,browser+cw_len-1)
            else : 
                if ((lst[browser:cw_len+browser]) == cleaned_composed_word and 
                (len(resulting_list) == 0 or composed_word != resulting_list[len(resulting_list)-1]) and composed_word in resulting_list):
                    if browser <= i_max:
                        i_min = min(i_min,browser)
                    else : 
                        i_min = browser
                    i_max = max(i_max,browser+cw_len-1)
            if browser != 0 :
                p_browser = 0
                while p_browser < browser :
                    if (lst[p_browser:p_browser+cw_len]== cleaned_composed_word and 
                        composed_word not in resulting_list):
                        resulting_list+=[composed_word]
                        while len(resulting_list[len(resulting_list)-2].split(" "))==1 and resulting_list[len(resulting_list)-2].split(" ")[0] in resulting_list[len(resulting_list)-1].split(" "):
                            resulting_list = resulting_list[:len(resulting_list)-2]+resulting_list[len(resulting_list)-1:]
                        index_of_latest_cw = len(resulting_list)-1
                        last_added_is_a_cw = True
                        len_longest_composed_word = max(len_longest_composed_word,p_browser+len(cleaned_composed_word))
                        passage = True
                        if browser <= i_max:
                                i_min = min(i_min,p_browser)
                        else : 
                            i_min = p_browser
                        i_max = max(i_max,p_browser+cw_len-1)
                    else : 
                        if (lst[p_browser:p_browser+cw_len]== cleaned_composed_word and composed_word in resulting_list):
                            if browser <= i_max:
                                i_min = min(i_min,p_browser)
                            else : 
                                i_min = p_browser
                            i_max = max(i_max,p_browser+cw_len-1)
                    p_browser+=1
            rcw_browser+=1            
        if (len_rl_before == len(resulting_list) and browser >= len_longest_composed_word and lst[browser] not in resulting_list and 
            (browser < i_min or browser > i_max)):
            if not passage:
                resulting_list+=[lst[browser]]
                passage = False
            else : 
                side[browser] = lst[browser]
            remove_from_side = [k for k in side if (k >= i_min and k <= i_max)]
            for key in remove_from_side:
                del side[key]
            last_added_is_a_cw = False
        browser+=1
    for key,value in side.items() :
        if value not in resulting_list:
            resulting_list += [value]
    return resulting_list

def only_compsoed_words(lst):
    resulting_list = []
    browser = 0
    len_longest_composed_word = -1
    index_of_latest_cw = -1
    last_added_is_a_cw = False
    while browser < len(lst):
        related_composed_words = reseauxDump(lst[browser],11)
        rcw_browser = 1
        rcw_len = len(related_composed_words)
        len_rl_before = len(resulting_list)
        while rcw_browser < rcw_len :
            composed_word = related_composed_words[rcw_browser]['t']
            cleaned_composed_word = clean_expr_from_additionals(composed_word)
            cw_len = len(cleaned_composed_word)
            if ((lst[browser:cw_len+browser]) == cleaned_composed_word and 
                (len(resulting_list) == 0 or composed_word != resulting_list[len(resulting_list)-1])):
                index_of_latest_cw = len(resulting_list)
                resulting_list+=[composed_word]
                last_added_is_a_cw = True
                len_longest_composed_word = max(len_longest_composed_word,browser+len(cleaned_composed_word))
            if browser != 0 :
                p_browser = 0
                while p_browser < browser :
                    if (lst[p_browser:p_browser+cw_len]== cleaned_composed_word and 
                        composed_word not in resulting_list):
                        resulting_list+=[composed_word]
                        while len(resulting_list[len(resulting_list)-2].split(" "))==1 and resulting_list[len(resulting_list)-2].split(" ")[0] in resulting_list[len(resulting_list)-1].split(" "):
                            resulting_list = resulting_list[:len(resulting_list)-2]+resulting_list[len(resulting_list)-1:]
                        index_of_latest_cw = len(resulting_list)-1
                        last_added_is_a_cw = True
                        len_longest_composed_word = max(len_longest_composed_word,p_browser+len(cleaned_composed_word))
                    p_browser+=1
            rcw_browser+=1            
        if len_rl_before == len(resulting_list) and browser >= len_longest_composed_word:
            #resulting_list+=[lst[browser]]
            last_added_is_a_cw = False
        browser+=1
    return resulting_list

def cleanes_list_that_has_composes_words(lst):
    new_lst = []
    for word in lst :
        new_lst+=[word.split(" ")]
    #print(new_lst)
    for b_lst in new_lst :
        #print(b_lst)
        if len(b_lst) == 1:
            #print(b_lst)
            for e_lst in new_lst :
                if b_lst[0] in e_lst and len(e_lst) != 1: 
                    '''print("//////////////////////////hey")
                    print(b_lst[0])
                    print(e_lst)'''
                    lst.remove(b_lst[0])
                    break
    return lst

def deletes_stop_words(lst):
    browser = 0
    for word in lst:
        if word in stopwords_list:
            if browser == 0:
                lst = lst[1:]
            else :
                if browser - 1 == 0:
                    lst = [lst[0]] + lst[browser+1:]
                else :
                    lst = lst[:browser]+lst[browser+1:]
        else :
            #word = word.lower()
            #w = nlp(word)
            lst = lst[:browser]+[lst[browser].lower()]+lst[browser+1:]
            browser += 1
    return lst

#revoir et tester sur jeu de mots
def lemmatization(lst):
    lemm = []
    for word in lst :
        dict = reseauxDump_norelin(word,19)
        #print(dict)
        #print("----------------------------------------------")
        if not dict == []:
            #print(dict[0]['t'])
            if len(dict)==1:
                index = 0
            else : 
                index = 1
            lemm += [dict[index]['t']]
            #print(lemm)
    return lemm



# researched_expression is a string
def related_comment(researched_expression):
    key_words = researched_expression.split(" ")
    returned_comments = []
    for key_word in key_words :
        for comment in comments : 
            words_from_comm = clean_expr_from_additionals(comment)
            if (key_word in words_from_comm
                and words_from_comm not in returned_comments): 
                returned_comments.append(words_from_comm)
                print(comment)
                print('\n')
            else :
                for word in words_from_comm :
                    if (key_word.lower() == word.lower() 
                        and words_from_comm not in returned_comments):
                        returned_comments.append(words_from_comm)
                        print(comment)
                        print('\n')
                        break


expr = "    /*----vue------/*----'(-----sur---+++'(-=)mer jjksq574 7865clj [\\++ '-,',? * ;/-------"
#expr = "    /*-vue/*-'(magnifique'(-=)iuezh jjksq574 7865clj [\\++ '-,',? * ;/"
#expr = "    /*----j'ai marché------/*----'(-----sur la---+++'(-=)mer jjksq574 7865clj [\\++ '-,',? * ;/-------"
#expr = "ùùùùSalut ça va"
# example of 2 mixed composed words
expression = "une magnifique belle vue sur la mer" 
expr = "j'ai témoigné d'une belle vue sur le champ de nature en neige"
expression = "vue sur la mer"
expression = "hey à vue de nez une belle vue vue sur la mer vue vue sur la mer vue vuu gdfs grand magasin vue sur la mer"
expression = " belle vue sur la mer vue sur mer belle ovierhj vue "
expression = " une une belle vue à vue de nez belle vue sur la mer djazh mer mer "
expression = " hey there what's you doing à vue de nez belle vue sur la mer pzeijd mer mer "
expression =  "détermination de la présence de taurine | technique indéterminée | nez | ponctuel | résultat qualitatif | présence/seuil"
expression = "une belle vue sur la mer vue"
expression = " Idée d'une histoire universelle au point de vue cosmopolitique "
expression = "Idée d'une histoire universelle au point de vue de la part de cosmopolitique"
print("\n---------------------------------------------------------->")
print("before cleaning from special chars")
print(expression)
expression = clean_expr_from_additionals(expression)
#print("-------------------------final")
#print(expression)
expression = gets_rid_of_dashes(expression)
#expression=cleanSpecialChar(expr)
print("\t->after cleaning from special chars")
print(expression)
print("\n")
print("\t->before detecting composed words:")
print(expression)
print("\t->after detecting composed words:")
#expression = detects_composed_words(expression)
#---------------------------------------------------------
# finds only composed words
expr=only_composed_words(expression)
print(expr)
#finds compsoed and not compseod words
expr1=composed_words_detecting(expression)
expr1_bis=cleanes_list_that_has_composes_words(expr1)
print(expr1_bis)
print("\n")
#----------------------------------------
'''
print("\t->before deleting stop words")
print(expression)
print("\t->after deleting stop words")
expression = deletes_stop_words(expression)
print(expression)
print("\n")
print("\t->before lemmatization")
print(expression)
print("\t->after lemmatization")
expression = lemmatization(expression)
print(expression)
lst = ['1', '2' , '3', '4','5','6','7']
print(lst[:3])
print(lst[3:])
'''
#-------------------------------------
'''
expression = deletes_stop_words(expression)
print(expression)
print("----------------------------------------------")
'''
'''
expression = " veux partir à londres"
expression = clean_expr_from_additionals(expression)
'''

#--------------------------------
#key_words = gets_rid_of_additional(key_words)
#print(key_words)

#related_comment("         vue         ")

'''
file = open("commentaires.txt")
print("hy")
for f in file :
    print(f)
'''

'''
-+ and [^[a-z]+-[a-z]+]
[^ [^-+]|[a-z]+-[a-z]+]
'''


# plus qu'un mot composé 
# continuer a voir s'il y a d'autres mots composés
#detecter tous els mots composés 
# rechercher les termes composés dans les avis 
# utiliser les relations pour étendre le résultat
# garder que les mots composés et les noms

# relation 3 , antologie
# filtrer : ne garder que les mots du domaine
# poids du terme (pas important)
# poids des relations importants
# après les mots composés
# filtrage par antologie 

''' QUESTIONS pour la prochaine séance 
1) idée d'une histoire au point de vue cosmopolitique
dans jeux de mots cette expression commence par une majuscule, si je cherche 
la meme expression et qu'au lieu que la première lettre soit en majuscule , 
je la mets en minuscule, est ce que l'algo doit reconnaitre l'expression 
commençant par une minuscule comme étant un mot composé meme si dans jeux de mots
cette expression commence par une majuscule ? 
'''




#['idée', 'd', 'une', 'histoire universelle', 'au point', 'point de vue', 'de vue', 'cosmopolitique']
#['idée', 'd', 'une', 'histoire universelle', 'au', 'au point de', 'au point', 'point de', 'point de vue', 'de vue', 'cosmopolitique']
#['idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'point de', 'point de vue', 'de vue', 'cosmopolitique']

#['une', 'belle vue', 'vue sur la mer', 'vue']
#['une', 'belle vue', 'vue sur la mer', 'vue']

#['détermination de la présence de taurine', 'détermination de la présence de taurine | technique indéterminée | nez | ponctuel | résultat qualitatif | présence/seuil', 'technique indéterminée', 'résultat qualitatif']
#['détermination de la présence de taurine', 'détermination de la présence de taurine | technique indéterminée | nez | ponctuel | résultat qualitatif | présence/seuil', 'technique indéterminée', 'résultat qualitatif']

#['hey', 'there', 'what', 's', 'you', 'doing', 'à vue', 'à vue de nez', 'belle vue', 'vue sur la mer', 'pzeijd', 'mer', 'mer']
#['hey', 'there', 'what', 's', 'you', 'doing', 'à', 'à vue', 'à vue de nez', 'belle vue', 'vue sur la mer', 'pzeijd', 'mer', 'mer']


#['une', 'une', 'belle vue', 'à vue', 'à vue de nez', 'belle vue', 'vue sur la mer', 'djazh', 'mer', 'mer']
#['une', 'une', 'belle vue', 'à', 'à vue', 'à vue de nez', 'belle vue', 'vue sur la mer', 'djazh', 'mer', 'mer']


#['belle vue', 'vue sur la mer', 'vue sur mer', 'sur mer', 'belle', 'ovierhj', 'vue']
#['belle vue', 'vue sur la mer', 'vue sur mer', 'sur mer', 'belle', 'ovierhj', 'vue']

#['hey', 'à vue', 'à vue de nez', 'une', 'belle vue', 'vue sur la mer', 'vue', 'vue sur la mer', 'vue', 'vuu', 'gdfs']
#['hey', 'à', 'à vue', 'à vue de nez', 'une', 'belle vue', 'vue sur la mer', 'vue', 'vue sur la mer', 'vue', 'vuu', 'gdfs']




#['de la part', 'la', 'idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'point de', 'point de vue', 'de vue', 'cosmopolitique']
#['de', 'la', 'de la part', 'idée', 'd', 'une', 'histoire universelle', 'au', 'au point de', 'au point', 'point de', 'point de vue', 'de vue', 'cosmopolitique']




#['de la part', 'idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'point de', 'point de vue', 'de vue', 'cosmopolitique']
#['de', 'la', 'de la part', 'idée', 'd', 'une', 'histoire universelle', 'au', 'au point de', 'au point', 'point de', 'point de vue', 'de vue', 'cosmopolitique']


#['idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'point de', 'point de vue', 'de vue', 'cosmopolitique', 'de la part']
#['idée', 'd', 'une', 'histoire universelle', 'au', 'au point de', 'au point', 'point de', 'point de vue', 'de vue', 'cosmopolitique', 'de', 'la', 'de la part']


#['idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'de la part de', 'de la part', 'de vue', 'cosmopolitique']
#['idée', 'd', 'une', 'histoire universelle', 'au', 'au point de', 'au point', 'point de', 'la', 'de la part de', 'de la part', 'de vue', 'cosmopolitique']
#['idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'de la part de', 'de la part', 'de vue', 'cosmopolitique']
#['idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'de la part de', 'de la part', 'de vue', 'cosmopolitique']


#['idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'point de', 'de la part', 'de vue', 'cosmopolitique']
#['idée', 'd', 'une', 'histoire universelle', 'au', 'au point de', 'au point', 'point de', 'la', 'de la part de', 'de la part', 'de vue', 'cosmopolitique']

#['idée', 'd', 'une', 'histoire universelle', 'au point', 'point de', 'de la part', 'de vue', 'cosmopolitique']
#['idée', 'd', 'une', 'histoire universelle', 'au point de', 'au point', 'point de', 'de la part de', 'de la part', 'de vue', 'cosmopolitique']
#['idée', 'd', 'une', 'histoire universelle', 'au', 'au point de', 'au point', 'point de', 'la', 'de la part de', 'de la part', 'de vue', 'cosmopolitique']


#---------------------------------------------------------------------
'''
def composed_words_detection(lst):
    resulting_list = []
    browser = 0
    index_of_latest_detected_cw = -1
    ldcw_len_indecator = -1
    index_of_single_word = -1
    while browser < len(lst):
        #print(lst[browser])
        related_composed_words = reseauxDump(lst[browser],11)
        rcw_browser = 1
        rcw_len = len(related_composed_words)
        while rcw_browser < rcw_len :
            composed_word = related_composed_words[rcw_browser]['t']
            cw_len=len(composed_word.split(" "))
            if list_to_string(lst[browser:cw_len+browser]) == composed_word:
                index_of_latest_detected_cw = browser
                ldcw_len_indecator = len(composed_word.split(" "))-1
                resulting_list+=[composed_word]
                print("resulting list composed word")
                print(resulting_list)
                index_of_single_word = -1
                #break
            if index_of_single_word != -1 :
                p_browser = index_of_single_word
                while p_browser < browser :
                    cleaned_composed_word = clean_expr_from_additionals(composed_word)
                    if lst[p_browser:cw_len+p_browser] == cleaned_composed_word:
                        index_of_latest_detected_cw = p_browser
                        ldcw_len_indecator = len(composed_word.split(" "))
                        if place == index_of_single_word:
                            if composed_word not in resulting_list:
                                print("trying to find the source of the problem")
                                print(resulting_list[:place])
                                print(composed_word)
                                print(resulting_list[place+1:])
                                print(place)
                                resulting_list = resulting_list[:len(resulting_list)-1]+[composed_word]#+resulting_list[place+1:]
                                print("resulting list backwards")
                                print(resulting_list)
                                place +=1
                        else :
                            if composed_word not in resulting_list :
                                resulting_list = resulting_list[:len(resulting_list)]+[composed_word]#+resulting_list[place:]
                                print("resulting list adding if not already there")
                                print(resulting_list)
                                place+=1
                        #resulting_list[index_of_single_word]=composed_word
                        #break
                    p_browser+=1
            rcw_browser+=1
        if rcw_len == rcw_browser or rcw_browser == 1 : # no composed word found
            if index_of_latest_detected_cw == -1 :
                resulting_list+=[lst[browser]]
                print("resulting list no composed word found")
                print(resulting_list)

                if index_of_single_word == -1:
                    index_of_single_word = browser
                    place = browser
            else :
                if browser-index_of_latest_detected_cw==ldcw_len_indecator:
                    index_of_latest_detected_cw = -1 
                    ldcw_len_indecator = -1
        browser+=1
    return resulting_list
'''  

'''
def composed_words_detection(lst):
    resulting_list = []
    browser = 0
    index_of_latest_detected_cw = -1
    ldcw_len_indecator = -1
    while browser < len(lst):
        #print(lst[browser])
        related_composed_words = reseauxDump(lst[browser],11)
        rcw_browser = 1
        rcw_len = len(related_composed_words)
        while rcw_browser < rcw_len :
            composed_word = related_composed_words[rcw_browser]['t']
            cw_len=len(composed_word.split(" "))
            if list_to_string(lst[browser:cw_len+browser]) == composed_word:
                index_of_latest_detected_cw = browser
                ldcw_len_indecator = len(composed_word.split(" "))-1
                resulting_list+=[composed_word]
                break
            rcw_browser+=1
        if rcw_len == rcw_browser or rcw_browser == 1 : # no composed word found
            if index_of_latest_detected_cw == -1 :
                resulting_list+=[lst[browser]]
            else :
                if browser-index_of_latest_detected_cw==ldcw_len_indecator:
                    index_of_latest_detected_cw = -1 
                    ldcw_len_indecator = -1
        browser+=1
    return resulting_list
'''
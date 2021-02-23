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

stopwords_list = stopwords.words('french')

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
            resulting_list+=[lst[browser]]
            last_added_is_a_cw = False
        browser+=1
    return resulting_list

# returns a list of words from the expression passed in parameters
# excluding stopwords
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
#expr = "j'ai témoigné d'une belle vue sur le champ de nature en neige"
expr1 = "vue sur la mer"
expression = "hey à vue de nez une belle vue vue sur la mer vue vue sur la mer vue vuu gdfs"
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
expression = gets_rid_of_dashes(expression)
print("\t->after cleaning from special chars")
print(expression)
print("\n")
print("\t->before detecting composed words:")
print(expression)
print("\t->after detecting composed words:")
expression=composed_words_detecting(expression)
print(expression)
print("\n")

print("\t->before deleting stop words")
print(expression)
print("\t->after deleting stop words")
expression = deletes_stop_words(expression)
print(expression)
print("\n")

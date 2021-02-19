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


def detects_composed_words(lst):
    resulting_list = []
    browser = 0
    #browsing lst
    while browser < len(lst) :
        #print("start of while browser")
        #print(browser)
        #print(lst[browser])
        dict = reseauxDump(lst[browser],11)
        dict_table=pd.DataFrame(dict).apply(pd.Series)
        if not dict_table.empty :
            print(dict_table)
        #print(dict_table.columns)
        dict_browser = 1
        # browsing the dictionary
        while dict_browser < len(dict):
            dict_expression = dict[dict_browser]['t']
            '''if lst[browser] == "vue" and dict_expression == "vue sur mer":# and dict_expression[0] == "vue" and dict_expression[1]=="sur":'''
            #print(dict_expression)
            dict_len = len(dict_expression.split(" "))
            #print(list_to_string(lst[browser:dict_len]))
            if list_to_string(lst[browser:dict_len])==dict_expression : 
                resulting_list += [dict_expression]
                #print("hey")
                #print(resulting_list)
                browser += dict_len
                dict_browser+=1
                #print("browser")
                #print(browser)
                break
            else :
                #print("else browser")
                #print(browser)
                dict_browser += 1
        #print("------------------")
        #print(dict_browser)
        #print("before if")
        #print(browser)
        if dict_browser>=len(dict) or dict_browser==1:
            #print("------------------------------------hey")
            #print(browser)
            resulting_list += [lst[browser]]
            browser+=1
        #print("while browser")
        #print(browser)
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
expression = "vue sur mer"
print("\n---------------------------------------------------------->")
print("before cleaning from special chars")
print(expr)
expression = clean_expr_from_additionals(expr)
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
expression = detects_composed_words(expression)
print(expression)
print("\n")
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

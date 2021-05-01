# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et une relation

import urllib.request
import pandas as pd
from operator import itemgetter
import re
import sys
import time

# Nettoyer le mot avant de le passer dans l'URL
def encodeURLTerme(terme):
    url_encode_terme = terme.replace("%", "%25").replace(" ", "%20").replace('""', "%22").replace("#", "%23").replace("$", "%24").replace("&", "%26").replace("'", "%27").replace(
        "(", "%28").replace(")", "%29").replace("*", "%2A").replace("+", "%2B").replace(",", "%2C").replace(";", "%3B").replace("<", "%3C").replace("=", "%3D").replace(">", "%3E").replace("?", "%3F").replace("@", "%40").replace("[", "%5B").replace("]", "%5D").replace("^", "%5E").replace("`", "%60").replace("{", "%7B").replace("|", "%7C").replace("}", "%7D").replace("~", "%7E").replace("¢", "%A2").replace("£", "%A3").replace("¥", "%A5").replace("|", "%A6").replace("§", "%A7").replace("«", "%AB").replace("¬", "%AC").replace("¯", "%AD").replace("º", "%B0").replace("±", "%B1").replace("ª", "%B2").replace(",", "%B4").replace("µ", "%B5").replace("»", "%BB").replace("¼", "%BC").replace("½", "%BD").replace("¿", "%BF").replace("À", "%C0").replace("Á", "%C1").replace("Â", "%C2").replace("Ã", "%C3").replace("Ä", "%C4").replace("Å", "%C5").replace("Æ", "%C6").replace("Ç", "%C7").replace("È", "%C8").replace("É", "%C9").replace("Ê", "%CA").replace("Ë", "%CB").replace("Ì", "%CC").replace("Í", "%CD").replace("Î", "%CE").replace("Ï", "%CF").replace("Ð", "%D0").replace("Ñ", "%D1").replace("Ò", "%D2").replace("Ó", "%D3").replace("Ô", "%D4").replace("Õ", "%D5").replace("Ö", "%D6").replace("Ø", "%D8").replace("Ù", "%D9").replace("Ú", "%DA").replace("Û", "%DB").replace("Ü", "%DC").replace("Ý", "%DD").replace("Þ", "%DE").replace("ß", "%DF").replace("à", "%E0").replace("á", "%E1").replace("â", "%E2").replace("ã", "%E3").replace("ä", "%E4").replace("å", "%E5").replace("æ", "%E6").replace("ç", "%E7").replace("è", "%E8").replace("é", "%E9").replace("ê", "%EA").replace("ë", "%EB").replace("ì", "%EC").replace("í", "%ED").replace("î", "%EE").replace("ï", "%EF").replace("ð", "%F0").replace("ñ", "%F1").replace("ò", "%F2").replace("ó", "%F3").replace("ô", "%F4").replace("õ", "%F5").replace("ö", "%F6").replace("÷", "%F7").replace("ø", "%F8").replace("ù", "%F9").replace("ú", "%FA").replace("û", "%FB").replace("ü", "%FC").replace("ý", "%FD").replace("þ", "%FE").replace("ÿ", "%FF").replace(u"\x9c", "oe")
    return url_encode_terme

# Verifier si le mot n'est pas déja enregistré
def cacheExists(filename):
    try :
        with open("jdm_cache/"+filename) as my_file:
            return my_file
    except :
        return False        


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


# récupérer une liste des mot avec un saut de ligne
def getWordsFromDict(words_dict):
    words_list=[]
    for word_dict_item  in words_dict:
        words_list.append("\n"+word_dict_item)
        # print(word_dict_item)
    
    return words_list

# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et une relation
def reseauxDump(terme, numRel):
    idDuTerme = -1
    filename=terme+"_"+str(numRel)+".txt"
    if (cacheExists(filename)):
        # print("cache exists ")
        # je retourne les mots apartire du fichier en qst 
        try :
            with open("jdm_cache/"+filename) as my_file:
                # print (my_file.readlines())
                return formatResault(filterTermesAndRelations(my_file.readlines()))
               
        except :
            print ("problem while oppening file ")
        
    else :
        # je lance la requete  j'ecrit le fichier et je retourn les mots 
        with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}".format(encodeURLTerme(terme), numRel)) as url:
            s = url.read().decode('ISO-8859-1')
            line = s.split("\n")

            words = filterTermesAndRelations(line)

            # print(formatResault(filterTermesAndRelations(line)))
            saveWords(terme,numRel,words)
            # print(filterTermesAndRelations(line))
           
            return formatResault(filterTermesAndRelations(line))

# Exectution d'une requetes  sur Réseaux Dumpe pour un terme  et 
# une relation (seulment les relations sortantes sont prises en comptes )
def reseauxDumpByRelations(terme, numRel):

    idDuTerme = -1
    filename=terme+"_"+str(numRel)+".txt"
    if (cacheExists(filename)):
        # print("cache exists ")
        # je retourne les mots apartire du fichier en qst 
        try :
            with open("jdm_cache/"+filename) as my_file:
                # print (my_file.readlines())
                return formatResaultByRelation(filterTermesAndRelations(my_file.readlines()))
               
        except :
            print ("problem while oppening file ")
        
    else :
        print("cache not found  ")
        # je lance la requete  j'ecrit le fichier et je retourn les mots 


        with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}".format(encodeURLTerme(terme), numRel)) as url:
            s = url.read().decode('ISO-8859-1')
            line = s.split("\n")

            words = filterTermesAndRelations(line)

            # print(formatResault(filterTermesAndRelations(line)))
            saveWords(terme,numRel,words)
            # print(filterTermesAndRelations(line))
            
            return formatResaultByRelation(filterTermesAndRelations(line))


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
    p2 = ":"
    for line in lines:
        casesTermes = line.split(";")
        # on filtre les lignes des relations ainsi que les termes en anglais
        if (not casesTermes[0] == "r" and not en in casesTermes[2] and not sup in casesTermes[2] and not inf in casesTermes[2]and not "_COM" in casesTermes[2] and not p2 in casesTermes[2] ):

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
        if (not casesTermes[0] == "r" and not en in casesTermes[2] and not sup in casesTermes[2] and not inf in casesTermes[2]and not "_COM" in casesTermes[2] and not p2 in casesTermes[2] ):

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

    returned_words_dict = []
    searched_word = {"id":words[0].get("id"),"t":words[0].get("t"),"rw":float(999)}
    # print(f"searched word {searched_word}")
    for line1 in lines:
        splitedTermes = line1.split(";")
       
        # on filtre les relations sortoantes et on produits la liste des mot qui sont lier au mot concérner 
        if (splitedTermes[0] == "r" and int(splitedTermes[2])== words[0].get("id")and len(splitedTermes)==6 and int(splitedTermes[3])!=239128):
            id_terme1 = int(splitedTermes[2])
            id_terme2= int(splitedTermes[3])
            if(splitedTermes[5]!="w"):
                weight = float(splitedTermes[5]) 
            else :
                weight = 0 
            #relation terme1---------> terme2
            
            relation_dict = {"id":id_terme2,"t":getTermeById(id_terme2,words),"rw":weight}
            returned_words_dict.append(relation_dict)
            # print(relation_dict)

        # supprimer les temres non retrouver 
    res = list(filter(lambda i: i['t'] != None, returned_words_dict))
    res.append(searched_word)
    # print (res)
    # print(len(res))
        
    return res


def getTermeById(id,words):
    for w in words : 
        if (id==w["id"]):
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


# Récupérer  seulement les terme apartire de chaque dictionaire pour la relation 0
def getTermesR0(word):
    words_list = []
    words_dict = reseauxDump(word, 0)
    for w in words_dict:
        if (w["t"]!= word):
            words_list.append(w.get("t"))
    # print(words_list)
    return words_list


# Récupérer  seulement les terme sortant  apartire de chaque dictionaire pour la relation 0
def getTermesR0Sortants(word):
    words_list = []
    words_dict = reseauxDumpByRelations(word, 0)
    for word in words_dict:
        words_list.append(word.get("t"))
    #print(words_list)
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
        if (w["t"]!= word):
            words_list.append(w.get("t"))
    # print(words_list)
    return words_list


def getTermesR6(word):
    words_list = []
    words_dict = reseauxDump(word, 6)
    for w in words_dict:
        if (w["t"]!= word):
            words_list.append(w.get("t"))
    # print(words_list)
    return words_list


def getTermesR9(word):
    words_list = []
    words_dict = reseauxDump(word, 9)
    for w in words_dict:
        if (w["t"]!= word):
            words_list.append(w.get("t"))
    # print(words_list)
    return words_list


#----------------------------------my part
# retrieving comments from thhe text file
com = pd.read_csv('commentaires.txt', header = None)
comments = com[0]


# in case a typed research ends with multipule spaces this function gets
# rid of them

def gets_rid_of_empty_quotes(lst):
    while len(lst)-1>=0 and lst[len(lst)-1] == '' :
        lst = lst[:len(lst)-1]
    while len(lst)-1>=0 and lst[0] == '' :
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
    i=ii=iii=0
    while browser < len(lst):
        if skip != -1 and browser > skip :
            skip = -1
            leave = len(resulting_list)
        related_composed_words = reseauxDump(lst[browser],11)
        rcw_browser = 1
        if related_composed_words!=None:
            rcw_len = len(related_composed_words)
            len_rl_before = len(resulting_list)
            while rcw_browser < rcw_len :
                composed_word = related_composed_words[rcw_browser]['t']
                cleaned_composed_word = clean_expr_from_additionals(composed_word)
                cw_len = len(cleaned_composed_word)
                if cleaned_composed_word != [] and (lst[browser:cw_len+browser] == cleaned_composed_word): 
                    index_of_latest_cw = len(resulting_list)
                    if (composed_word not in resulting_list[leave:len(resulting_list)]) or skip == -1 :
                        resulting_list+=[composed_word]
                        if skip == -1 or browser < skip:
                            var = browser
                        else: 
                            var = skip
                        
                        skip = max(skip,len(cleaned_composed_word)+var-1)#-1
                    else:
                        if skip == -1 or browser > skip:
                            resulting_list+=[composed_word]
                    
                    len_longest_composed_word = max(len_longest_composed_word,browser+len(cleaned_composed_word))
                if browser != 0 :                
                    if lst[browser] in cleaned_composed_word :
                        i = cleaned_composed_word.index(lst[browser])
                        ii = len(cleaned_composed_word[:i])
                        iii = len(cleaned_composed_word[i:])
                    if (cleaned_composed_word != [] and ((lst[browser-ii:browser+iii])== cleaned_composed_word)):
                        if (composed_word not in resulting_list[leave:len(resulting_list)]) or skip == -1 :
                            resulting_list+=[composed_word]
                            if skip == -1 or browser <= skip:
                                var = browser-ii
                            else: 
                                var = skip

                            if skip == -1 :
                                b = browser
                            skip = max(skip,len(cleaned_composed_word)+var-1)#-1
                        else:
                            if skip == -1 or browser > skip:
                                resulting_list+=[composed_word]
                        while len(resulting_list[len(resulting_list)-2].split(" "))==1 and resulting_list[len(resulting_list)-2].split(" ")[0] in resulting_list[len(resulting_list)-1].split(" "):
                            resulting_list = resulting_list[:len(resulting_list)-2]+resulting_list[len(resulting_list)-1:]
                        index_of_latest_cw = len(resulting_list)-1
                        len_longest_composed_word = max(len_longest_composed_word,browser-ii+len(cleaned_composed_word))
                rcw_browser+=1            
            if len_rl_before == len(resulting_list) and browser >= len_longest_composed_word:
                resulting_list+=[lst[browser]]
                last_added_is_a_cw = False
        browser+=1
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
    i=ii=iii=0
    b = 0
    while browser < len(lst):
        if skip != -1 and browser > skip :
            skip = -1
            leave = len(resulting_list)
        related_composed_words = reseauxDump(lst[browser],11)
        rcw_browser = 1
        if related_composed_words!=None:
            rcw_len = len(related_composed_words)
            len_rl_before = len(resulting_list)
            while rcw_browser < rcw_len :
                composed_word = related_composed_words[rcw_browser]['t']
                cleaned_composed_word = clean_expr_from_additionals(composed_word)
                cw_len = len(cleaned_composed_word)
                if cleaned_composed_word != [] and (lst[browser:cw_len+browser] == cleaned_composed_word):                
                    index_of_latest_cw = len(resulting_list)
                    if (composed_word not in resulting_list[leave:len(resulting_list)]) or skip == -1: 
                        l = len(resulting_list[leave:len(resulting_list)])                   
                        if l==0 and len(resulting_list)==0:
                            resulting_list+=[composed_word]
                        else :
                            if (len(resulting_list)!=0 and (composed_word != resulting_list[len(resulting_list)-1]) and 
                                composed_word not in resulting_list[len(resulting_list)-1]): 
                                if resulting_list[len(resulting_list)-1] in composed_word :
                                    resulting_list[len(resulting_list)-1]=composed_word
                                else :
                                    resulting_list+=[composed_word]
                        if skip == -1 or browser < skip:
                            var = browser
                        else: 
                            var = skip
                        skip = max(skip,len(cleaned_composed_word)+var-1)#-1
                    else:
                        if skip == -1 or browser > skip:
                            l = len(resulting_list[leave:len(resulting_list)])                   
                            if l==0:
                                resulting_list+=[composed_word]
                            else :
                                if (len(resulting_list)!=0 and (composed_word != resulting_list[len(resulting_list)-1]) and 
                                    composed_word not in resulting_list[len(resulting_list)-1]): 
                                    if resulting_list[len(resulting_list)-1] in composed_word :
                                        resulting_list[len(resulting_list)-1]=composed_word
                                    else :
                                        resulting_list+=[composed_word]
                    len_longest_composed_word = max(len_longest_composed_word,browser+len(cleaned_composed_word))
                if browser != 0 :                
                    if lst[browser] in cleaned_composed_word :
                        i = cleaned_composed_word.index(lst[browser])
                        ii = len(cleaned_composed_word[:i])
                        iii = len(cleaned_composed_word[i:])
                    if (cleaned_composed_word != [] and ((lst[browser-ii:browser+iii])== cleaned_composed_word)):
                        if (composed_word not in resulting_list[leave:len(resulting_list)]) or skip == -1: 
                            l = len(resulting_list[leave:len(resulting_list)])
                            if len(resulting_list)!=0 and composed_word not in resulting_list[len(resulting_list)-1]:
                                if l==0 or len(resulting_list)==0:
                                    resulting_list+=[composed_word]
                                else :
                                    if (len(resulting_list)!=0 and (composed_word != resulting_list[len(resulting_list)-1]) and 
                                        composed_word not in resulting_list[len(resulting_list)-1]): 
                                        if resulting_list[len(resulting_list)-1] in composed_word :
                                            resulting_list[len(resulting_list)-1]=composed_word
                                        else :
                                            resulting_list+=[composed_word]
                            if skip == -1 or browser <= skip:
                                var = browser-ii
                            else: 
                                var = skip

                            if skip == -1 :
                                b = browser
                            skip = max(skip,len(cleaned_composed_word)+var-1)#-1
                        else:
                            if skip == -1 or browser > skip:
                                l = len(resulting_list[leave:len(resulting_list)])                   
                                if l==0:
                                    resulting_list+=[composed_word]
                                else :
                                    if (len(resulting_list)!=0 and (composed_word != resulting_list[len(resulting_list)-1]) and 
                                        composed_word not in resulting_list[len(resulting_list)-1]): 
                                        if resulting_list[len(resulting_list)-1] in composed_word :
                                            resulting_list[len(resulting_list)-1]=composed_word
                                        else :
                                            resulting_list+=[composed_word]
                        if (len(resulting_list)>=2):
                            while (len(resulting_list[len(resulting_list)-2].split(" "))==1 
                                and resulting_list[len(resulting_list)-2].split(" ")[0] in resulting_list[len(resulting_list)-1].split(" ")
                                and skip != -1):
                                resulting_list = resulting_list[:len(resulting_list)-2]+resulting_list[len(resulting_list)-1:]
                        index_of_latest_cw = len(resulting_list)-1
                        len_longest_composed_word = max(len_longest_composed_word,browser-ii+len(cleaned_composed_word))
                rcw_browser+=1            
            if len_rl_before == len(resulting_list) and browser >= len_longest_composed_word:
                resulting_list+=[lst[browser]]
                last_added_is_a_cw = False
        browser+=1
    return resulting_list 


#--------------------------------------testing area
expression = "Superbe chambre, spacieuse, vue sur le parc Très beau domaine, calme, en harmonie avec la nature Nombreuses possibilités de balades alentours, à pied ou à vélo Plats maison et bien cuisinés Hôtes très aimables, à l'écoute, et à nos petits soins"

print("\n") 
print("\t->before detecting composed words:")
print(expression)
print("\n")

print("\t->after detecting composed words:")
startTime = time.time()

expr=composed_words_cleaner_version(expression)
print(expr)
print("\n")

executionTime = (time.time()-startTime)
print("Execution time in seconds composed_words_cleaner_version: "+str(executionTime))


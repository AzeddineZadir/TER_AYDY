import urllib.request
import re


def reseauxDump(terme, numRel):
    # prend un temre et une relation, extrait de jeux de mot et retourne des liste de termes et de relations
    
    idDuTerme = -1
    termeURL = terme.replace("é", "%E9").replace("è", "%E8").replace("ê", "%EA").replace(
        "à", "%E0").replace("ç", "%E7").replace("û", "%FB").replace(" ", "+")

    with urllib.request.urlopen("http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={}&rel={}".format(termeURL, numRel)) as url:
        s = url.read().decode('ISO-8859-1')
        line = {}
        line=s.split("\n")
        
        filterReseauxDumpReturn(line)
       
        return 0;


def filterReseauxDumpReturn(lines):
    words = []
    regx = "((e;[0-9]+;.*)|(r;[0-9]+;.*))"
    for item in lines:
        x = re.search("((e;[0-9]+;.*)|(r;[0-9]+;.*))", item)
        
        if x != None:
            print(x.group())             
    
    return words

def 

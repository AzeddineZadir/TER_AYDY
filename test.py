#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import spacy
import json
import numpy as np
nlp = spacy.load("fr_core_news_sm")

def return_token(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte de chaque token
    return [X.text for X in doc]


user_ = "un très bon acceuil"

dictio =["bon", "très", "bcp","acceuil", "quantitatif", "quantité", "fortement", "intensité", "super", "foutrement", "généreusement", "trop", "pas", "much", "excessivement", "peu", "au plus haut point", "cruellement", "salement", "parfaitement", "bigrement", "adverbe", "vraiment", "soupçon", "sérieusement", "drôlement", "extrêmement", "bien", "sensiblement", "assez", "joliment", "supérieurement", "immensément", "tout à fait", "effroyablement", "à l'excès", "absolument", "pleinement", "moult", "énormément", "exceptionnellement", "follement", "formidablement", "durement", "agressivement", "tout", "hyper", "largement", "Très", "merveilleusement", "furieusement", "tout plein", "rudement", "éperdument", "passionnément", "terriblement", "vigoureusement", "odieusement", "généralement", "infiniment", "abusivement", "tellement", "intensément", "Tres", "gavé", "prodigieusement", "incroyablement", "horriblement", "richement", "rien", "extraordinairement", "fermement", "méchamment", "hargneusement", "violemment", "hautement", "vachement", "diablement", "tres", "remarquablement", "fort", "beaucoup", "_COM", "grumeleux", "poudrin", "flegmatique", "buissonnant", "slicer", "fritter", "Thales", "Invincible Armada", "achalander", "loquace", "galbe", "volailler", "ductile", "fluorhydrique", "quartzeux", "incapacitant", "psychologisme", "failler", "brunissement", "poissonneux", "introspectif", "thermiquement", "ininflammable", "concevable", "cordialement", "ubiquitaire", "bouture", "iridescent", "eutrophe", "laconique", "blondeur", "ambulacre", "pubescence", "relaxant", "dissemblable", "impressionnable", "zoochorie", "singulariser", "indusie", "diplodocus", "perfectionniste", "marginalement", "ascensionniste", "lisiblement", "ostensible", "tavelure", "pictographique", "prognathe", "velociraptor", "transpirant", "endurant", "drolatique", "acculturer", "plaqueur", "souvent", "L'Homme invisible", "centennal", "liposoluble", "stylistiquement", "nettement", "papillomavirus", "biologie", "Zen", "histoire d'Athènes", "liquide", "argent", "fennec", "Beau travail !", "fort de café", "se jeter contre [qch]", "se jeter contre quelque chose", "très impatient de commencer", "castagner [qqn]", "castagner quelqu'un", "castagner", "tôt le matin", "chargé à bloc", "c'est du bon boulot", "abusive", "à un tour de roue", "funk", "groupuscule", "une garce de", "vie de chien", "Coeur de Lion", "pas possible", "payer rubis sur l'ongle", "comme toi et moi", "comme toi ou moi", "de bon matin", "myope comme une taupe", "n'avoir jamais été à pareil fête", "n'avoir rien en commun avec", "nannofossile", "nanocorme", "nanomélie", "ne pas avoir la langue dans sa poche", "ne pas dater d'hier", "ne pas en mener large", "ne plus avoir goutte sang", "ne tenir qu'à fil", "nid d'aigle", "olympien", "orthoacide", "os éburné", "plat comme limande", "plat comme une galette", "plat comme une punaise", "plein à craquer", "plein comme un oeuf", "plein comme une huître", "plus tôt sera le mieux", "poilant", "pointu", "pour ce que ça vaut", "prendre des libertés avec", "raide comme des baguettes de tambour", "raisonner comme un sabot", "raisonner comme un tambour", "raisonner comme une pantoufle", "raisonner comme une savate", "rapproché", "rase-pet", "regarder à la dépense", "réglé comme du papier à musique", "réglé comme une horloge", "rembourré avec noyaux pêche", "rire comme un bossu", "rire comme un fou", "rire comme un petit fou", "rire comme une baleine", "roman-fleuve", "ronger les sangs", "rouler les yeux", "rupin", "sacré", "sacro-saint", "salé", "trapu", "triste à pleurer", "trois quarts d'heure", "ultra-chic", "ultramoderne", "un abîme de", "un atome de", "un chouïa de", "un filet de", "un froid de canard", "un froid de loup", "un soupçon de", "une chienne de", "une fraction de", "une infinité de", "une paye de", "une trace de", "vélin","adn", "squelette", "bras", "tête", "jambes", "cou", "ADN", "nez", "corps", "pied", "jambe", "acide désoxyribonucléique", "être vivant", "sensation agréable", "saveur", "mets", "bon du Trésor", "manger", "copie", "échantillon", "spécimen", "heureux", "comestible", "précieux", "méritant", "vertueux", "sérieux", "brave", "savoureux", "humain", "satisfaisant", "honnête", "bonhomme", "fameux", "bienfaisant", "productif", "désintéressé", "noble", "adroit", "performant", "correct", "ingénu", "merveilleux", "certain", "gai", "abondant", "fort", "considérable", "boniface", "calembourg", "amusant", "décent", "coupure", "emballé", "ingénieux", "sauf", "rigoureux", "drôle", "valide", "fait", "heureuses", "humaine", "fidèles", "apprécier", "se régaler", "entériner", "cuisine", "adorable", "affable", "type", "clément", "typique", "bénéfique", "commode", "magnanime", "jouisseur", "gracieux", "expert", "apte", "dévoué", "délectable", "meilleur", "benoît", "cher", "moyen", "héroïque", "sensible", "riche", "robuste", "utilisable", "avisé", "spirituel", "cordial", "certifié", "convaincant", "valeur", "friand", "faste", "bête", "soit", "gracieuse", "gaies", "compétent", "personne", "individu", "être humain", "gay", "sociable", "brillant", "bonasse", "représentatif", "prototype", "propice", "chanceux", "pacifique", "joyeux drille", "indulgent", "autorisation", "estimable", "approprié", "altruiste", "adéquat", "susceptible", "chic", "paterne", "gros", "parfait", "sûr", "acceptable", "bénévole", "opérant", "souverain", "énergique", "pondéré", "délicieuse", "décente", "bienveillante", "divin", "élégant", "caritatif", "tolérant", "tranquille", "digne", "débonnaire", "jugement", "charitable", "calembour", "boute-en-train", "propre", "profitable", "épicurien", "prodigue", "appétissant", "Bon", "exquis", "génial", "prudent", "agréablement", "chéri", "pitoyable", "forte", "affectueux", "chrétien", "enviable", "piquant", "intéressante", "succulente", "certains", "intègre", "bonniste", "psychologie", "voix", "bruit", "façon", "manière", "céleste", "mou", "mangeable", "fructueux", "serviable", "rentable", "bien-fondé", "raté", "bienfaiteur", "attestation", "entendement", "potable", "suave", "haut", "supérieur", "candide", "judicieux", "grand", "solide", "complaisant", "valable", "remarquable", "salutaire", "secourable", "comme il faut", "accessible", "suffisant", "bien tassé", "crédule", "plein", "éclairé", "sauvé", "innocente", "déclaration", "en bas", "beau", "avantageux", "innocent", "pratique", "miel", "bon d'achat", "Adj", "chaud", "décence", "convenable", "ticket", "capable", "bienveillant", "raison", "exemplaire", "efficace", "angélique", "modèle", "sain", "jugeotte", "extra", "belle", "intéressant", "joli", "distingué", "strict", "lucratif", "véritable", "reposant", "vénérable", "aromatique", "admissible", "paternel", "à point", "gaie", "exquise", "commerce", "admirable", "simple", "gars", "édifiant", "consommable", "important", "titre", "jugeote", "consciencieux", "sage", "habile", "pondération", "moral", "géniale", "fidèle", "droit", "pur", "ferme", "tutélaire", "Sains", "recevable", "bonard", "cuit", "Gentil", "sentimental", "naïf", "justes", "vertueuse", "bienfaisante", "affectueuse", "effet de commerce", "conclusion", "au porteur", "avenant", "coruscant", "accueillant", "favorable", "faible", "compatissant", "opportun", "inoffensif", "louable", "nécessaire", "miséricordieux", "utile", "quolibet", "astuce", "prêt", "franc", "équitable", "marine", "droite", "stable", "passable", "obligeant", "formidable", "honorable", "costaud", "délicieusement", "fertile", "adoré", "authentique", "courageux", "naïve", "délicate", "plaisant", "charmant", "amical", "archétype", "épreuve", "humanoïde", "anodin", "calme", "méritoire", "indispensable", "climats", "valeurs mobilières", "interjections", "salutations", "philosophie", "sottise", "norme", "honnêteté", "mariage", "simplicité", "générosité", "opportunité", "plaisir", "intensité", "normalité", "conformité", "avoir", "rémunérateur", "bénin", "promis", "délicat", "joyeux", "militaire", "tendre", "vrai", "raisonnable", "biquet", "instructif"]

def pertinence(comment):
    user =[]
    avis =[]
    for token in return_token(user_) :
        user.append(1)

    for token in return_token(user_):
        if token in return_token(comment):
                avis.append(10)
        else : 
            if token in dictio:
                avis.append(1)
            else :
                avis.append(0)
    mult = np.multiply(user,avis)    
    result = np.sum(mult)
    return result



def Sortpertinance(comments):
    bestComments = []
    pert =[]
    for comment in comments:
        pert.append(pertinence(comment))

    dico = "{"
    for index,item in enumerate(pert):
        
        dico+="'{}':'{}',".format(index,item)
    size = len(dico)
    dico = dico[0:size-1]
    dico+="}"
    finalDic = eval(dico)
    finalDic = {k: v for k, v in sorted(finalDic.items(), key=lambda item: int(item[1]) ,reverse=True)}
    
    
    print(finalDic)
    for key in finalDic :
     
        bestComments.append(comments[int(key)])
        
    return bestComments
     

comments=["super acceuil","un acceuil trés chaleureux","une trés bonne expérience"]
bestComments = Sortpertinance(comments)
print(bestComments)
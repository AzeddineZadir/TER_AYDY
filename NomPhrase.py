def getNom(sentence):
    Nom =[]
    pos = stanzaPosTagging(sentence)
    for phrase in pos:
        for mot in phrase:
            if "NOUN" in mot.values():
                nom = ""
                # print(mot)
                for n in mot.keys():
                  nom = n
                #   print(nom)
                  Nom.append(nom)
    posJDM = posTagging(sentence)
    for phrase in posJDM:
        for mot in phrase:
            if "Nom" in mot.values():
                for nom in mot.keys():
                    if nom not in Nom:
                        Nom.append(nom)
    return Nom

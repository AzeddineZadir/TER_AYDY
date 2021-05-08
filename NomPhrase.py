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

    return Nom
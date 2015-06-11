# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks, returnValue

# Fonctions d'aide utilisées à plusieurs endroits
class Helper(object):
    def __init__(self, provider):
        self.provider = provider

    @inlineCallbacks
    def parsecondition(self, condition):
        "Remplace les noms d'attributs de services par leur valeur"

        #Trouver tout ce qui est entre crochets
        services = []
        toreplace = str(condition).split("[")
        for part in toreplace:
            if part.find(']') != -1:
                services.append(part.split(']')[0])

        #Parcourir la liste de valeurs trouvées
        for serv in services:
            s = serv.split('.')
            oldvalue = "[" + str(serv) + "]"
            newvalue = None
            if s[0] == self.provider.name: # Lire directement l'attribut d'un service local
                try:
                    newvalue = self.provider.services[s[1]].access(s[2])
                except Exception:
                    pass
            elif self.provider.net_session: # Si la session réeau existe, lire à distance
                try:
                    newvalue = yield self.provider.net_session.call(s[0]+ '.serv.' +s[1], s[2])
                except Exception:
                    pass
            #Remplacer le nom d'attribut par sa valeur
            condition = condition.replace(oldvalue, str(newvalue))

        # Les opérateurs de comparaison fonctionnent entre parenthèse dans eval
        condition = "(" + str(condition) + ")"
        try: # Bloquer l'accès aux fonctions sauf abs, round, min et max
            retour = eval(condition, {"__builtins__": None}, {"abs": abs, "round": round, "min":min, "max":max})
        except: # La condition n'est pas évaluable
            retour = None

        returnValue(retour)
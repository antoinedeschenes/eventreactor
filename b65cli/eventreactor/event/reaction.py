# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks, returnValue

__author__ = 'Antoine Deschênes'

class Reaction(object):
    def __init__(self, provider, service_attribute, value, execute = False):
        # Construire la réaction
        self.provider = provider
        self.service_attribute = service_attribute
        self.value = value
        if execute:
            self.execute()

    @inlineCallbacks
    def execute(self):

        #Parser la formule de valeur, l'évaluer puis prendre la valeur de retour.
        value = yield self.provider.helper.parsecondition(self.value)

        s = self.service_attribute.split('.')
        # Vérifier si l'attribut est local (même nom de machine) ou distant
        # Si la connexion ne fonctionne plus, les événements locaux continuent de fonctionner.
        if s[0] == self.provider.name: #Local
            try: # Accéder directement au service local
                self.provider.services[s[1]].access(s[2], value)
            except Exception: # Retourne faux si non réussi
                returnValue(False)
        elif self.provider.net_session: # Si la session existe
            try: # Faire un appel distant si le service est ailleurs
                yield self.provider.net_session.call(s[0]+ '.serv.' +s[1], s[2], value)
            except:
                returnValue(False)
        else: #Appel distant et non connecté au serveur, ne rien faire.
            returnValue(False)
        returnValue(True)
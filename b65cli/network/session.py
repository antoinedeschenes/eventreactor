# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import auth
from twisted.internet.defer import inlineCallbacks, returnValue

# Toute l'action réseau se passe ici. On doit
# au minimum redéfinir onJoin de ApplicationSession
class Session(ApplicationSession):
    # Méthodes redéfinies

    def onDisconnect(self):
        super(Session, self).onDisconnect()
        #Vider la référence net_session dans le Provider
        self.mainapp.net_session = None

    def onConnect(self):
        "Envoyer son nom d'usager"
        self.join(self.config.realm, [u"wampcra"], "provider")

    def onChallenge(self, challenge):
        "Répondre à la demande de mot de passe"
        signature = auth.compute_wcs("secret".encode("utf8"), challenge.extra['challenge'].encode('utf8'))
        return signature.decode('ascii')

    @inlineCallbacks
    def onJoin(self, details):
        "Fonction vide redéfinie : actions à faire lorsque la connexion est réussie"

        #Donner une référence à la session au Provider.
        self.mainapp = self.config.extra["mainapp"]
        self.mainapp.net_session = self

        #Enregistrer les fonctions pour retourner la structure du Provider et modifier la configuration
        yield self.register_or_replace_rpc(str(self.mainapp.get_name()) + '.structure', self.mainapp.get_structure)
        yield self.register_or_replace_rpc(str(self.mainapp.get_name()) + '.configure', self.mainapp.configure)

        #Enregistrer tous les services et événements existants
        for service in self.mainapp.services:
            yield self.register_service(service)

        for event in self.mainapp.events:
            yield self.register_event(event)

        print("Event Reactor: online session started")

    # Nouvelles méthodes à partir d'ici :

    @inlineCallbacks
    def register_service(self, service):
        "Pour enregistrer un service"
        yield self.register_or_replace_rpc(str(self.mainapp.get_name()) + '.serv.' + str(service), self.mainapp.services[service].access)

    @inlineCallbacks
    def unregister_service(self, service):
        "Pour désenregistrer un service"
        yield self.unregister_rpc(self.mainapp.get_name() + '.serv.' +service)

    @inlineCallbacks
    def register_event(self, event):
        "Pour enregistrer un événement"
        yield self.register_or_replace_rpc(str(self.mainapp.get_name()) + '.evt.' + str(event), self.mainapp.events[event].access)

    @inlineCallbacks
    def unregister_event(self, event):
        "Désenregistrer un événement"
        yield self.unregister_rpc(self.mainapp.get_name() + '.evt.' + event)

    @inlineCallbacks
    def register_or_replace_rpc(self, procedure, func):
        "Enregistre la méthode d'appel à un service ou événement. \
        la méthode sera désenregistrée au préalable si elle existait déjà."

        # S'assurer de désenregistrer un appel avant de l'enregistrer
        yield self.unregister_rpc(procedure)
        try:
            yield self.register(func, procedure)
        except Exception as e: # Problème retourne faux
            print e
            returnValue(False)
        returnValue(True)

    @inlineCallbacks
    def unregister_rpc(self, procedure):
        "Retire un enregistrement de procédure existant."
        for i in self._registrations.keys(): # Trouver la clé correspondante au nom d'appel
            if self._registrations[i].procedure == procedure:
                try: # Désenregistrer la clé
                    yield self._unregister(self._registrations[i])
                except Exception as e:
                    print e


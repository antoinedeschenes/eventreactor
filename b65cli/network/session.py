# -*- coding: utf-8 -*-
from time import sleep
from twisted.internet.task import LoopingCall

__author__ = 'Antoine Deschênes'
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import auth
from twisted.internet.defer import inlineCallbacks

class Session(ApplicationSession):
    def onDisconnect(self):
        super(Session, self).onDisconnect()
        self.mainapp.net_session = None
        print("sessionDisconnect")

    # Nom d'usager pour la connexion
    def onConnect(self):
        self.join(self.config.realm, [u"wampcra"], "provider")

    #Retourner le mot de passe encrypté
    def onChallenge(self, challenge):
        signature = auth.compute_wcs("secret".encode("utf8"), challenge.extra['challenge'].encode('utf8'))
        return signature.decode('ascii')

    #Connexion d'un autre usager
    def onjn(self, msg):
        print(msg)
        print(msg["authrole"])

    #Deconnexion d'un autre usager
    def onlv(self, msg):
        print(msg)

    @inlineCallbacks
    def onJoin(self, details):
        print("sessionJoin")

        self.mainapp = self.config.extra["mainapp"]
        self.mainapp.net_session = self

        "Choses à faire lorsqu'une connexion est réussie"
        yield self.subscribe(self.onjn, 'wamp.session.on_join')
        yield self.subscribe(self.onlv, 'wamp.session.on_leave')
        yield self.register(self.mainapp.get_structure, str(self.mainapp.get_name()) + '.structure')

        for service in self.mainapp.services:
            yield self.register(self.mainapp.services[service].access, str(self.mainapp.get_name())+'.serv.'+str(service))


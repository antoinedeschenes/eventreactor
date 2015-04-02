# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import auth
from twisted.internet.defer import inlineCallbacks


class Session(ApplicationSession):
    #Nom d'usager pour la connexion
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
        self.mainapp = self.config.extra["mainapp"]

        "Choses à faire lorsqu'une connexion est réussie"
        yield self.subscribe(self.onjn, 'wamp.session.on_join')
        yield self.subscribe(self.onlv, 'wamp.session.on_leave')
        yield self.register(self.mainapp.getInfo(), str(details.session) + '.info')
        #yield self.subscribe()

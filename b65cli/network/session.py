# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import auth
from twisted.internet.defer import inlineCallbacks, returnValue


class Session(ApplicationSession):

    def __init__(self, config=None):
        super(Session, self).__init__(config)


    def onDisconnect(self):
        super(Session, self).onDisconnect()
        self.mainapp.net_session = None
        #print("sessionDisconnect")

    # Nom d'usager pour la connexion
    def onConnect(self):
        self.join(self.config.realm, [u"wampcra"], "provider")

    #Retourner le mot de passe encrypté
    def onChallenge(self, challenge):
        signature = auth.compute_wcs("secret".encode("utf8"), challenge.extra['challenge'].encode('utf8'))
        return signature.decode('ascii')

    #Connexion d'un autre usager
    def onjn(self, msg):
        #print(msg)
        #print(msg["authrole"])
        pass

    #Deconnexion d'un autre usager
    def onlv(self, msg):
        #print(msg)
        pass

    @inlineCallbacks
    def onJoin(self, details):

        self.mainapp = self.config.extra["mainapp"]
        self.mainapp.net_session = self

        "Choses à faire lorsqu'une connexion est réussie"
        #yield self.subscribe(self.onjn, 'wamp.session.on_join')
        #yield self.subscribe(self.onlv, 'wamp.session.on_leave')

        yield self.register_or_replace_rpc(str(self.mainapp.get_name()) + '.structure', self.mainapp.get_structure)
        yield self.register_or_replace_rpc(str(self.mainapp.get_name()) + '.configure', self.mainapp.configure)

        for service in self.mainapp.services:
            yield self.register_service(service)

        for event in self.mainapp.events:
            yield self.register_event(event)


    @inlineCallbacks
    def register_service(self, service):
        yield self.register_or_replace_rpc(str(self.mainapp.get_name()) + '.serv.' + str(service), self.mainapp.services[service].access)

    @inlineCallbacks
    def unregister_service(self, service):
        yield self.unregister_rpc(self.mainapp.get_name() + '.serv.' +service)

    @inlineCallbacks
    def register_event(self, event):
        yield self.register_or_replace_rpc(str(self.mainapp.get_name()) + '.evt.' + str(event), self.mainapp.events[event].access)

    @inlineCallbacks
    def unregister_event(self, event):
        yield self.unregister_rpc(self.mainapp.get_name() + '.evt.' + event)

    @inlineCallbacks
    def register_or_replace_rpc(self, procedure, func):
        "S'assure de désenregistrer un appel avant de l'enregistrer"
        yield self.unregister_rpc(procedure)
        try:
            yield self.register(func, procedure)
        except Exception as e:
            print e
            returnValue(False)
        returnValue(True)

    @inlineCallbacks
    def unregister_rpc(self, procedure):
        "Retire un enregistrement de procédure existant pour le réassigner éventuellement si reconfiguration"
        for i in self._registrations.keys():
            if self._registrations[i].procedure == procedure:
                try:
                    yield self._unregister(self._registrations[i])
                except Exception as e:
                    print e


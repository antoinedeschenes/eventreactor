# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

from autobahn.twisted.websocket import WampWebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory
from network.protocol import Protocol


class Factory(WampWebSocketClientFactory, ReconnectingClientFactory):
    "Factory qui produit des clients Twisted"

    # Modification de maxDelay de ReconnectingClientFactory
    # pour le délai maximum entre les tentatives de reconnexion.
    maxDelay = 15

    # Ma documentation
    #self.stopTrying() pour arreter d'essayer de connecter
    #self.continueTrying=1 pour reprendre les tentatives
    #self.delay le temps avant le prochain essai de connexion

    def __init__(self, factory, mainapp=None, *args, **kwargs):
        super(Factory, self).__init__(factory, *args, **kwargs)
        # Référence vers mainapp pour qu'elle soit au courant de l'état de la connexion.
        self.mainapp = mainapp
        self.debugCodePaths = True
        self.echoCloseCodeReason = True
        self.autoPingInterval = 10.0
        self.autoPingTimeout = 3.0
        self.protocol = Protocol

    # def startedConnecting(self, connector):
    #     "Appel sur tentative de connexion"
    #     # self.mainapp.connexionTentative()
    #     #print("factoryStartedConnecting")
    #     return ReconnectingClientFactory.startedConnecting(self, connector)
    #
    # def clientConnectionFailed(self, connector, reason):
    #     "Appel sur échec de tentative"
    #     #self.mainapp.connexion_echec()
    #     #print("factoryClientConnectionFailed")
    #     return ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
    #
    # def clientConnectionLost(self, connector, reason):
    #     "Appel lorsque la connexion est perdue"
    #     #self.mainapp.connexion_perdue()
    #     #print("factoryClientConnectionLost")
    #     return ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def buildProtocol(self, addr):
        "Appel lorsque la tentative réussit à se connecter"
        self.resetDelay()  # Remettre le délai entre les tentatives à zéro
        #self.mainapp.connexionReussie()
        #print("factoryBuildProtocol")
        return ReconnectingClientFactory.buildProtocol(self, addr)

# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

from autobahn.twisted.websocket import WampWebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory
from network.protocol import Protocol

# Classe Factory pour la session.
# Héritage multiple avec ReconnectingClientFactory pour permettre 
# une reconnexion si la session est coupée.
class Factory(WampWebSocketClientFactory, ReconnectingClientFactory):
    "Factory qui produit des clients Twisted"

    # Modification de maxDelay de ReconnectingClientFactory
    # pour le délai maximum entre les tentatives de reconnexion.
    # Sinon, le délai d'attente incrémentera continuellement.
    maxDelay = 15

    def __init__(self, factory, mainapp=None, *args, **kwargs):
        super(Factory, self).__init__(factory, *args, **kwargs)
        # mainapp est une référence à l'objet Provider pour le donner à la Session
        self.mainapp = mainapp
        #Paramètres redéfinis.
        self.debugCodePaths = True
        self.echoCloseCodeReason = True
        self.autoPingInterval = 10.0
        self.autoPingTimeout = 3.0
        self.protocol = Protocol # Utiliser le protocol custom.

    def buildProtocol(self, addr):
        "Appel lorsque la connexion est en négociation"
        self.resetDelay()  # Remettre le délai entre les tentatives à zéro
        return ReconnectingClientFactory.buildProtocol(self, addr)

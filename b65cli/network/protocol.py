# -*- coding: utf-8 -*-

from autobahn.twisted.websocket import WampWebSocketClientProtocol, WebSocketAdapterProtocol

import txaio

class Protocol(WampWebSocketClientProtocol):
    def onConnect(self, response):
        returnVal = super(Protocol, self).onConnect(response)

        #Fonction redéfinie pour utiliser l'autoping
        #Permet de reconnecter si la connexion a été coupée
        if self.autoPingInterval:
            self.autoPingPendingCall = txaio.call_later(self.autoPingInterval, self._sendAutoPing)

        return returnVal

    def _sendAutoPing(self):
        super(Protocol, self)._sendAutoPing()
        #print("sendAutoPing")

    def onAutoPingTimeout(self):
        super(Protocol, self).onAutoPingTimeout()
        #print("AutoPingTimeout")

    def dropConnection(self, abort=False):
        super(Protocol, self).dropConnection(abort)
        #print("protocolDropConnection")

    def connectionMade(self):
        WebSocketAdapterProtocol.connectionMade(self)
        #print("protocolConnectionMade")
        #print(self.autoPingInterval)

    def connectionLost(self, reason):
        WebSocketAdapterProtocol.connectionLost(self, reason)
        #print("protocolConnectionLost")




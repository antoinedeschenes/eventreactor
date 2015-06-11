# -*- coding: utf-8 -*-

from autobahn.twisted.websocket import WampWebSocketClientProtocol, WebSocketAdapterProtocol

import txaio

# Classe de protocol redéfinie pour active l'autoping

class Protocol(WampWebSocketClientProtocol):
    def onConnect(self, response):
        returnVal = super(Protocol, self).onConnect(response)

        # Fonction redéfinie pour utiliser l'autoping qui permet
        # de reconnecter si la connexion a été coupée "non-proprement"
        if self.autoPingInterval:
            self.autoPingPendingCall = txaio.call_later(self.autoPingInterval, self._sendAutoPing)

        return returnVal

    def connectionLost(self, reason):
        WebSocketAdapterProtocol.connectionLost(self, reason)
        print("Event Reactor: connection lost")




#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import sys

from autobahn.twisted import websocket
from autobahn.wamp.types import ComponentConfig
from twisted.internet import reactor
from twisted.python import log

from eventreactor.provider import Provider
from network.factory import Factory
from network.session import Session

if __name__ == '__main__':
    "Initialiser l'application"

    # Instance de l'objet qui gère les services
    provider = Provider()

    #Paramètres de base pour la connexion
    url = "ws://a.antoinedeschenes.com:8080/ws"
    realm = "realm1"

    # Donner un accès au gestionnaire de services à la session websocket
    extra = {'mainapp': provider}

    # Options de débogage
    debug = False
    debug_app = False
    debug_wamp = False
    if debug or debug_app or debug_wamp:
        log.startLogging(sys.stdout)

    #Boucle de rafraîchissement du logiciel
    reactor.callLater(1.0,provider.refresh_services)
    reactor.callLater(1.0,provider.refresh_events)

    #On doit fournir une factory de 'session' au service de websocket
    def factory():
        session = Session(ComponentConfig(realm, extra))
        session.debug_app = debug_app
        return session

    transport_factory = Factory(factory,
                                mainapp=provider,
                                url=url,
                                debug=debug,
                                debug_wamp=debug_wamp,
                                headers={"hostname": provider.get_name()})

    transport_factory.setProtocolOptions(autoPingInterval=10.0, autoPingTimeout=5.0)
    websocket.connectWS(transport_factory)

    #Démarrer la boucle d'événements
    reactor.run()

    print('Exit')

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from autobahn.wamp import protocol

__author__ = 'Antoine Deschênes'

import sys
from autobahn.twisted import websocket
from autobahn.wamp.types import ComponentConfig
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log
from eventreactor.provider import Provider
from network.factory import Factory
from network.session import Session


if __name__ == '__main__':
    "Initialiser l'application"



    #configuration de test
    config = {}

    #L'application entant que telle
    provider = Provider()



    url = "ws://a.antoinedeschenes.com:8080/ws"
    realm = "realm1"
    extra = {'mainapp':provider} # config a passer à la session

    debug = True
    debug_app = True
    debug_wamp = True
    if debug or debug_app or debug_wamp:
        log.startLogging(sys.stdout)


    #Boucle de rafraichissement logiciel
    boucle = LoopingCall(provider.refresh)
    boucle.start(0.5)


    def factory():
        session = Session(ComponentConfig(realm,extra))
        session.debug_app = debug_app
        return session

    transport_factory = Factory(factory,
                                mainapp=provider,
                                url=url,
                                debug=debug,
                                debug_wamp=debug_wamp,
                                headers={"hostname":os.uname()[1]})

    transport_factory.setProtocolOptions(autoPingInterval=10.0, autoPingTimeout=3.0)
    websocket.connectWS(transport_factory)

    reactor.run()


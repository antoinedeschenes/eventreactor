# -*- coding: utf-8 *-*
from autobahn.wamp.protocol import BaseSession
from twisted.internet import reactor

from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall

from autobahn.twisted.wamp import ApplicationSession

from CustomRunner import CustomRunner

import RPi.GPIO as GPIO


class Provider(ApplicationSession):
    def onChallenge(self, challenge):
        print("onChallenge")
        return ApplicationSession.onChallenge(self, challenge)

    def onMessage(self, msg):
        print("onMessage " + str(msg) )
        return ApplicationSession.onMessage(self, msg)

    def onOpen(self, transport):
        ApplicationSession.onOpen(self, transport)
        print("onOpen")

    def onDisconnect(self):
        BaseSession.onDisconnect(self)
        print("onDisconnect")

    def onLeave(self, details):
        ApplicationSession.onLeave(self, details)
        print("onLeave")

    def __init__(self, config=None):
        print("init")
        #self.tb=config.extra.thebahn
        self.chose = config.extra
        print(self.chose())
        self.statut = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        test = LoopingCall(self.scan)
        test.start(0.02)

        ApplicationSession.__init__(self, config)


    def onConnect(self):
        #self.tb += 1
        ApplicationSession.onConnect(self)
        print("onConnect")

    def onClose(self, wasClean):
        print("onClose"+ str(wasClean))
        ApplicationSession.onClose(self, wasClean)
        print("onClose2")
        GPIO.cleanup()

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.theval, 'com.test.test')
        yield self.register(self.doled, 'com.test.doled')
        print(self.chose())
        print("onJoin")

    def doled(self):
        GPIO.output(21, abs(GPIO.input(21) - 1))

    def scan(self):
        try:
            self.statut = GPIO.input(22)
        except:
            pass

    def theval(self):
        return self.statut


if __name__ == '__main__':
    jujube = 0
    def patante():
        global jujube
        return jujube

    def patanteLoop():
        global jujube
        jujube += 1
        print(jujube)

    #runner = CustomRunner("ws://antoinedeschenes.com:8080/ws", "realm1",debug=True, debug_app=True, debug_wamp=True)
    runner = CustomRunner("ws://localhost:8080/ws", "realm1",extra=patante)
    #runner = CustomRunner("ws://antoinedeschenes.com:8080/ws", "realm1",extra=patante)

    boucle = LoopingCall(patanteLoop)
    boucle.start(1)

    runner.run(Provider, start_reactor=False)


    reactor.run()

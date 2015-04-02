# -*- coding: utf-8 *-*

from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import RPi.GPIO as GPIO


class AppSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        self.statut = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        test = LoopingCall(self.scan)
        test.start(0.02)

        yield self.register(self.theval, 'com.test.test')

        yield self.register(self.doled, 'com.test.doled')

    def doled(self):
        GPIO.output(21, abs(GPIO.input(21) - 1))

    def scan(self):
        self.statut = GPIO.input(22)

    def theval(self):
        return self.statut


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://antoinedeschenes.com:8080/ws", "realm1")
    runner.run(AppSession)

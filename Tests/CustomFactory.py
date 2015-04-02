# coding=utf-8
from autobahn.twisted.websocket import WampWebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory


class CustomFactory(WampWebSocketClientFactory, ReconnectingClientFactory):
    maxDelay = 15

    #Appelé à chaque tentative
    def startedConnecting(self, connector):
        print 'Started to connect. ' + str(self.delay)
        return ReconnectingClientFactory.startedConnecting(self, connector)
 
    def clientConnectionFailed(self, connector, reason):
        #print "*************************************"
        print "Connection Failed"
        #print "reason:", reason
        #print "*************************************"
        #self.stopTrying()
        #print(str(self.continueTrying))
        #self.continueTrying=1
        return ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
 
    def clientConnectionLost(self, connector, reason):
        #print "*************************************"
        print "Connection Lost"
        #print "reason:", reason
        #print "*************************************"

        return ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    #Appelé lors d'une connexion valide
    def buildProtocol(self, addr):
        print("yoooBuildProtocol")
        self.resetDelay()

        return ReconnectingClientFactory.buildProtocol(self, addr)

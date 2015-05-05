# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks, returnValue

__author__ = 'Antoine Deschênes'

class Reaction(object):
    def __init__(self, provider, service, value):
        self.provider = provider
        self.service = service
        self.value = value
        pass

    @inlineCallbacks
    def execute(self):
        value = yield self.provider.helper.parsecondition(self.value)
        s = self.service.split('.')
        if s[0] == self.provider.name:
            self.provider.services[s[1]].access(s[2], value)
        elif self.provider.net_session:
            try:
                yield self.provider.net_session.call(s[0]+ '.serv.' +s[1], s[2], value)
            except:
                returnValue(False)
        else:
            returnValue(False)

        returnValue(True)
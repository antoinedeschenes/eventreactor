# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks, returnValue

__author__ = 'Antoine Deschênes'

class Reaction(object):
    def __init__(self, provider, service_attribute, value, execute = False):
        self.provider = provider
        self.service_attribute = service_attribute
        self.value = value
        if execute:
            self.execute()

    @inlineCallbacks
    def execute(self):
        value = yield self.provider.helper.parsecondition(self.value)
        s = self.service_attribute.split('.')
        if s[0] == self.provider.name:
            try:
                self.provider.services[s[1]].access(s[2], value)
            except Exception:
                returnValue(False)
        elif self.provider.net_session:
            try:
                yield self.provider.net_session.call(s[0]+ '.serv.' +s[1], s[2], value)
            except:
                returnValue(False)
        else:
            returnValue(False)
        returnValue(True)
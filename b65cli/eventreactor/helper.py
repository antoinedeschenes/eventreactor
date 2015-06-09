# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks, returnValue


class Helper(object):
    def __init__(self, provider):
        self.provider = provider

    @inlineCallbacks
    def parsecondition(self, condition):
        services = []
        toreplace = str(condition).split("[")
        for part in toreplace:
            if part.find(']') != -1:
                services.append(part.split(']')[0])

        for serv in services:
            s = serv.split('.')
            oldvalue = "[" + str(serv) + "]"
            newvalue = None
            if s[0] == self.provider.name:
                try:
                    newvalue = self.provider.services[s[1]].access(s[2])
                except Exception:
                    pass
            elif self.provider.net_session:
                try:
                    newvalue = yield self.provider.net_session.call(s[0]+ '.serv.' +s[1], s[2])
                except Exception:
                    pass

            condition = condition.replace(oldvalue, str(newvalue))

        condition = "(" + str(condition) + ")"
        try:
            retour = eval(condition, {"__builtins__": None}, {"abs": abs, "round": round, "min":min, "max":max})
        except:
            retour = None

        returnValue(retour)
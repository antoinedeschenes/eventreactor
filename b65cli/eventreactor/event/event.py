# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks

__author__ = 'Antoine Deschênes'

from eventreactor.reaction import Reaction


class Event(object):
    def __init__(self, provider, config):
        self.provider = provider
        self.description = None
        #self.condition = '[raspberrypi21.monThermometre.temp] > 25'
        self.condition = config["condition"]
        self.last_state = None

        self.onTrue = []
        for reaction in config["onTrue"]:
            self.onTrue.append(Reaction(provider, reaction, config["onTrue"][reaction]))

        self.onFalse = []
        for reaction in config["onFalse"]:
            self.onFalse.append(Reaction(provider, reaction, config["onFalse"][reaction]))

        #self.onTrue = Reaction(provider, 'raspberrypi21.out21.state', 1)
        #self.onFalse = Reaction(provider, 'raspberrypi21.out21.state', 0)


    @inlineCallbacks
    def refresh(self):
        new_state = yield self.provider.helper.parsecondition(self.condition)
        #print(self.last_state, new_state)
        if (self.last_state is None and new_state is not None) or self.last_state != new_state:
            if new_state is True:
                for reaction in self.onTrue:
                    reaction.execute()
            else:
                for reaction in self.onFalse:
                    reaction.execute()

            self.last_state = new_state


    def access(self):
        return self.condition

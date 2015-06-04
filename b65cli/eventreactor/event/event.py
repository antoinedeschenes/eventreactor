# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks

__author__ = 'Antoine Deschênes'

from eventreactor.event.reaction import Reaction


class Event(object):
    def __init__(self, provider, config):
        self.provider = provider
        self.last_state = None
        self.config = {
            "condition":None,
            "onTrue":[],
            "onFalse":[]
        }
        self.onTrue = []
        self.onFalse = []
        self.configure(config)


    def configure(self, config):
        self.config = config
        self.onTrue = []
        for reaction in config["onTrue"]:
            self.onTrue.append(Reaction(self.provider, reaction, config["onTrue"][reaction]))

        self.onFalse = []
        for reaction in config["onFalse"]:
            self.onFalse.append(Reaction(self.provider, reaction, config["onFalse"][reaction]))

    @inlineCallbacks
    def refresh(self):
        new_state = yield self.provider.helper.parsecondition(self.config["condition"])

        if (self.last_state is None and new_state is not None) or self.last_state != new_state:
            if new_state is True:
                for reaction in self.onTrue:
                    try:
                        reaction.execute()
                    except Exception as e:
                        print(e.message)
            else:
                for reaction in self.onFalse:
                    try:
                        reaction.execute()
                    except Exception as e:
                        print(e.message)

            self.last_state = new_state

    def access(self):
        return self.config

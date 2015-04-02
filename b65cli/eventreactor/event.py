# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

from eventreactor.reaction import Reaction


class Event(object):
    def __init__(self):
        self.description = None
        self.condition = None
        self.lastState = None
        self.onTrue = Reaction()
        self.onFalse = Reaction()

    def refresh(self):
        newState = eval(self.condition)
        if self.lastState is None or self.lastState != newState:
            if newState:
                self.onTrue.execute()
            else:
                self.onFalse.execute()
        self.lastState = newState

# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'


class Service(object):
    TYPE_GPIO = 1
    TYPE_TEMPERATURE = 2
    TYPE_THERMOELECTRIC = 3

    def __init__(self, config):
        self.readables = dict()
        self.writables = dict()
        self.config = config

    def access(self, attribute=None, value=None):
        if attribute is None:
            return { 'values':self.readables, 'config':self.config}
        elif value is None:
            return self.readables[attribute]
        else:
            self.writables[attribute]=value
            return

    def refresh(self):
        pass




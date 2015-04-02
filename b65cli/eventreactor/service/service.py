# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

class Service(object):

    TYPE_GPIO = 1
    TYPE_TEMPERATURE = 2
    TYPE_THERMOPLATE = 3

    def __init__(self):
        self.readables = dict()
        self.writables = dict()
        self.config = dict()

    def refresh(self):
        pass
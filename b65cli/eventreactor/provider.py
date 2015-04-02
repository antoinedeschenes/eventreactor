# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import os
from eventreactor.service.temperature import Temperature

class Provider(object):
    def __init__(self):
        self.name = os.uname()[1]
        self.services = dict()
        self.events = dict()

        self.services["monThermometre"] = Temperature()
        print("EventReactor initialized")

    #Placeholders
    def connexionEchec(self):
        print("Failed connection attempt")


    def connexionPerdue(self):
        print("Lost connection")

    def connexionReussie(self):
        print("connect successful")

    def connexionTentative(self):
        print("attempt")

    def getInfo(self):
        return {"name":self.name}

    def getAvailableServices(self):
        return self.services.keys()

    def refresh(self):
        for service in self.services:
            self.services[service].refresh()
        for event in self.events:
            self.events[event].refresh()


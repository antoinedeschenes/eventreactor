# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

__author__ = 'Antoine Deschênes'

import os
import json

from eventreactor.service.service import Service
from eventreactor.event.event import Event
from eventreactor.helper import Helper

class Provider(object):
    def __init__(self):
        try:
            self.name = os.uname()[1]
        except Exception:
            self.name = os.getenv('COMPUTERNAME')
        self.helper = Helper(self)
        self.services = dict()
        self.events = dict()
        self.net_session = None

        self.initConf = {}
        with open(self.name + '.conf', 'r') as configfile:
            self.initConf = json.loads(configfile.read())

        #with open('raspberrypi21.conf', 'w') as f:
        #    f.write(json.dumps(self.initConf, sort_keys=True, indent=4, separators=(',', ': ')))

        for service in self.initConf["services"].keys():
            self.addService(service,self.initConf["services"][service])

        for event in self.initConf["events"].keys():
            self.addEvent(event, self.initConf["events"][event])

        #print("EventReactor provider init")

    def addEvent(self, name, config):
        self.events[name] = Event(self, config)

    def addService(self, name, config):
        #Ajouter le service approprié et importer seulement quand nécessaire.
        #Python ne s'occupe pas des importations dupliquées.
        type = config["type"]
        if type == Service.TYPE_GPIO:
            from eventreactor.service.gpio import GPIO
            self.services[name] = GPIO(config)
        elif type == Service.TYPE_TEMPERATURE:
            from eventreactor.service.temperature import Temperature
            self.services[name] = Temperature(config)
        elif type == Service.TYPE_THERMOELECTRIC:
            from eventreactor.service.thermoelectric import Thermoelectric
            self.services[name] = Thermoelectric(config)
        elif type == Service.TYPE_TIMECLOCK:
            from eventreactor.service.timeclock import Timeclock
            self.services[name] = Timeclock(config)
            
    def delService(self, name):
        self.net_session.unregister(self.name + '.serv.' + name)
        del self.services[name]
        pass

    def get_name(self):
        return self.name

    def get_structure(self):
        return {"services":self.services.keys(),
                "events":self.events.keys()}

    def refresh(self):
        #Rafraîchissement des services
        for service in self.services:
            try:
                self.services[service].refresh()
            except Exception as e:
                print(e.message)

        for event in self.events:
            try:
                self.events[event].refresh()
            except Exception as e:
                print(e.message)

        reactor.callLater(0.15, self.refresh)


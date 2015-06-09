# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks

__author__ = 'Antoine Deschênes'

import os
import dao.config
from twisted.internet import reactor


from eventreactor.service.service import Service
from eventreactor.event.event import Event
from eventreactor.helper import Helper


class Provider(object):
    def __init__(self):
        try: #Linux
            self.name = os.uname()[1]
        except Exception: #Windows
            self.name = os.getenv('COMPUTERNAME')

        self.helper = Helper(self)
        self.services = dict()
        self.events = dict()
        self.net_session = None

        self.providerConf = dao.config.read_config(self.name)

        for service in self.providerConf["services"].keys():
            self.load_service(service, self.providerConf["services"][service])

        for event in self.providerConf["events"].keys():
            self.load_event(event, self.providerConf["events"][event])

    @inlineCallbacks
    def configure(self, config):
        "Appelé à distance pour ajouter, modifier ou retirer un service ou événement"
        if 'services' in config.keys():
            services = config['services']
            for s in services.keys():
                if services[s] is None: # Service null à effacer
                    del self.providerConf['services'][s]
                    yield self.unload_service(s)
                elif s in self.providerConf['services'].keys(): # Service existant à remplacer
                    self.providerConf['services'][s] = services[s]
                    yield self.unload_service(s)
                    self.load_service(s, self.providerConf['services'][s])
                    yield self.net_session.register_service(s)
                else: # Service nouveau à ajouter
                    self.providerConf['services'][s] = services[s]
                    self.load_service(s, self.providerConf['services'][s])
                    yield self.net_session.register_service(s)

        if 'events' in config.keys():
            events = config['events']
            for e in events.keys():
                if events[e] is None:  # null à effacer
                    del self.providerConf['events'][e]
                    self.unload_event(e)
                elif e in self.providerConf['events'].keys():  # existant à remplacer
                    self.providerConf['events'][e] = self.events[e].configure(events[e])
                else:  # Nouvel événement
                    self.providerConf['events'][e] = events[e]
                    self.load_event(e, self.providerConf['events'][e])
                    yield self.net_session.register_event(e)

        dao.config.write_config(self.name, self.providerConf)

    def load_event(self, name, config):
        # Ajouter un événement
        self.events[name] = Event(self, config)

    @inlineCallbacks
    def unload_event(self, name):
        if self.net_session is not None:
            try:
                yield self.net_session.unregister_event(name)
            except Exception:
                pass
        del self.events[name]


    def load_service(self, name, config):
        # Ajouter le service approprié et importer seulement quand nécessaire.
        # Python ne s'occupe pas des importations dupliquées.
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

        elif type == Service.TYPE_VARIABLE:
            from eventreactor.service.variable import Variable
            self.services[name] = Variable(config)

    @inlineCallbacks
    def unload_service(self, name):
        if self.net_session is not None:
            try:
                yield self.net_session.unregister_service(name)
            except Exception:
                pass
        self.services[name].cleanup()
        del self.services[name]

    def get_name(self):
        return self.name

    def get_structure(self):
        return {"services": self.services.keys(),
                "events": self.events.keys()}

    def refresh_services(self):
        # Rafraîchissement des services
        for service in self.services:
            try:
                self.services[service].refresh()
            except Exception as e:
                print(e.message)

        reactor.callLater(0.15, self.refresh_services)

    def refresh_events(self):
        #Rafraîchissement des événements
        for event in self.events:
            try:
                self.events[event].refresh()
            except Exception as e:
                print(e.message)

        reactor.callLater(0.1, self.refresh_events)


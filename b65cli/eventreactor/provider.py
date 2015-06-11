# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks

__author__ = 'Antoine Deschênes'

import os
import dao.config
from twisted.internet import reactor


from eventreactor.service.service import Service
from eventreactor.event.event import Event
from eventreactor.helper import Helper

# Gestion des événements et services
class Provider(object):
    def __init__(self):
        #Nom de machine
        try: #Linux
            self.name = os.uname()[1]
        except Exception: #Windows
            self.name = os.getenv('COMPUTERNAME')

        self.helper = Helper(self) #Créer un helper
        self.services = dict()
        self.events = dict()
        self.net_session = None

        #Lire la config
        self.providerConf = dao.config.read_config(self.name)

        # Charger tous les services et événements.
        # Ce constructeur est appelé avant le démarrage du "reactor", donc le réesau n'est pas encore connecté.
        for service in self.providerConf["services"].keys():
            self.load_service(service, self.providerConf["services"][service])

        for event in self.providerConf["events"].keys():
            self.load_event(event, self.providerConf["events"][event])

    @inlineCallbacks
    def configure(self, config):
        "Appelé à distance pour ajouter, modifier ou retirer un service ou événement"
        if 'services' in config.keys(): #Si la clé services est présente
            services = config['services']
            for s in services.keys(): # Pour tous les objets trouvés sous la clé services
                if services[s] is None: # Service dont la valeur est None à effacer
                    del self.providerConf['services'][s]
                    yield self.unload_service(s)
                elif s in self.providerConf['services'].keys(): # Service existant à remplacer
                    self.providerConf['services'][s] = services[s] # Mettre en config
                    yield self.unload_service(s) # Décharger l'ancien
                    self.load_service(s, self.providerConf['services'][s]) # Charger le nouveau
                    yield self.net_session.register_service(s) # Enregistrer sur le réseau
                else: # Service nouveau à ajouter
                    self.providerConf['services'][s] = services[s] # MÀJ config
                    self.load_service(s, self.providerConf['services'][s]) # Charger
                    yield self.net_session.register_service(s) # Enregistrer sur le réseau

        if 'events' in config.keys(): #Si la clé events est présente
            events = config['events']
            for e in events.keys(): # Pour tous les objets trouvés sous la clé events
                if events[e] is None:  # Événement dont la valeur est None à effacer
                    del self.providerConf['events'][e]
                    self.unload_event(e)
                elif e in self.providerConf['events'].keys():  # Existant à reconfigurer. La classe Event se gère elle-même
                    self.providerConf['events'][e] = self.events[e].configure(events[e])
                else:  # Nouvel événement
                    self.providerConf['events'][e] = events[e] # MÀJ config
                    self.load_event(e, self.providerConf['events'][e]) # Charger
                    yield self.net_session.register_event(e) # Enregistrer

        dao.config.write_config(self.name, self.providerConf) # Écrire la config quand réussi.

    def load_event(self, name, config):
        "Charger un événement"
        self.events[name] = Event(self, config)

    @inlineCallbacks
    def unload_event(self, name):
        "Décharger et désenregistrer un événement"
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
        "Décharger et désenregistrer un service"
        if self.net_session is not None:
            try:
                yield self.net_session.unregister_service(name)
            except Exception:
                pass
        self.services[name].cleanup()
        del self.services[name]

    def get_name(self):
        "Renvoie le nom de machine"
        return self.name

    def get_structure(self):
        "Renvoie la structure d'événements et services"
        return {"services": self.services.keys(),
                "events": self.events.keys()}

    def refresh_services(self):
        "Rafraîchissement des services"
        for service in self.services:
            try:
                self.services[service].refresh()
            except Exception as e:
                print(e.message)

        #Planifier un nouvel appel lorsque tout est terminé
        reactor.callLater(0.15, self.refresh_services)

    def refresh_events(self):
        "Rafraîchissement des événements"
        for event in self.events:
            try:
                self.events[event].refresh()
            except Exception as e:
                print(e.message)

        # Planifier un nouvel appel lorsque tout est terminé
        reactor.callLater(0.1, self.refresh_events)


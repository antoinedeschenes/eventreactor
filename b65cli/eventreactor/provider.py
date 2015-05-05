# -*- coding: utf-8 -*-

__author__ = 'Antoine Deschênes'

import os

from eventreactor.service.gpio import GPIO
from eventreactor.service.service import Service
from eventreactor.service.temperature import Temperature
from eventreactor.event.event import Event
from eventreactor.helper import Helper


class Provider(object):
    def __init__(self):
        self.name = os.uname()[1]
        self.helper = Helper(self)
        self.services = dict()
        self.events = dict()
        self.net_session = None

        self.initConf = \
            {
                "events":{
                    "tempcheck":{
                        "condition":"[raspberrypi21.monThermometre.temp] > 25",
                        "onTrue":{"raspberrypi21.out21.state":1},
                        "onFalse":{"raspberrypi21.out21.state":0}
                    }
                },
                "services":{
                    "monThermometre":{"type":Service.TYPE_TEMPERATURE,
                                      "sensorType":Temperature.SENSOR_MCP9808},
                    "in23":{"type":Service.TYPE_GPIO,
                            "mode":GPIO.GPIO_INPUT,
                            "pin":23},
                    "out21":{"type":Service.TYPE_GPIO,
                             "mode":GPIO.GPIO_OUTPUT,
                             "pin":21}
                }
            }


        for service in self.initConf["services"].keys():
            self.addService(service,self.initConf["services"][service])

        for event in self.initConf["events"].keys():
            self.addEvent(event, self.initConf["events"][event])

        #self.services["monThermometre"] = Temperature()
        #self.services["in23"] = GPIO(23, GPIO.GPIO_INPUT)
        #self.services["out21"] = GPIO(21, GPIO.GPIO_OUTPUT)

        #self.events["tempcheck"]= Event(self)
        print("EventReactor provider init")

    def addEvent(self, name, config):
        self.events[name] = Event(self, config)

    def addService(self, name, config):
        type = config["type"]
        if type == Service.TYPE_GPIO:
            self.services[name] = GPIO(config)
        elif type == Service.TYPE_TEMPERATURE:
            self.services[name] = Temperature(config)

    def delService(self, name):
        self.net_session.unregister(self.name + '.serv.' + name)
        del self.services[name]
        pass


    # Placeholders
    def connexion_echec(self):
        print("Failed connection attempt")
    def connexion_perdue(self):
        print("Lost connection")
    def connexionReussie(self):
        print("connect successful")
    def connexionTentative(self):
        print("attempt")


    def get_name(self):
        return self.name

    def get_structure(self):
        return {"services":self.services.keys(),
                "events":self.events.keys()}

    def refresh(self):
        for service in self.services:
            self.services[service].refresh()
        for event in self.events:
            self.events[event].refresh()


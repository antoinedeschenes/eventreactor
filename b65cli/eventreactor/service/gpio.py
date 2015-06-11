# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import dao.gpio
from .service import Service

#Service d'accès aux pins d'entrée sortie
class GPIO(Service):
    GPIO_INPUT = dao.gpio.GPIO_INPUT
    GPIO_OUTPUT = dao.gpio.GPIO_OUTPUT

    def __init__(self, config):
        super(GPIO, self).__init__(config)
        #Initialiser les clés de 'dictionnaires'
        self.readables["state"] = None
        self.writables["state"] = None
        #Configurer le DAO de GPIO en mode entrée ou sortie pour la pin.
        dao.gpio.setup(self.config["pin"], self.config["mode"])

    def refresh(self):
        #Rafraichir la valeur lue et appliquer celle qui aurait été écrite par un événement
        self.readables["state"] = dao.gpio.pin(self.config["pin"], self.writables["state"])
        self.writables["state"] = None

    def cleanup(self):
        #Libérer la GPIO quand on enlève le service.
        dao.gpio.setup(self.config["pin"])


# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import dao.smbus
from .service import Service

#Accès à une température lue par un thermomètre
class Temperature(Service):
    SENSOR_MCP9808 = dao.smbus.SENSOR_MCP9808
    SENSOR_TMP007 = dao.smbus.SENSOR_TMP007

    def __init__(self, config):
        super(Temperature, self).__init__(config)
        # Initialiser les clés spécifiques au service.
        self.readables["temp"] = None

    def refresh(self):
        # Si le thermomètre ne répond pas, garder l'ancienne valeur.
        # --Les thermomètres "gèlent" parfois.

        try:
            reading = round(dao.smbus.lire(self.config['sensorType'], self.config['address']),3)
            if reading is not None:
                self.readables["temp"] = reading
        except Exception:
            pass

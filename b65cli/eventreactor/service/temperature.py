# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import dao.smbus
from .service import Service

class Temperature(Service):
    SENSOR_MCP9808 = dao.smbus.SENSOR_MCP9808
    SENSOR_TMP007 = dao.smbus.SENSOR_TMP007

    def __init__(self, config):
        super(Temperature, self).__init__(config)
        self.readables["temp"] = None

    def refresh(self):
        self.readables["temp"] = round(dao.smbus.lire(self.config['sensorType'], self.config['address']),2)

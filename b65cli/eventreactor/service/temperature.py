# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import dao.smbus
from .service import Service

class Temperature(Service):

    SENSOR_MCP9808 = 0
    SENSOR_TMP007 = 1

    def __init__(self):
        super(Temperature, self).__init__()
        self.config["type"]=Service.TYPE_TEMPERATURE
        self.readables["temp"] = None
        self.config["sensorType"]=Temperature.SENSOR_MCP9808

    def refresh(self):
        self.readables["temp"] = dao.smbus.lire("dummy",0x18)


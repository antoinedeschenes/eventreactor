# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import dao.powersupply
from .service import Service

class Thermoelectric(Service):
    MAX_VOLT = 13.5
    MAX_CURRENT = 8.5
    MAX_POWER = MAX_VOLT * MAX_CURRENT

    def __init__(self, config):
        self.counter = 0
        super(Thermoelectric, self).__init__(config)
        self.config['max_current'] = Thermoelectric.MAX_CURRENT
        self.config['max_voltage'] = Thermoelectric.MAX_VOLT
        self.readables['duty'] = None
        self.writables['duty'] = None
        dao.powersupply.set_clamp(Thermoelectric.MAX_VOLT, Thermoelectric.MAX_CURRENT)

    def refresh(self):
        # Rafraichissement moins fréquents que les autres services pour ne pas surcharger le PSU
        self.counter = (self.counter + 1) % 1
        if self.counter == 0:
            psustatus = dao.powersupply.get_status()
            if psustatus is not None:
                self.readables.update(psustatus)

            if self.writables['duty'] is not None:
                self.readables['duty'] = self.writables['duty']
                self.writables['duty'] = None
                dao.powersupply.on()

            if self.readables['duty'] is None:
                dao.powersupply.off()
            else:
                targetpower = abs((float(Thermoelectric.MAX_POWER) * float(self.readables['duty'])) / 100.0)
                currentpower = self.readables['power']
                coolheat = int(self.readables['duty'] >= 0)  # 0:cool, 1:heat

                if currentpower > targetpower:
                    targetvoltage = self.readables['voltage'] - 0.2
                    if self.readables['cvcc'] and targetvoltage >= 3.3:
                        # Réduire voltage, 3.3V est le minimum pour le ventilateur
                        dao.powersupply.set_voltage(targetvoltage)
                    else: #Réduire courant
                        dao.powersupply.set_current(self.readables['current'] - 0.2)
                elif currentpower < targetpower:
                    targetvoltage = self.readables['voltage'] + 0.3
                    if targetvoltage < 3.3:
                        targetvoltage = 3.3
                    if self.readables['cvcc']:
                        # Augmenter courant
                        dao.powersupply.set_current(self.readables['current'] + 0.15)
                    else:
                        # Augmenter voltage
                        dao.powersupply.set_voltage(targetvoltage)

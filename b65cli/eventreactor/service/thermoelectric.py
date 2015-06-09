# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import dao.powersupply
import dao.gpio
from .service import Service

class Thermoelectric(Service):
    MAX_VOLT = 14.0
    MAX_CURRENT = 8.5
    MAX_POWER = MAX_VOLT * MAX_CURRENT

    def __init__(self, config):
        self.counter = 0
        super(Thermoelectric, self).__init__(config)
        self.config['max_current'] = Thermoelectric.MAX_CURRENT
        self.config['max_voltage'] = Thermoelectric.MAX_VOLT
        self.readables['duty'] = None
        self.readables['coolheat'] = None
        self.writables['duty'] = None
        dao.powersupply.set_clamp(Thermoelectric.MAX_VOLT, Thermoelectric.MAX_CURRENT)
        dao.gpio.setup(4, 'O') # Relais d'inversion.

    def refresh(self):
        # Rafraichissement moins fréquents que les autres services pour ne pas surcharger le PSU
        self.counter = (self.counter + 1) % 1
        if self.counter == 0:
            psustatus = dao.powersupply.get_status()
            self.readables['coolheat'] = dao.gpio.pin(4)

            if psustatus is not None:
                self.readables.update(psustatus)

            if self.writables['duty'] is not None:
                new_duty = self.writables['duty']
                if new_duty > 100:
                    new_duty = 100
                if new_duty < -100:
                    new_duty = -100
                self.readables['duty'] = new_duty
                self.writables['duty'] = None
                dao.powersupply.on()

            if self.readables['duty'] is None:
                dao.powersupply.off()
            else:
                targetpower = abs((float(Thermoelectric.MAX_POWER) * float(self.readables['duty'])) / 100.0)
                currentpower = self.readables['power']
                coolheat_wanted = int(self.readables['duty'] > 0)  # 0:cool, 1:heat
                coolheat_current = dao.gpio.pin(4)


                #Contrôle du relais
                if coolheat_wanted != coolheat_current:
                    if currentpower > 2: #Threshold pour changer de direction
                        targetpower = 0 #Forcer une descente
                    else: #Faire le changement de polarité
                        dao.powersupply.off()
                        dao.gpio.pin(4, coolheat_wanted)
                        dao.powersupply.on()

                if (currentpower - targetpower) > 5 :
                    targetvoltage = self.readables['voltage'] - 0.2
                    if self.readables['cvcc'] and targetvoltage >= 3.3:
                        # Réduire voltage, 3.3V est le minimum pour le ventilateur
                        dao.powersupply.set_voltage(targetvoltage)
                    else: #Réduire courant
                        dao.powersupply.set_current(self.readables['current'] - 0.2)
                elif (currentpower - targetpower) < 5 :
                    targetvoltage = self.readables['voltage'] + 0.3
                    if targetvoltage < 3.3:
                        targetvoltage = 3.3
                    if self.readables['cvcc']:
                        # Augmenter courant
                        dao.powersupply.set_current(self.readables['current'] + 0.2)
                    else:
                        # Augmenter voltage
                        dao.powersupply.set_voltage(targetvoltage)
                elif targetpower == 0:
                    dao.powersupply.off()

    def cleanup(self):
        dao.powersupply.off()
        dao.gpio.setup(4)

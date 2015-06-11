# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import dao.powersupply
import dao.gpio
from .service import Service

#Contrôle d'une plaque thermoélectrique
class Thermoelectric(Service):
    # Valeurs forcées pour empêcher un utilisateur de briser le TEC.
    MAX_VOLT = 14.0
    MAX_CURRENT = 8.5
    MAX_POWER = MAX_VOLT * MAX_CURRENT

    def __init__(self, config):
        super(Thermoelectric, self).__init__(config)
        #Initialiser la config et les clés de dictionnaire possibles
        self.config['max_current'] = Thermoelectric.MAX_CURRENT
        self.config['max_voltage'] = Thermoelectric.MAX_VOLT
        self.readables['duty'] = None
        self.readables['coolheat'] = None
        self.readables['voltage'] = None
        self.readables['current'] = None
        self.readables['power'] = None
        self.writables['duty'] = None
        #Appliquer les limites au PSU
        dao.powersupply.set_clamp(Thermoelectric.MAX_VOLT, Thermoelectric.MAX_CURRENT)
        dao.gpio.setup(4, 'O') # Relais d'inversion.

    def refresh(self):

        psustatus = dao.powersupply.get_status() # Aller chercher mesure voltage et courant
        self.readables['coolheat'] = dao.gpio.pin(4)

        if psustatus is not None: # Si le powersupply a répondu, mettre à jour
            self.readables.update(psustatus)

        if self.writables['duty'] is not None: # Une valeur a été envoyée par une réaction d'événement
            new_duty = self.writables['duty']
            if new_duty > 100: # Clamper la valeur à +/-100
                new_duty = 100
            if new_duty < -100:
                new_duty = -100
            self.readables['duty'] = new_duty
            self.writables['duty'] = None
            dao.powersupply.on()

        if self.readables['duty'] is None: # Duty jamais paramétré. Ne rien faire.
            dao.powersupply.off()
        else:
            # Recalculer la tension et courant visée selon les nouvelles données.

            # Pourcentage du maximum que la plaque thermo peut prendre.
            targetpower = abs((float(Thermoelectric.MAX_POWER) * float(self.readables['duty'])) / 100.0)
            currentpower = self.readables['power'] # Puissance courante
            coolheat_wanted = int(self.readables['duty'] > 0)  # 0:cool, 1:heat
            coolheat_current = dao.gpio.pin(4) # État actuel du relais.

            #Contrôle du relais
            if coolheat_wanted != coolheat_current: # Si on est pas dans le bon mode
                if currentpower > 2: #Threshold pour changer de direction
                    targetpower = 0 #Forcer une descente
                else: #Renverser les pôles quand la puissance est assez basse pour ne pas endommager relais et TEC.
                    dao.powersupply.off()
                    dao.gpio.pin(4, coolheat_wanted)
                    dao.powersupply.on()

            if (currentpower - targetpower) > 5 :
                #Si on doit baisser la puissance de sortie (on se garde 5W de marge)
                targetvoltage = self.readables['voltage'] - 0.2
                if self.readables['cvcc'] and targetvoltage >= 3.3:
                    # Réduire voltage, 3.3V est le minimum pour le ventilateur
                    dao.powersupply.set_voltage(targetvoltage)
                else: #Réduire courant
                    dao.powersupply.set_current(self.readables['current'] - 0.2)
            elif (currentpower - targetpower) < 5 :
                #Si on doit augmenter la puissance de sortie
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
                # Si jamais moins de 5W et qu'on a demandé aucune sortie
                dao.powersupply.off()

    def cleanup(self):
        "À la suppression du service, fermer le powersupply et libérer la GPIO du relais."
        dao.powersupply.off()
        dao.gpio.setup(4)

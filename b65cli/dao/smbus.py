# -*- coding: utf-8 -*-
from __future__ import absolute_import

__author__ = 'Antoine Deschênes'

import smbus as __smbuslib
import atexit as __atexit

# Instancier une connexion au bus I2C à l'importation du module.
__smbus = __smbuslib.SMBus(1)

# Fermer le bus à la fermeture
__atexit.register(__smbus.close)

SENSOR_MCP9808 = 0
SENSOR_TMP007 = 1


def lire(sensor_type, adresse):
    #Datasheet MCP9808 section 5.1.3.1
    if sensor_type == SENSOR_MCP9808:
        t = __smbus.read_i2c_block_data(adresse, 0x05)
        t = ((t[0] << 8) + t[1]) & 0x1FFF
        t -= t & 0x1000
        return t / 16.0
    elif sensor_type == SENSOR_TMP007:
        t = __smbus.read_i2c_block_data(adresse, 0x03)
        t = ((t[0] << 8) + t[1])
        if t & 0x8000: # Température négative
            t -= 0x10000

        if t & 0x0001:  # Bit d'erreur, cette valeur ne compte pas
            return None
        else:
            # 14 premiers bits contiennent la température en 32e de degrés
            return (t >> 2) / 32.0

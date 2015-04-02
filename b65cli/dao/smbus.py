# -*- coding: utf-8 -*-
from __future__ import absolute_import
__author__ = 'Antoine Deschênes'

import smbus as __smbuslib
import atexit as __atexit

#Instancier une connexion au bus I2C à l'importation du module.
__smbus = __smbuslib.SMBus(1)

#Fermer le bus à la fermeture
__atexit.register(__smbus.close)

MCP9080 = 0
TMP007_ = 1


print("dao.smbus loaded")

def lire(type, adresse):
    #Voir datasheet MCP9808 5.1.3.1
    t = __smbus.read_i2c_block_data(adresse, 0x05)
    t = ((t[0] << 8) + t[1]) & 0x1FFF
    t -= t & 0x1000
    return t / 16.0

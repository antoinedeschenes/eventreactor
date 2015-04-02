# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import RPi.GPIO as __gpiolib
import atexit as __atexit


#Ouvrir le GPIO à l'importation - module singleton
__gpiolib.setmode(__gpiolib.BCM)

#Libérer les GPIO à la fermeture
__atexit.register(__gpiolib.cleanup)

print("dao.gpio loaded")

def setupPin(numero, mode=None):
    if mode == 'I':
        __gpiolib.setup(numero, __gpiolib.IN, pull_up_down=__gpiolib.PUD_DOWN)
    elif mode == 'O':
        __gpiolib.setup(numero, __gpiolib.OUT, initial=__gpiolib.LOW)
    else:
        __gpiolib.cleanup(numero)

def accesPin(numero, etat=None):
    if etat is not None:
        __gpiolib.output(numero, etat)
    return __gpiolib.input(numero)
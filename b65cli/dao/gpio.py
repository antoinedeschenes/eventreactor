# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import atexit as __atexit
import RPi.GPIO as __gpiolib
#import eventreactor.service.gpio as __gpioservice

# Ouvrir le GPIO à l'importation - module singleton
__gpiolib.setmode(__gpiolib.BCM)

# Libérer les GPIO à la fermeture
__atexit.register(__gpiolib.cleanup)

print("dao.gpio loaded")

GPIO_INPUT = 'I'
GPIO_OUTPUT = 'O'


def setup(numero, mode=None):
    if mode == GPIO_INPUT:
        __gpiolib.setup(numero, __gpiolib.IN, pull_up_down=__gpiolib.PUD_DOWN)
    elif mode == GPIO_OUTPUT:
        __gpiolib.setup(numero, __gpiolib.OUT, initial=__gpiolib.LOW)
    else:
        __gpiolib.cleanup(numero)


def pin(numero, state=None):
    if (state is not None) and __gpiolib.gpio_function(numero) == __gpiolib.OUT:
        __gpiolib.output(numero, state)


    current_state = __gpiolib.input(numero)

    return current_state
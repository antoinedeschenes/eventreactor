# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import atexit as __atexit
import RPi.GPIO as __gpiolib

# Ouvrir le GPIO à l'importation - module à la 'singleton'
__gpiolib.setmode(__gpiolib.BCM)

# Libérer les GPIO à la fermeture
__atexit.register(__gpiolib.cleanup)

GPIO_INPUT = 'I'
GPIO_OUTPUT = 'O'

def setup(numero, mode=None):
    # Mettre en mode input, mode output ou libérer la GPIO.
    if mode == GPIO_INPUT:
        __gpiolib.setup(numero, __gpiolib.IN, pull_up_down=__gpiolib.PUD_DOWN)
    elif mode == GPIO_OUTPUT:
        __gpiolib.setup(numero, __gpiolib.OUT, initial=__gpiolib.LOW)
    else:
        __gpiolib.cleanup(numero)


def pin(numero, state=None):
    # Lecture, et optionnellement écriture si 'state' n'est pas vide et la pin est en OUTPUT.
    if (state is not None) and __gpiolib.gpio_function(numero) == __gpiolib.OUT:
        __gpiolib.output(numero, state)

    return __gpiolib.input(numero)
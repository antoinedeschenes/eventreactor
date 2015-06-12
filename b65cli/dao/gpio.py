# -*- coding: utf-8 -*-
import time

__author__ = 'Antoine Deschênes'

import atexit as __atexit
import RPi.GPIO as __gpiolib

# Ouvrir le GPIO à l'importation - module à la 'singleton'
__gpiolib.setmode(__gpiolib.BCM)

# Libérer les GPIO à la fermeture
__atexit.register(__gpiolib.cleanup)

GPIO_INPUT = 'I'
GPIO_OUTPUT = 'O'
GPIO_PWM = 'P'

# Les entrées numériques font des pulsations
__pwm_list = {}

def setup(pin_number, mode=None):
    # Mettre en mode input, mode output ou libérer la GPIO.
    if mode == GPIO_INPUT:
        __gpiolib.setup(pin_number, __gpiolib.IN, pull_up_down=__gpiolib.PUD_DOWN)
    elif mode == GPIO_OUTPUT:
        __gpiolib.setup(pin_number, __gpiolib.OUT, initial=__gpiolib.LOW)
    elif mode == GPIO_PWM:
        __gpiolib.setup(pin_number, __gpiolib.OUT, initial=__gpiolib.LOW)
        __pwm_list[pin_number] = {"pwm":__gpiolib.PWM(pin_number, 0.1), "freq":0}
    else:
        if pin_number in __pwm_list:
            __pwm_list[pin_number]["pwm"].stop()
            del __pwm_list[pin_number]
        __gpiolib.cleanup(pin_number)


def pin(pin_number, state=None):
    # Lecture, et optionnellement écriture si 'state' n'est pas vide et la pin est en OUTPUT.
    if (state is not None):
        if pin_number in __pwm_list and __pwm_list[pin_number]["freq"] != state:
            if state > 0:  # En PWM changer la fréquence. 0 est off.
                __pwm_list[pin_number]["pwm"].start(50)
                __pwm_list[pin_number]["freq"] = state
                __pwm_list[pin_number]["pwm"].ChangeFrequency(__pwm_list[pin_number]["freq"])
            else:
                __pwm_list[pin_number]["pwm"].stop()
                __pwm_list[pin_number]["freq"] = 0
        elif __gpiolib.gpio_function(pin_number) == __gpiolib.OUT and __gpiolib.input(pin_number) != state:
            __gpiolib.output(pin_number, state)

    if pin_number in __pwm_list:
        return __pwm_list[pin_number]["freq"]
    else:
        return __gpiolib.input(pin_number)

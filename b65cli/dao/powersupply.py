# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import atexit as __atexit

import serial as __serial

import time as __time

#Déclarer port série
__comm = None

#Conserver en mémoire pour éviter de surcharger le port série
__curr_ovp = None
__curr_ocp = None
__curr_volt = 0
__curr_current = 0
__curr_voltage = None

#Paramètres
DELAY = 0.07

def shutdown():
    off()
    close()

#Il faut l'appeler après la déclaration
__atexit.register(shutdown)

def connect(port='/dev/ttyUSB0', baud=9600):
    global __comm
    if __comm is None or not __comm.isOpen():
        try:
            __comm = __serial.Serial(port, baud, parity=__serial.PARITY_NONE, stopbits=__serial.STOPBITS_ONE, timeout=0.25, writeTimeout=0.25)
            off()
        except Exception as e:
            __comm = None
            print(e)

def close():
    if __comm is not None:
        __comm.close()


def __call(command):
    'Appels sur port série et retour.'
    try:
        print command,
        connect()
        __comm.flush()
        __comm.write(command + '\r')
        output = ''
        __time.sleep(DELAY)
        nb = __comm.inWaiting()
        if nb:
            output += __comm.read(nb)

        if len(output) == 0:
            raise Exception('InvalidCommandOrDelayTooShort')
            #off()  # Erreur -> éteindre sortie
        else:
            output = output.replace('\r', '')[:-2]
        print output
    except Exception as e:
        output = None
        print e

    return output

# Datasheet Power Supply
# http://www.testequity.com/documents/pdf/manuals/1685B-1687B-1688B-M.pdf

# Shutdown off
def on():
    '0 pour allumer'
    global __curr_voltage
    if __curr_voltage != 0:
        while __call('SOUT0') is None:
            __time.sleep(DELAY)
        __curr_voltage = 0

# Shutdown on
def off():
    '1 pour fermer'
    global __curr_current
    global __curr_volt
    global __curr_voltage
    if __curr_voltage != 1:
        while __call('SOUT1') is None:
            __time.sleep(DELAY)
        while __call('VOLT000') is None:
            __time.sleep(DELAY)
        while __call('CURR000') is None:
            __time.sleep(DELAY)
        __curr_current = 0
        __curr_volt = 0
        __curr_voltage = 1

def state():
    '1 pour actif, 0 pour inactif'
    state = __call('GOUT')
    while state is None:
        __time.sleep(DELAY)
        state = __call('GOUT')
    return 1 - state

def set_clamp(volt, curr):
    global __curr_ovp
    global __curr_ocp

    'Protection survoltage, surcourant'
    volt = int(volt * 10)
    curr = int(curr * 10)

    __curr_ovp = volt
    __curr_ocp = curr

    max = int(__call('GMAX'))
    if volt <= (max / 1000):
        while __call('SOVP' + str(volt).zfill(3)) is None:
            __time.sleep(DELAY)

    if curr <= (max % 1000):
        while __call('SOCP' + str(curr).zfill(3)) is None:
            __time.sleep(DELAY)

def get_status():
    'Retourne voltage, courant et si la sortie est limitée par la tension ou le courant'
    output = __call('GETD')
    if output is None: # Si erreur port série on ignore et continue
        return None

    voltage = float(output[0:4]) / 100.0
    current = float(output[4:8]) / 100.0
    cvcc = int(output[8:9])  # 0=cv, 1=cc
    power = round(voltage * current,2)

    return {
        'voltage': voltage,
        'current': current,
        'power': power,
        'cvcc': cvcc
    }

def set_current(curr):
    global __curr_current
    curr = int(curr * 10)

    if curr < 0:
        curr = 0

    if __curr_current != curr and __curr_ocp >= curr:
    # Format CURRnnn en dixiemes
        if __call('CURR' + str(curr).zfill(3)) is not None:
            __curr_current = curr

def set_voltage(volt):
    global __curr_volt
    volt = int(volt * 10)

    if volt < 33:
        volt = 33

    if __curr_volt != volt and __curr_ovp >= volt:
    # Format VOLTnnn en dixiemes
        if __call('VOLT' + str(volt).zfill(3)) is not None:
            __curr_volt = volt
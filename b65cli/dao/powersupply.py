# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import atexit as __atexit
import serial as __serial
import time as __time
import os as __os

#Accès au powersupply B&K 1687B par le port série.

#Déclarer port série
__comm = None

#Conserver en mémoire pour éviter de surcharger le port série
__curr_ovp = None
__curr_ocp = None
__curr_volt = 0
__curr_current = 0
__curr_state = None

#Paramètres
DELAY = 0.07

def shutdown():
    off()
    close()

#Fermer quand le programme est quitté : Il faut l'appeler après la déclaration
__atexit.register(shutdown)

def connect(port='/dev/ttyUSB0', baud=9600):
    "Vérifier si la connexion est déjà ouverte, sinon ouvrir."
    global __comm
    if not __os.path.exists(port):
        raise Exception('PortDoesNotExist')

    if __comm is None or not __comm.isOpen():
        try:
            __comm = __serial.Serial(port, baud, parity=__serial.PARITY_NONE, stopbits=__serial.STOPBITS_ONE, timeout=0.25, writeTimeout=0.25)
            off()
        except Exception as e:
            __comm = None
            print(e)

def close():
    "Fermer la connexion"
    if __comm is not None:
        __comm.close()

def __call(command):
    "Écrire sur port série et retourner la réponse."
    try:
        connect()
        __comm.flush() # Vider le buffer
        __comm.write(command + '\r') # Envoyer la commande
        output = ''
        __time.sleep(DELAY) # Attendre la réponse...
        nb = __comm.inWaiting() # Savoir combien d'octets lire
        if nb: # Lecture si plus que zéro caractères en attente
            output += __comm.read(nb)

        if len(output) == 0:
            # Le power supply répond toujours quand la commande est valide.
            # Soit on a pas attendu assez ou la commande n'est pas bonne.
            raise Exception('NoAnswerInvalidCommandOrDelayTooShort')
        else:
            # Enlever les retours de ligne non standards et le "OK"
            output = output.replace('\r', '')[:-2]

    except Exception: # Envoyer nul à la sortie si une exception est lancée par PySerial
        output = None

    return output

# Datasheet Power Supply
# http://www.testequity.com/documents/pdf/manuals/1685B-1687B-1688B-M.pdf

# Fonctions suivantes pour rendre les appels au powersupply plus conviviaux
# et rendre la valeur de retour en format utilisable

# Shutdown off - donc ON
def on():
    '0 pour allumer'
    global __curr_state
    if __curr_state != 0:
        count = 0
        while __call('SOUT0') is None and count < 5 : # Si le PSU ne répond pas correctement, 5 essais
            __time.sleep(DELAY) # Attendre et recommencer
            count +=1
        __curr_state = 0

# Shutdown on - donc OFF
def off():
    '1 pour fermer'
    global __curr_current
    global __curr_volt
    global __curr_state
    if __curr_state != 1: #Si pas déjà fermé
        count = 0
        while __call('SOUT1') is None and count < 5: #Shutdown
            __time.sleep(DELAY)
            count += 1
        count = 0
        while __call('VOLT000') is None and count < 5: #Reset voltage à zero
            __time.sleep(DELAY)
            count += 1
        count = 0
        while __call('CURR000') is None and count < 5: #Reset courant à zéro
            __time.sleep(DELAY)
            count += 1
        __curr_current = 0
        __curr_volt = 0
        __curr_state = 1

def state(): #Retourne si on ou off
    '1 pour actif, 0 pour inactif'
    state = __call('GOUT')
    count = 0
    while state is None and count < 5:
        __time.sleep(DELAY)
        state = __call('GOUT')
        count += 1
    return 1 - state

def set_clamp(volt, curr):
    'Settings de protection survoltage, surcourant \
    empêche une erreur du programme de surcharger la sortie'
    global __curr_ovp
    global __curr_ocp

    volt = int(volt * 10)
    curr = int(curr * 10)


    max = __call('GMAX')
    count = 0
    while max is None and count < 5:
        max = __call('GMAX')
        count += 1

    if max is not None:
        max = int(max)
    else:  # Power supply ne communique pas - ne pas faire planter pour être capable d'effacer le service par le web
        max = 0
        volt = 0
        curr = 0

    if volt <= (max / 1000):
        count = 0
        while __call('SOVP' + str(volt).zfill(3)) is None and count < 5:
            __time.sleep(DELAY)
            count += 1
    __curr_ovp = volt

    if curr <= (max % 1000):
        count = 0
        while __call('SOCP' + str(curr).zfill(3)) is None and count < 5:
            __time.sleep(DELAY)
            count += 1
    __curr_ocp = curr


def get_status():
    'Retourne voltage, courant et si la sortie est limitée par la tension ou le courant'
    output = __call('GETD')
    if output is None: # Si erreur port série on ignore et continue
        return None

    voltage = float(output[0:4]) / 100.0 #4 premiers caracteres voltage en 0.01V
    current = float(output[4:8]) / 100.0 #4 suivants courant en 0.01V
    cvcc = int(output[8:9])  # 0=cv, 1=cc
    power = round(voltage * current,2) # Calculer puissance (W) arrondie au 100eme

    return {
        'voltage': voltage,
        'current': current,
        'power': power,
        'cvcc': cvcc
    }

def set_current(curr):
    "Changer le setting de courant max"
    global __curr_current
    curr = int(curr * 10)

    if curr < 0:
        curr = 0

    # Si le setting est déjà le même, ne pas envoyer d'appels inutiles.
    if __curr_current != curr and __curr_ocp >= curr:
    # Format CURRnnn en dixiemes
        if __call('CURR' + str(curr).zfill(3)) is not None:
            __curr_current = curr # Conserver le courant actuel si l'envoi a fonctionné

def set_voltage(volt):
    "Changer le voltage max"
    global __curr_volt
    volt = int(volt * 10)

    if volt < 33: # Minimum pour faire tourner le ventilateur, ne pas aller en dessous.
        volt = 33

    # Si la tension est déjà au même niveau, ne pas modifier.
    if __curr_volt != volt and __curr_ovp >= volt:
    # Format VOLTnnn en dixiemes
        if __call('VOLT' + str(volt).zfill(3)) is not None:
            __curr_volt = volt # Appel réussi, conserver la nouvelle valeur en mémoire.
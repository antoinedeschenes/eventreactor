#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import serial


ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 1)

def ecrire(chaine):
    ser.write(chaine + '\r')
    sortie=''
    while sortie[-3:]!='OK\r':
        lecture = ser.read()
        sortie = sortie + str(lecture)
	if len(lecture)==0:
            return
    sortie = sortie.replace('\r','\n')[:-3]
    print(sortie)


while True:
    ecrire(raw_input('?'))




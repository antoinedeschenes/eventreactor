#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
import RPIO.PWM as PWM

#GPIO.cleanup()
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(13, GPIO.OUT)
#reponse=''
#p=GPIO.PWM(13, 20)#

#p.start(50)
#while reponse!='q':
#    reponse=raw_input('freq')
#    if reponse!='q':
#	p.ChangeFrequency(float(reponse))
#	reponse=raw_input('duty')
#	p.ChangeDutyCycle(float(reponse))
    
#p.stop()
#GPIO.cleanup()

patate = 0

PWM.setup(5,1)

PWM.init_channel(0,10000)

while (patate<2200):
    time.sleep(0.5)
    patate+=20
    #PWM.clear_channel(0)
    PWM.add_channel_pulse(0,13,patate,5)
    PWM.add_channel_pulse(0,27,patate,5)
	


raw_input("...")

PWM.clear_channel(0)

PWM.cleanup()

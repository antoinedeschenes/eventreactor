#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import smbus
import time

t_reg = 0x05
address = 0x18
bus = smbus.SMBus(1) # change to 0 for older RPi revision

csv='{0};{1:.4f};\n'

while True:
    reading = bus.read_i2c_block_data(address, t_reg)
    t = (reading[0] << 8) + reading[1]

    # calculate temperature (see 5.1.3.1 in datasheet)
    temp = t & 0x0FFF
    temp /=  16.0
    if (t & 0x1000):
        temp -= 256

    thetime=time.strftime('%Y-%m-%d;%H:%M')
    thestring=csv.format(thetime,temp)
    with open("temp.log", 'a') as f:
        f.write(thestring)
    print('{0:.1f}°C').format(temp)
    print(str(temp*9.0/5.0+32.0)+"°F")
    time.sleep(60)
    

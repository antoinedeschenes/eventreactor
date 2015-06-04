#!/usr/bin/python
# -*- coding: utf-8 -*-


import smbus

class TMP007:

    # TMP007 Address
    address = 0x40


    # Constructor
    def __init__(self):
        self.bus = smbus.SMBus(1)

    def readObjTemp(self):
        t = self.bus.read_i2c_block_data(self.address, 3)
        t = ((t[0] << 8) + t[1])
        if t & 0x8000:
            t -= 0x10000

        print "{0:b}".format(t)
        if t & 0x0001: # Bit d'erreur, cette valeur ne compte pas
            return None

        # 14 premiers bits contiennent la température en 32e de degrés
        return  (t >> 2) / 32.0

    def readDieTemp(self):
        t = self.bus.read_i2c_block_data(self.address, 1)
        t = ((t[0] << 8) + t[1])

        if t & 0x0001:  # Bit d'erreur, cette valeur ne compte pas
            return None

        # 14 premiers bits contiennent la température en 32e de degrés
        return (t >> 2) / 32.0

    def readSensorVoltage(self):
        "Read IR sensor voltage data from sensor"

        rawData = self.readU16(0)
        rawData = self.reverseByteOrder(rawData)

        # IR Voltage in uV
        irVoltage = float(rawData) * 156.25 / 1000000

        return irVoltage



    def readU16(self, reg):
        return self.bus.read_word_data(self.address, reg)



    def reverseByteOrder(self, data):
        byteCount = len(hex(data)[2:].replace('L', '')[::2])
        val = 0
        for i in range(byteCount):
            val = (val << 8) | (data & 0xff)
            data >>= 8
        return val


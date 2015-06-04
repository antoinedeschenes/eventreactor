#!/usr/bin/python

import smbus

# ===========================================================================
# I2C Base Class
# Thanks for Adafruit-Raspberry-Pi-Python-Code - Adafruit_I2C.py
# ===========================================================================

class I2CBase:
    def __init__(self, address):
        self.address = address
        self.bus = smbus.SMBus(1)


    def reverseByteOrder(self, data):
        byteCount = len(hex(data)[2:].replace('L', '')[::2])
        val = 0
        for i in range(byteCount):
            val = (val << 8) | (data & 0xff)
            data >>= 8
        return val

    def write16(self, reg, value):
            self.bus.write_word_data(self.address, reg, value)


    def write16(self, reg, value):
            self.bus.write_word_data(self.address, reg, value)

    def readU16(self, reg):
            result = self.bus.read_word_data(self.address, reg)

    def readU16(self, reg):
            result = self.bus.read_word_data(self.address, reg)

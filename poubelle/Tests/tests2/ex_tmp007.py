#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import math
import os

from lib_tmp007 import TMP007


# ===========================================================================
# Example Code of TMP007
# ===========================================================================

# Initialize the TMP007
tmp = TMP007()

for _ in range(1000):
    objTemp = tmp.readObjTemp()
    #dieTemp = tmp.readDieTemp()
    #irVoltage = tmp.readSensorVoltage()
    #os.system('clear');
    print (objTemp)

    time.sleep(0.2)

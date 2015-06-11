# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import time
from .service import Service

# Retourne le temps UNIX - peut servir pour les événements périodiques
class Timeclock(Service):
    def __init__(self, config):
        super(Timeclock, self).__init__(config)
        self.readables["time"] = None

    def refresh(self):
        "Mets le temps unix en mémoire "
        self.readables["time"] = round(time.time(), 2)


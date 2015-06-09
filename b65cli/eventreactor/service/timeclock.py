from twisted.internet.defer import Deferred

__author__ = 'Antoine'

import time
from .service import Service


class Timeclock(Service):
    def __init__(self, config):
        super(Timeclock, self).__init__(config)
        self.readables["time"] = None

    def refresh(self):
        self.readables["time"] = round(time.time(), 2)


from twisted.internet.defer import Deferred

__author__ = 'Antoine'

import dao.gpio
from .service import Service


class GPIO(Service):
    GPIO_INPUT = dao.gpio.GPIO_INPUT
    GPIO_OUTPUT = dao.gpio.GPIO_OUTPUT

    def __init__(self, config):
        super(GPIO, self).__init__(config)

        self.readables["state"] = None
        self.writables["state"] = None

        dao.gpio.setup(self.config["pin"], self.config["mode"])

    def refresh(self):
        self.readables["state"] = dao.gpio.pin(self.config["pin"], self.writables["state"])
        self.writables["state"] = None

    def cleanup(self):
        dao.gpio.setup(self.config["pin"])


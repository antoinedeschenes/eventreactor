# -*- coding: utf-8 -*-
__author__ = 'Antoine'

from .service import Service

class Variable(Service):
    def __init__(self, config):
        super(Variable, self).__init__(config)
        self.readables["value"] = config["initial"]
        self.writables["value"] = None

    def refresh(self):
        if self.writables["value"] is not None:
            self.readables["value"] = self.writables["value"]
            self.writables["value"] = None



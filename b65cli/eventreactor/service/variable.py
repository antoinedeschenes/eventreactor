# -*- coding: utf-8 -*-
__author__ = 'Antoine'

from .service import Service

# Conserve une valeur écrite par une réaction d'événement en variable
# On peut mettre une valeur initiale en configuration
class Variable(Service):
    def __init__(self, config):
        super(Variable, self).__init__(config)
        self.readables["value"] = config["initial"]
        self.writables["value"] = None

    def refresh(self):
        "Si une nouvelle valeur est reçue, la mettre à jour"
        if self.writables["value"] is not None:
            self.readables["value"] = self.writables["value"]
            self.writables["value"] = None



# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

#Classe de base pour tous les services
class Service(object):
    #Constantes de types
    TYPE_GPIO = 1
    TYPE_TEMPERATURE = 2
    TYPE_THERMOELECTRIC = 3
    TYPE_TIMECLOCK = 4
    TYPE_VARIABLE = 5

    def __init__(self, config):
        self.readables = dict() # Valuers lues dans les refresh
        self.writables = dict() # Valeurs écrites par les réactions des événements à procéder au refresh
        self.config = config

    def access(self, attribute=None, value=None):
        "Méthode enregistrée sur le réseau."
        if attribute is None: #Sans paramètres : retourner toutes les valeurs et la config.
            return { 'values':self.readables, 'config':self.config}
        elif value is None: # Valeur en paramètres : retourner la donnée
            return self.readables[attribute]
        else: # Valeur en écriture passée, l'écrire dans le service.
            self.writables[attribute]=value
            return

    def refresh(self):
        "Méthode bidon commune à redéfinir"
        pass

    def cleanup(self):
        "Méthode bidon commune à redéfinir optionnellement s'il y a des suppressions nécessaires"
        pass


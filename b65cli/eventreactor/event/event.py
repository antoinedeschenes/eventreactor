# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks

__author__ = 'Antoine Deschênes'

from eventreactor.event.reaction import Reaction

# Génère les événements et appelle les réactions lorsque la condition change.
class Event(object):
    def __init__(self, provider, config):
        self.provider = provider
        self.config = {
            "condition": None,
            "onTrue": {},
            "onFalse": {},
            "lastState": None
        }
        self.onTrue = []
        self.onFalse = []
        self.configure(config)

    def configure(self, new_config):
        # Fonction pour la configuration initiale ou subséquente d'un événement.

        # Pour appliquer les réactions créées après que l'événement se soit produit
        execute_reaction = self.config["lastState"]

        if "condition" in new_config:
            self.config["condition"] = new_config["condition"]

        #Chercher les attributs modifié et les supprimer. La création se fait plus tard
        if "onTrue" in new_config:
            for attribute in self.config["onTrue"].keys():
                if attribute in new_config["onTrue"]:
                    if new_config["onTrue"][attribute] != self.config["onTrue"][attribute]:
                        # Une valeur différente efface la réaction.
                        del self.config["onTrue"][attribute]
                        for reaction_object in self.onTrue:
                            if reaction_object.service_attribute == attribute:
                                self.onTrue.remove(reaction_object)

            # Nouvelle réaction à créer si cet attribut n'existait pas. Un None est une suppression, à ignorer.
            for attribute in new_config["onTrue"]:
                if attribute not in self.config["onTrue"] and new_config["onTrue"][attribute] is not None:
                    self.config["onTrue"][attribute] = new_config["onTrue"][attribute]
                    self.onTrue.append(
                        Reaction(self.provider, attribute, self.config["onTrue"][attribute], execute_reaction))


        #Même chose pour onFalse
        if "onFalse" in new_config:
            for attribute in self.config["onFalse"].keys():
                if attribute in new_config["onFalse"]:
                    if new_config["onFalse"][attribute] != self.config["onFalse"][attribute]:
                        del self.config["onFalse"][attribute]
                        for reaction_object in self.onFalse:
                            if reaction_object.service_attribute == attribute:
                                self.onFalse.remove(reaction_object)

            #Répéter pour onFalse
            for attribute in new_config["onFalse"]:
                if attribute not in self.config["onFalse"] and new_config["onFalse"][attribute] is not None:
                    self.config["onFalse"][attribute] = new_config["onFalse"][attribute]
                    self.onFalse.append(Reaction(self.provider, attribute, self.config["onFalse"][attribute], not execute_reaction))

        #Configuration à garder dans le fichier. lastState n'est pas utile.
        output_config = self.config.copy()
        del output_config["lastState"]
        return output_config

    @inlineCallbacks
    def refresh(self):
        #Vérifier l'état de la condition
        new_state = yield self.provider.helper.parsecondition(self.config["condition"])

        # Si la réponse passe vers True ou vers False, appeler les réactions
        if (self.config["lastState"] is None and new_state is not None) or self.config["lastState"] != new_state:
            if new_state is True:
                for reaction in self.onTrue:
                    try:
                        reaction.execute()
                    except Exception as e:
                        print(e.message)
            elif new_state is False:
                for reaction in self.onFalse:
                    try:
                        reaction.execute()
                    except Exception as e:
                        print(e.message)

            self.config["lastState"] = new_state

    def access(self):
        "Retourne la config courante"
        return self.config

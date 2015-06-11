# -*- coding: utf-8 -*-
__author__ = 'Antoine Deschênes'

import json as __json

# Lecture et écriture du fichier JSON qui contient la configuration.
# Le nom est toujours celui de la machien qui l'exécute.

def read_config(name):
    "Lire le fichier de configuration ou le modèle vide"
    config = { "services":{}, "events":{} }
    try:
        with open(name + '.conf', 'r') as configfile:
            config.update(__json.loads(configfile.read()))
    except Exception:
        pass
    return config

def write_config(name, config):
    "Écrire le fichier de config"
    with open(name + '.conf', 'w') as configfile:
        configfile.write(__json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')))



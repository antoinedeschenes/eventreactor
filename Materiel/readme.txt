Documentation pour les librairies matérielles fournies avec Raspbian:

PySerial : 	http://pyserial.sourceforge.net/
SMBus : 	https://github.com/bivab/smbus-cffi 
RPi.GPIO : 	http://sourceforge.net/projects/raspberry-gpio-python/

Le code pour la lecture des thermomètres est basé légèrement sur 
celui fourni par Adafruit pour le capteur MCP9808, puis modifié pour le TMP007 :
https://learn.adafruit.com/mcp9808-temperature-sensor-python-library/overview


Contenu des fichiers PDF :

Semiconducteurs:
ULN2003A 	- Sert à alimenter le relais inversant la phase de la plaque thermoélectrique;
CP85438 	- Plaque thermoélectrique;
MCP9808 	- Thermomètre à contact direct;
TMP007  	- Thermomètre infrarouge.

Bloc d'alimentation:
1687B   	- Protocole de communication par port série du bloc d'alimentation à partir de la page 26.



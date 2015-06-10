Documentation pour les librairies mat�rielles fournies avec Raspbian:

PySerial : 	http://pyserial.sourceforge.net/
SMBus : 	https://github.com/bivab/smbus-cffi 
RPi.GPIO : 	http://sourceforge.net/projects/raspberry-gpio-python/

Le code pour la lecture des thermom�tres est bas� l�g�rement sur 
celui fourni par Adafruit pour le capteur MCP9808, puis modifi� pour le TMP007 :
https://learn.adafruit.com/mcp9808-temperature-sensor-python-library/overview


Contenu des fichiers PDF :

Semiconducteurs:
ULN2003A 	- Sert � alimenter le relais inversant la phase de la plaque thermo�lectrique;
CP85438 	- Plaque thermo�lectrique;
MCP9808 	- Thermom�tre � contact direct;
TMP007  	- Thermom�tre infrarouge.

Bloc d'alimentation:
1687B   	- Protocole de communication par port s�rie du bloc d'alimentation � partir de la page 26.



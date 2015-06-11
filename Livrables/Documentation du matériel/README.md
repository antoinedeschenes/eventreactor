###Documentation pour les librairies matérielles fournies avec Raspbian :
 - PySerial : http://pyserial.sourceforge.net/
 - SMBus : https://github.com/bivab/smbus-cffi
 - RPi.GPIO : http://sourceforge.net/projects/raspberry-gpio-python/
 
>Le code pour la lecture des thermomètres est basé légèrement sur 
celui fourni par Adafruit pour le capteur MCP9808, puis modifié pour le TMP007 : <br>
[MCP9808 Temperature Sensor Library](https://learn.adafruit.com/mcp9808-temperature-sensor-python-library/overview)

###Fiches techniques dans le dossier : 

#####Semiconducteurs:
 - [STMicro ULN2003A](ULN2003A.pdf) : Sert à alimenter le relais inversant la phase de la plaque thermoélectrique;
 - [CUI CP85438](CP85438.pdf) : Plaque thermoélectrique;
 - [Microchip MCP9808](MCP9808.pdf) : Thermomètre à contact direct;
 - [Texas Instruments TMP007](TMP007.pdf) : Thermomètre infrarouge.

#####Bloc d'alimentation : 
 - [B&K 1687B](1687B.pdf) : Protocole de communication par port série du bloc d'alimentation à partir de la page 26.



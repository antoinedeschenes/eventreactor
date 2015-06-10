Event Reactor
=============

[Event Reactor] est un ensemble d'applications permettant la programmation d'événements et de réactions à distance. On peut 

Outils technologiques
---------------------
Informations sur les outils technologiques utilisés pour le développement d'Event Reactor.

### Environnements de développement (**IDE**)
 - [PhpStorm] - **IDE** basé sur [IntelliJ IDEA] optimisé pour le web (PHP, JS, HTML5, CSS, etc.)
 - [PyCharm] - **IDE** basé sur [IntelliJ IDEA] optimisé pour Python


### Librairies et langages de programmation
Interface de gestion web __(HTML/JS)__ :
 - [jQuery] - Accélère le développement JavaScript.
 - [Autobahn|JS] - Permet la communication [WAMP] avec JavaScript.

Fournisseur de services __(Python)__ :
 - [Autobahn|Python] - Fournit une couche supplémentaire permettant la communication [WAMP] à travers Twisted.
 - [Twisted] - Librairie permettant la communication réseau et fournissant un système de programmation asynchrone.

Serveur web __(Python)__ :
 - [Crossbar] - Fournit un serveur/routeur [WAMP] en Python.

Installation et exécution
-------------------------
### Serveur
Le serveur est déjà fonctionnel en ligne. Pour l'installer soi-même, voici les étapes d'installation pour [Ubuntu] :
```sh 
# Installer les prérequis
$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-pip

# Utiliser pip pour installer la librairie Crossbar et toutes ses dépendances 
$ sudo pip install crossbar[all]

# Ouvrir le port du pare-feu s'il n'est pas standard
$ sudo ufw allow 8080

# Envoyer le dossier b65serv au serveur par SFTP ou un autre moyen, puis se déplacer dans le dossier
$ cd b65serv

# Démarrer le serveur crossbar
$ crossbar start
```
Note: Il est préférable d'exécuter le programme dans une session virtuelle `screen` pour que le programme fonctionne même lorsqu'on se déconnecte de notre session. Pour revenir à la session sur le  serveur, simplement exécuter `screen -R`.

### Client Raspberry Pi (Raspbian)
Si vous avez un [Raspberry Pi] avec la distribution Raspbian, voici comment installer et exécuter le logiciel client :
```sh
# Installer les prérequis 
$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-pip libi2c-dev i2c-tools

# Installer la librairie Autobahn-Python et ses dépendances à l'aide de pip
$ pip install autobahn[twisted]

# Déplacer le dossier b65cli par SFTP ou un autre moyen, puis se déplacer dans le dossier
$ cd b65cli

# Démarrer l'application client (les droits root sont nécessaires pour avoir accès au matériel)
$ sudo python main.py
```
Note : Comme pour le serveur, une session `screen` est préférable.

###Client Windows

Installation du logiciel client sous Windows :
 * Télécharger Python 2.7 32-bits : https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi
 * Démarrer l'installation en prenant soin d'ajouter l'option **"Add python.exe to path"**
 * Par la ligne de commande, installer la librairie Autobahn|Python : 

```cmd
pip install autobahn[twisted]
```

 - Exécuter le fichier `main.py` du dossier b65cli. Si Python n'est pas associé aux fichiers .py, vous pouvez exécuter `python main.py` en ligne de commande. Les droits administratifs ne sont pas nécessaires, car la version Windows n'a aucun accès au matériel. 

Temps investi
-------------


Coordonnées
-----------
Pour me contacter par courriel : antoine@antoinedeschenes.com


<!-- Sites en références -->

[Event Reactor]:https://bitbucket.org/antoinedeschenes/eventreactor

[Crossbar]:http://crossbar.io/
[WAMP]:http://wamp.ws/
[Autobahn|JS]:http://autobahn.ws/js/
[jQuery]:https://jquery.com/
[Autobahn|Python]:http://autobahn.ws/python/
[Twisted]:https://twistedmatrix.com/

[IntelliJ IDEA]:https://www.jetbrains.com/idea/
[PhpStorm]:https://www.jetbrains.com/phpstorm/
[PyCharm]:https://www.jetbrains.com/pycharm/

[Ubuntu]:http://www.ubuntu.com
[Raspberry Pi]:https://www.raspberrypi.org/
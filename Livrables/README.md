Event Reactor
=============

Event Reactor est un ...

  - Type some Markdown on the left
  - See HTML in the right
  - Magic

Quote : 
> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a


Outils technologiques
---------------------
Informations sur les outils technologiques utilisés pour le développement d'Event Reactor.

### Environnements de développement (**IDE**)

- [PhpStorm] - **IDE** basé sur [IntelliJ IDEA] optimisé pour le web (PHP, JS, HTML5, CSS, etc.)
- [PyCharm] - **IDE** basé sur [IntelliJ IDEA] optimisé pour Python

### Librairies 

Interface de gestion web (HTML/JS) :
- [jQuery] - Accélère le développement JavaScript.
- [Autobahn|JS] - Permet la communication [WAMP] avec JavaScript.

Fournisseur de services (Python) :
- [Autobahn|Python] - Fournit une couche supplémentaire permettant la communication [WAMP] à travers Twisted.
- [Twisted] - Librairie permettant la communication réseau et fournissant un système de programmation asynchrone.

Serveur web (Python) :
- [Crossbar] - Fournit un serveur/routeur [WAMP] en Python.

Installation
------------
```sh
$ sudo apt-get install dev ci dev ça
```


### Development

First Tab:
```cmd
$ node app
```

Second Tab:
```sh
$ gulp watch
```

(optional) Third:
```sh
$ karma start
```

[WAMP]:http://wamp.ws/

[Autobahn|JS]:http://autobahn.ws/js/
[jQuery]:https://jquery.com/

[Autobahn|Python]:http://autobahn.ws/python/
[Twisted]:https://twistedmatrix.com/

[Crossbar]:http://crossbar.io/

[IntelliJ IDEA]:https://www.jetbrains.com/idea/
[PhpStorm]:https://www.jetbrains.com/phpstorm/
[PyCharm]:https://www.jetbrains.com/pycharm/


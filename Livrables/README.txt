# Event Reactor

Dillinger is a cloud-enabled, mobile-ready, offline-storage, AngularJS powered HTML5 Markdown editor.

  - Type some Markdown on the left
  - See HTML in the right
  - Magic

Markdown is a lightweight markup language based on the formatting conventions that people naturally use in email.  As [John Gruber] writes on the [Markdown site] [1]:

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Version
3.0.0

### Outils technologiques

Informations sur les outils technologiques utilisés pour le développement d'Event Reactor.

Environnements de développement (*IDE*) :

* [PhpStorm] - *IDE* basé sur [IntelliJ IDEA] optimisé pour le web (PHP, JS, HTML5, CSS, etc.)
* [PyCharm] - *IDE* basé sur [IntelliJ IDEA] optimisé pour Python

Librairies JavaScript pour l'interface web :

* [jQuery] - API pour accélérer le développement JavaScript.
* [Autobahn|JS] - API permettant 

Librairies Python pour le fournisseur de services 

* [Autobahn|Python] - API permettant 
* [Twisted] - API dont Autobahn dépend




### Installation

```sh
$ git clone [git-repo-url] dillinger
$ cd dillinger
$ npm i -d
$ mkdir -p public/files/{md,html,pdf}
$ gulp build --prod
$ NODE_ENV=production node app
```

### Plugins

Dillinger is currently extended with the following plugins

* Dropbox
* Github
* Google Drive
* OneDrive

Readmes, how to use them in your own application can be found here:

* plugins/dropbox/README.md
* plugins/github/README.md
* plugins/googledrive/README.md
* plugins/onedrive/README.md

### Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantanously see your updates!

Open your favorite Terminal and run these commands.

First Tab:
```sh
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



[IntelliJ IDEA]:https://www.jetbrains.com/idea/
[PhpStorm]:https://www.jetbrains.com/phpstorm/
[PyCharm]:https://www.jetbrains.com/pycharm/

[jQuery]:http://jquery.com
[Autobahn|JS]:http://autobahn.ws/js/

[Twisted]:https://twistedmatrix.com/trac/
[Autobahn|Python]:http://autobahn.ws/python/
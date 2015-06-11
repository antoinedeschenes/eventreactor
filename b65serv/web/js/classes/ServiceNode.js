
//Représentation d'un service côté page web. Construit le DOM approprié et contient les fonctions de rafraîchissement.
function ServiceNode(parent, name) {
    var caller = this;
    this.parent = parent;
    this.name = name;

    this.config = {};
    this.values = {};

    //Rang de table des services
    this.node = $('<tr>').insertBefore(serviceEditNode);

    //Cellule du lien pour effacer le service
    var deletecell = $('<td>').appendTo(this.node);
    $('<a>',{href:"javascript:;", text:"del"}).click(function(){caller.deleteFromProvider()}).appendTo(deletecell);

    //Cellule du nom
    $('<td>').text(parent.name + '.' + name).appendTo(this.node);

    //Cellule affichant les configs
    var cfgtd = $('<td>').appendTo(this.node);
    this.configsNode = $('<ul>').appendTo(cfgtd);
    //Cellule affichant les valeurs
    var valtd = $('<td>').appendTo(this.node);
    this.valuesNode = $('<ul>').appendTo(valtd);


    setTimeout(function () {
        caller.refresh()
    }, 500);
}

//Rafraîchit la configuration dans le DOM
ServiceNode.prototype.refresh = function () {
    var caller = this;
    connection.session.call(this.parent.name + ".serv." + this.name).then(function (data) {
        for (var key in data.config) {
            if (!(key in caller.config))
                caller.config[key] = $('<li>').appendTo(caller.configsNode);

            var configvalue = data.config[key];
            if (key in configstrings)
                configvalue = configstrings[key][configvalue];
            caller.config[key].text(key + ": " + configvalue);
        }
    });
};

//Rafraîchit les données lues dans le DOM
ServiceNode.prototype.refreshReadings = function () {
    var caller = this;
    connection.session.call(this.parent.name + ".serv." + this.name).then(function (data) {
        for (var key in data.values) {
            if (!(key in caller.values))
                caller.values[key] = $('<li>').appendTo(caller.valuesNode);
            var readingvalue = data.values[key];
            if (key in suffixdict)
                readingvalue += suffixdict[key];
            caller.values[key].text(key + ": " + readingvalue);
        }
    });
};

//Appelé de l'externe à la suppression du service.
ServiceNode.prototype.erase = function () {
    this.node.remove();
    this.node = undefined;
};

//Appel du bouton "del" dans l'interface pour effacer ce service sur le fournisseur.
ServiceNode.prototype.deleteFromProvider = function () {
    var calldata = { 'services':{}};
    calldata.services[this.name] = null;

    connection.session.call(this.parent.name + ".configure",[calldata]);
};

//Remplit l'éditeur de configuration avec les données courantes.
ServiceNode.prototype.getServiceConfiguration = function() {
    var caller = this;
    connection.session.call(this.parent.name + ".serv." + this.name).then(function (data) {
        var servicetype = data.config.type;
        $('#service-type-select').val(servicetype);
        selectServiceType(servicetype);
        for (var key in data.config){
            if(key !== "type")
                $('#'+key).val(data.config[key]);
        }
    });
};
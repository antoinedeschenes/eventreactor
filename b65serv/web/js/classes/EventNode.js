
//Représentation d'un événement côté page web. Construit le DOM approprié et contient les fonctions de rafraîchissement.
function EventNode(parent, name) {
    this.parent = parent;
    this.name = name;
    this.node = $('<tr>').insertBefore(eventEditNode);

    var caller = this;
    var deletecell = $('<td>').appendTo(this.node);
    $('<a>',{href:"javascript:;", text:"del"}).click(function(){caller.deleteFromProvider()}).appendTo(deletecell);

    $('<td>').text(parent.name + '.' + name).appendTo(this.node);

    this.conditiontd = $('<td>').appendTo(this.node);
    var reactiontd = $('<td>').appendTo(this.node);
    this.ontruenode = $('<ul>').appendTo(reactiontd);
    $('<h4>').text('On True:').appendTo(this.ontruenode);
    this.onfalsenode = $('<ul>').appendTo(reactiontd);
    $('<h4>').text('On False:').appendTo(this.onfalsenode);

    var caller = this;
    setTimeout(function() { caller.refresh()}, 500);
};

//Rafraîchit la liste de réactions et la condition dans le DOM
EventNode.prototype.refresh = function() {
    var caller = this;
    connection.session.call(this.parent.name + ".evt." + this.name).then(function(data) {
        caller.conditiontd.text(data.condition);

        caller.ontruenode.find('li').remove();
        caller.onfalsenode.find('li').remove();

        for (var key in data.onTrue){
            value = data.onTrue[key]
            if (key in suffixdict)
                value += suffixdict[key];
            $('<li>').text(key + ":" + value).appendTo(caller.ontruenode);
        }
        for (var key in data.onFalse){
            value = data.onFalse[key]
            if (key in suffixdict)
                value += suffixdict[key];
            $('<li>').text(key + ":" + value).appendTo(caller.onfalsenode);
        }
    });
};

//Retourne l'état courant (si vrai ou faux)
EventNode.prototype.refreshReadings = function () {
    var caller = this;
    connection.session.call(this.parent.name + ".evt." + this.name).then(function(data) {
        if(data.lastState === false){
            caller.ontruenode.removeClass('active-reaction');
            caller.onfalsenode.addClass('active-reaction')
        }

        if(data.lastState === true){
            caller.onfalsenode.removeClass('active-reaction')
            caller.ontruenode.addClass('active-reaction');
        }
    });

};

//Appelé de l'externe pour effacer le DOM quand l'événement est supprimé.
EventNode.prototype.erase = function() {
    this.node.remove();
    this.node = undefined;
};

//Effacer l'événement sur le fournisseur (bouton del sur l'interface)
EventNode.prototype.deleteFromProvider = function () {
    var calldata = { 'events':{}};
    calldata.events[this.name] = null;

    connection.session.call(this.parent.name + ".configure",[calldata]);
};

//Remplit l'éditeur de config avec les données.
EventNode.prototype.getEventConfiguration = function() {
    connection.session.call(this.parent.name + ".evt." + this.name).then(function(data) {
        $('#event-condition-input').val(data.condition);
        var ontruelist = $('#event-true-reactions');
        var onfalselist = $('#event-false-reactions');
        ontruelist.empty();
        onfalselist.empty();

        for (var key in data.onTrue)
            $('<option>',{text:key}).appendTo(ontruelist);
        for (var key in data.onFalse)
            $('<option>',{text:key}).appendTo(onfalselist);
    });
};

//Reçoit la valeur d'affectation d'une réaction vraie lorsqu'elle est sélectionnée.
EventNode.prototype.getTrueReactionValue = function(attribute) {
    connection.session.call(this.parent.name + ".evt." + this.name).then(function(data) {
        $('#true-value').val(data.onTrue[attribute]);
    });
};

//Reçoit la valeur d'affectation d'une réaction fausse lorsqu'elle est sélectionnée.
EventNode.prototype.getFalseReactionValue = function(attribute) {
    connection.session.call(this.parent.name + ".evt." + this.name).then(function(data) {
        $('#false-value').val(data.onFalse[attribute]);
    });
};
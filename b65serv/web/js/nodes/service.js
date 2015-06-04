function Service(parent, name) {
    this.parent = parent;
    this.name = name;
    this.node = $('<tr>').appendTo(servicesNode);
    $('<td>').text(parent.name + '.' + name).appendTo(this.node);

    var td = $('<td>').appendTo(this.node);
    this.configsNode = $('<ul>').appendTo(td);
    td = $('<td>').appendTo(this.node);
    this.readablesNode = $('<ul>').appendTo(td);


    this.values = {};
    this.config = {};

    this.refresh();
}


Service.prototype.refresh = function () {
    var caller = this;
    connection.session.call(this.parent.name + ".serv." + this.name).then(function (data) {
        for (var key in data.config) {
            if (!(key in caller.config))
                caller.config[key] = $('<li>').appendTo(caller.configsNode);

            var configvalue = data.config[key];
            if (key in configdict)
                configvalue = configdict[key][configvalue];
            caller.config[key].text(key + ": " + configvalue);
        }
    });
    this.refreshReadings();
};

Service.prototype.refreshReadings = function() {
    var caller = this;
    connection.session.call(this.parent.name + ".serv." + this.name).then(function (data) {
        for (var key in data.values) {
            if (!(key in caller.values))
                caller.values[key] = $('<li>').appendTo(caller.readablesNode);
            var readingvalue = data.values[key];
            if (key in suffixdict)
                readingvalue += suffixdict[key];
            caller.values[key].text(key + ": " + readingvalue);
        }
    });
};


Service.prototype.erase = function () {
    this.node.remove();
    this.node = undefined;
};
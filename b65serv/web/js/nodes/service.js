function Service(parent, name) {
    this.parent = parent;
    this.name = name;
    this.node = $('<tr>').appendTo(servicesNode);
    $('<td>').text(parent.name + '.' + name).appendTo(this.node);

    var nametd = $('<td>').appendTo(this.node);
    this.readablesNode = $('<ul>').appendTo(nametd);
    var valuetd = $('<td>').appendTo(this.node);
    this.valuesNode = $('<ul>').appendTo(valuetd);

    //this.node.onclick = function() {servicenode.expandtree()};
    //this.node.appendChild(document.createTextNode(this.name));
    //this.expand = false;


    this.readables = {};
    this.values = {};
    //this.readablesNode = document.createElement("ul");
    //this.node.appendChild(this.readablesNode);
    //this.parent.serviceNode.appendChild(this.node);
    this.refresh();


}

Service.prototype.expandtree = function () {
    this.expand = !this.expand;
}

Service.prototype.refresh = function () {
    //if (this.expand) {
        var service = this;
        connection.session.call(this.parent.name + ".serv." + this.name).then(function (data) {
            console.log(data);
            for (var key in data) {
                if (!(key in service.readables)) {
                    service.readables[key] = $('<li>').text(key).appendTo(service.readablesNode);
                    service.values[key] = $('<li>').appendTo(service.valuesNode);
                    //service.readablesNode.appendChild(service.readables[key]);
                }
                service.values[key].text(data[key]);
            }
        });
    //}
}

Service.prototype.erase = function () {
    //this.parent.serviceNode.removeChild(this.node);
    this.node.remove();
    this.node = undefined;
}
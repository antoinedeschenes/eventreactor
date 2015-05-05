function Service(parent, name) {
    this.parent = parent;
    this.name = name;
    this.node = document.createElement("ul");


    var servicenode = this;
    this.node.onclick = function() {servicenode.expandtree()};

    this.node.appendChild(document.createTextNode(this.name));
    this.expand = false;



    this.readables = {}
    this.readablesNode = document.createElement("ul");
    this.node.appendChild(this.readablesNode);
    this.parent.serviceNode.appendChild(this.node);
    this.refresh()
}

Service.prototype.expandtree = function() {
    this.expand = !this.expand;
}

Service.prototype.refresh = function () {
    if(this.expand) {
        var service = this;
        connection.session.call(this.parent.name + ".serv." + this.name).then(function (data) {
            for (var key in data) {
                if (!(key in service.readables)) {
                    service.readables[key] = document.createElement("li");
                    service.readablesNode.appendChild(service.readables[key]);
                }
                service.readables[key].textContent = data[key];
            }
        });
    }
}

Service.prototype.erase = function() {
    this.parent.serviceNode.removeChild(this.node);
    this.node = undefined;
}
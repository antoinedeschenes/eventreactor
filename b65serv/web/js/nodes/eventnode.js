/**
 * Created by Antoine on 2015-04-04.
 */
function EventNode(parent, name) {
    this.parent = parent;
    this.name = name;
    this.node = $('<tr>').appendTo(eventsNode);
    $('<td>').text(parent.name + '.' + name).appendTo(this.node);

    var nametd = $('<td>').appendTo(this.node);
    this.readablesNode = $('<ul>').appendTo(nametd);
    var valuetd = $('<td>').appendTo(this.node);
    this.valuesNode = $('<ul>').appendTo(valuetd);


    //this.node = document.createElement("ul");
    //this.node.appendChild(document.createTextNode(this.name));
    //this.expand = false;

    //var eventnode = this;
    //this.node.onclick = function() {eventnode.expandtree()};

    //this.attrNode = document.createElement("ul");
    //this.node.appendChild(this.attrNode);
    //this.parent.eventNode.appendChild(this.node);

    this.refresh();
};

EventNode.prototype.expandtree = function() {
    //this.expand = !this.expand;
}

EventNode.prototype.refresh = function () {
    var event = this;
    connection.session.call(this.parent.name + ".evt." + this.name).then(function(data) {
        console.log(data);
        /*for (var key in data) {
            if(!(key in service.readables)) {
                service.readables[key] = document.createElement("li");
                service.readablesNode.appendChild(service.readables[key]);
            }
            service.readables[key].textContent=data[key];
        }*/
    });

};

EventNode.prototype.erase = function() {
    this.parent.eventNode.removeChild(this.node);
    this.node = undefined;
};
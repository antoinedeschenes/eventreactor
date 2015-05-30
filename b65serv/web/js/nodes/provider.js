function Provider(name) {
    this.name = name;
    //this.node = document.createElement("tr");
    //this.expand = false;

    var provider = this; //Faire avec les problèmes de namespace...

    /*this.expandCell = document.createElement("td");
     this.expandCell.innerText = "+";
     this.expandCell.className = "expandcol";
     this.expandCell.onclick=function() {provider.expandtree()};
     this.node.appendChild(this.expandCell);

     var nameCell = document.createElement("td");
     nameCell.innerText = this.name;

     this.node.appendChild(nameCell);
     providerDom.appendChild(this.node);*/

    //this.serviceNode = document.createElement("div");
    //this.node.appendChild(this.serviceNode);
    //this.eventNode = document.createElement("div");
    //this.node.appendChild(this.eventNode);
    this.services = {};
    this.events = {};
    this.refresh();

    //console.log(this);
}


Provider.prototype.refresh = function () {
    //if(this.expand){
    var provider = this;
    connection.session.call(this.name + ".structure", []).then(function (structure) {
            var services = structure["services"]
            var events = structure["events"]
            var delServices = Object.keys(provider.services);
            var delEvents = Object.keys(provider.events);

            for (var i = 0; i < services.length; i++) {
                if (services[i] in provider.services)
                    delServices.splice(delServices.indexOf(services[i]), 1);
                else
                    provider.services[services[i]] = new Service(provider, services[i]);
            }
            for (var i = 0; i < delServices.length; i++) {
                provider.services[delServices[i]].erase();
                delete provider.services[delServices[i]];
            }

            for (var i = 0; i < events.length; i++) {
                if (events[i] in provider.events)
                    delEvents.splice(delEvents.indexOf(events[i]), 1);
                else
                    provider.events[events[i]] = new EventNode(provider, events[i]);
            }
            for (var i = 0; i < delEvents.length; i++) {
                provider.events[delEvents[i]].erase();
                delete provider.events[delEvents[i]];
            }

        }
    );

    for (var key in this.services) {
        this.services[key].refresh();
    }

}


/*Provider.prototype.expandtree = function() {
 this.expand = !this.expand;

 if (!this.expand){
 this.expandCell.innerText = '+';
 servkeys = Object.keys(this.services);
 evtkeys = Object.keys(this.events);

 for (var i = 0; i < servkeys.length; i++) {
 console.log(this.services);
 this.services[servkeys[i]].erase();
 delete this.services[servkeys[i]];
 }

 console.log(this.events);

 for (var i = 0; i < evtkeys.length; i++) {
 console.log(this.events[evtkeys[i]]);
 this.events[evtkeys[i]].erase();
 delete this.events[evtkeys[i]];
 }

 } else{
 this.expandCell.innerText = '-';
 this.refresh();
 }
 };*/

Provider.prototype.erase = function () {
    //console.log("Delete node");
    //providerDom.removeChild(this.node);
    for (var i in this.services) {
        this.services[i].erase();
    }
    for (var i in this.events) {
        this.events[i].erase();
    }
};

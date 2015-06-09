function Provider(name, sessionkey) {
    this.name = name;

    var caller = this; //Faire avec les problèmes de namespace...

    this.services = {};
    this.events = {};

    this.listnode = $('<option>', {value: sessionkey, text: this.name}).appendTo($('.provider-select'));

    setTimeout(function () {
        caller.refreshReadings();
    }, 500);
}

Provider.prototype.refreshReadings = function () {
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
                    provider.services[services[i]] = new ServiceNode(provider, services[i]);
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
        this.services[key].refreshReadings();
    }
    for (var key in this.events) {
        this.events[key].refreshReadings();
    }
};

Provider.prototype.erase = function () {
    //Effacer de façon propre l'objet à la déconnexion.
    for (var i in this.services) {
        this.services[i].erase();
    }
    for (var i in this.events) {
        this.events[i].erase();
    }
    this.listnode.remove();
};

Provider.prototype.configure = function(config) {
    //Envoie l'objet de configuration au provider.
    console.log(config)
    connection.session.call(this.name + ".configure", [config]);
    var caller = this;
    setTimeout(function(){
        for (var key in caller.services) {
            caller.services[key].refresh();
        }
        for (var key in caller.events) {
            caller.events[key].refresh();
        }
    },500);
}
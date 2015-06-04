function Provider(name) {
    this.name = name;

    var caller = this; //Faire avec les problèmes de namespace...

    this.services = {};
    this.events = {};

    setTimeout(function(){caller.refresh();},500);
}


Provider.prototype.refresh = function () {
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
        this.services[key].refreshReadings();
    }

};

Provider.prototype.erase = function () {
    for (var i in this.services) {
        this.services[i].erase();
    }
    for (var i in this.events) {
        this.events[i].erase();
    }
};

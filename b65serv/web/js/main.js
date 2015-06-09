//Au chargement de la page, paramétrer les variables globales.
$(function () {
        servicesNode = $('#services');
        serviceEditNode = $('#service-edit');
        eventsNode = $('#events');
        eventEditNode = $('#event-edit');

        connection = getConnection();
        connection.open();
    }
);


function refresh() {
    if (connection.session != null) {
        connection.session.call("wamp.session.list").then(function (data) {
            var toRemove = Object.keys(providers);
            for (var i = 0; i < data.length; i++) {
                if (data[i] in providers)
                    toRemove.splice(toRemove.indexOf(data[i]), 1);
                else
                    addProvider(data[i]);
            }
            for (var i = 0; i < toRemove.length; i++)
                delProvider([toRemove[i]]);
        }, connection.session.log);


        for (var i in providers) {
            providers[i].refreshReadings();
        }

        setTimeout(refresh, 250);
    }
}

//Ajoute un noeud fournisseur de service
function addProvider(obj) {
    if (typeof obj == 'number') { //Chercher l'objet session au complet si on ne reçoit que la clé
        connection.session.call("wamp.session.get", [obj]).then(function (data) {
            addProvider([data]);
        }, connection.session.log);
    }
    else { //Créer un objet provider correspondant aux informations reçues
        for (var i = 0; i < obj.length; i++)
            if (obj[i].authrole == "provider") { // Vérifier que le client connecté n'est pas une autre page web
                var hostname = obj[i].transport.http_headers_received.hostname;
                providers[obj[i].session] = new Provider(hostname, obj[i].session);
            }
    }
}

//Efface un noeud fournisseur de service
function delProvider(key) {
    for (var i = 0; i < key.length; i++) {
        if (key[i] in providers) {
            providers[key[i]].erase();
            delete providers[key[i]];
        }
    }
}


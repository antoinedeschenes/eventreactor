//Au chargement de la page, paramétrer les variables globales.
$(function () {
        //Créer les références sur les objets souvent utilisés.
        servicesNode = $('#services');
        serviceEditNode = $('#service-edit');
        eventsNode = $('#events');
        eventEditNode = $('#event-edit');

        //Créer une connexion et ouvrir.
        connection = getConnection();
        connection.open();
    }
);

//Boucle de rafraîchissement
function refresh() {
    if (connection.session != null) { //Si connecté
        //Demander au serveur la liste de clients connectés
        connection.session.call("wamp.session.list").then(function (data) {
            //Faire l'ajout et la suppression de providers selon la liste reçue.
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

        //Rafraîchir les lectures des providers existants.
        for (var i in providers) {
            providers[i].refresh();
        }

        //Planifier un rappel à la fonction.
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


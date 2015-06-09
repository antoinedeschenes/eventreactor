
//Génère et paramètre un objet connection.
function getConnection() {
    var connection = new autobahn.Connection({
        url: connectionurl,
        realm: "realm1",
        authmethods: ["wampcra"],
        authid: "manager",
        onchallenge: onchallenge
    });
    connection.onopen = onopen;
    return connection;
}

//Retourner le mot de passe pour l'authentification
function onchallenge(session, method, extra) {
    return autobahn.auth_cra.sign("secret", extra.challenge);
}

//Connexion réussie
function onopen(session, details) {
    //Ajouter des inscriptions aux méthodes qui publient l'ajout et la suppression de clients au serveur
    session.subscribe('wamp.session.on_join', addProvider);
    session.subscribe('wamp.session.on_leave', delProvider);
    //Démarrer la boucle
    refresh();
}


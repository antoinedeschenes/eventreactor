var wsuri = "ws://a.antoinedeschenes.com:8080/ws";

var providers = {};

var providerDom;

var servicesNode;
var eventsNode;

var connection;

var t2;


function diff(old, data) {
    var oldKeys = Object.keys(old);

    for (i in data){};

}

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
            providers[i].refresh();
        }

        setTimeout(refresh, 4000);
    }
}

function addProvider(obj) {
    if (typeof obj == 'number') {
        connection.session.call("wamp.session.get", [obj]).then(function (data) {
            addProvider([data]);
        }, connection.session.log);
    }
    else {
        for (var i = 0; i < obj.length; i++)
            if (obj[i].authrole == "provider")
                providers[obj[i].session] = new Provider(obj[i].transport.http_headers_received.hostname);
    }
}

function delProvider(key) {
    for (var i = 0; i < key.length; i++) {
        if (key[i] in providers) {
            providers[key[i]].erase();
            delete providers[key[i]];
        }
    }
}

//Retourner le mot de passe pour l'authentification
function onchallenge(session, method, extra) {
    //if (method === "wampcra")
    console.log("challenge accepted");
    return autobahn.auth_cra.sign("secret", extra.challenge);
};

function onopen(session, details) {
    console.log("Connected");

    function checksession(data) {
        for (var i = 0; i < data.length; i++)
            session.call("wamp.session.get", [data[i]]).then(session.log, session.log);
    }

    session.subscribe('wamp.session.on_join', addProvider);
    session.subscribe('wamp.session.on_leave', delProvider);

    refresh();
};

function onclose(reason, details) {
    console.log("Connection lost: " + reason);
    if (t2) {
        clearInterval(t2);
        t2 = null;
    }
};


//Onload
$(function () {
        console.log("hi");

        //providerDom = document.getElementById("providers");
        servicesNode = $('#services');
        eventsNode = $('#events');

        connection = new autobahn.Connection({
            url: wsuri,
            realm: "realm1",
            authmethods: ["wampcra"],
            authid: "manager",
            onchallenge: onchallenge
        });
        connection.onclose = onclose;
        connection.onopen = onopen;
        connection.open();
    }
);

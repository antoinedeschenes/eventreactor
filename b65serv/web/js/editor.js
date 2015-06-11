
//Remplir la liste de choix d'événements ou de services selon le cas.
function selectProvider(e) {
    var source = e.target.id;
    var selectedvalue = e.target.value;
    var datalist = undefined;
    var list = [];
    if (source == "service-provider-select") {
        if (selectedvalue.length > 0)
            list = Object.keys(providers[selectedvalue].services);
        datalist = $('#service-datalist');
    }
    else if (source == "event-provider-select") {
        if (selectedvalue.length > 0)
            list = Object.keys(providers[selectedvalue].events);
        datalist = $('#event-datalist');
    }

    datalist.empty();
    for (var i in list)
        $('<option>', {text: list[i]}).appendTo(datalist);
}

//Charger un service existant dans l'éditeur
function selectService() {
    var selectedprovider = $('#service-provider-select').val();
    var selectedservice = $('#service-name-input').val();
    if (selectedprovider.length > 0 && selectedservice in providers[selectedprovider].services) {
        providers[selectedprovider].services[selectedservice].getServiceConfiguration();
    }
}

//Afficher les boîtes appropriées selon le type de service dans l'éditeur de services.
function selectServiceType() {
    var selectedservicetype = $('#service-type-select').val();
    var listofconfigs = serviceconfigvalues[selectedservicetype];
    var configlist = $('#service-config-list');
    configlist.empty();
    for (var key in listofconfigs) {
        var listitem = $('<li>', {text: key + ":"}).appendTo(configlist)
        var type = listofconfigs[key].type;
        if (type == "enum") {
            var inputnode = $('<select>', {id: key}).appendTo(listitem);

            for (value in listofconfigs[key].values) {
                var value = listofconfigs[key].values[value];
                if (key in configstrings)
                    $('<option>', {value: value, text: configstrings[key][value]}).appendTo(inputnode);
                else
                    $('<option>', {text: value}).appendTo(inputnode);
            }
        } else if (type == "range") {
            $('<input>', {
                id: key,
                type: "number",
                min: listofconfigs[key].min,
                max: listofconfigs[key].max
            }).appendTo(listitem);
        } else if (type == "text") {
            $('<input>', {id: key, type: "text"}).appendTo(listitem);
        }
    }
}

//Remplir la condition d'événement et la liste des réactions dans l'éditeur d'événements
function selectEvent() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val();
    if (selectedprovider.length > 0 && selectedevent in providers[selectedprovider].events) {
        providers[selectedprovider].events[selectedevent].getEventConfiguration();
    }
}

//Choisir une réaction vraie et envoyer la valeur dans la boîte input si elle existe déjà
function selectTrueReaction() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val();
    var selectedtruereaction = $('#true-attribute').val();
    if (selectedprovider.length > 0 && selectedevent in providers[selectedprovider].events) {
        providers[selectedprovider].events[selectedevent].getTrueReactionValue(selectedtruereaction);
    }
}

//Choisir une réaction fausse et envoyer la valeur dans la boîte input si elle existe déjà
function selectFalseReaction() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val();
    var selectedfalsereaction = $('#false-attribute').val();
    if (selectedprovider.length > 0 && selectedevent in providers[selectedprovider].events) {
        providers[selectedprovider].events[selectedevent].getFalseReactionValue(selectedfalsereaction);
    }
}

//Vider l'éditeur de services
function clearServiceEditor() {
    $('#service-provider-select').val('');
    $('#service-name-input').val('');
    $('#service-type-select').val('');
    $('#service-datalist').empty();
    $('#service-config-list').empty();
    $('#service-value-list').empty();
}

//Vider l'éditeur d'événements
function clearEventEditor() {
    $('#event-provider-select').val('');
    $('#event-name-input').val('');
    $('#event-condition-input').val('');
    $('#event-datalist').empty();
    $('#event-true-reactions').empty();
    $('#true-attribute').val('');
    $('#true-value').val('');
    $('#event-false-reactions').empty();
    $('#false-attribute').val('');
    $('#false-value').val('');
}

//Envoyer une config de service
function saveService() {
    var selectedprovider = $('#service-provider-select').val();
    var selectedservice = $('#service-name-input').val().trim().toLowerCase().replace(/[^a-z0-9]/g, '');
    var selectedservicetype = parseInt($('#service-type-select').val());

    if (selectedprovider.length > 0 && selectedservice.length > 0 && selectedservicetype > 0) {
        var configtosend = {services: {}};
        configtosend.services[selectedservice] = {type: selectedservicetype};

        var confattributelist = Object.keys(serviceconfigvalues[selectedservicetype]);
        for (var i in confattributelist) {
            var attribute = confattributelist[i];
            var value = convertString($('#' + attribute).val());
            configtosend.services[selectedservice][attribute] = value;
        }

        providers[selectedprovider].configure(configtosend);
    }

}

//Envoyer une config de réaction d'événement
function saveCondition() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val().trim().toLowerCase().replace(/[^a-z0-9]/g, '');
    var newcondition = convertString($('#event-condition-input').val());

    if (selectedprovider.length > 0 && selectedevent.length > 0 && newcondition != null) {
        var configtosend = {events: {}};
        configtosend.events[selectedevent] = {condition: newcondition};
        providers[selectedprovider].configure(configtosend);
    }
    selectEvent();
}

//Envoyer une config de réaction sur événement de condition vraie
function saveTrueReaction() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val().trim().toLowerCase().replace(/[^a-z0-9]/g, '');
    var selectedattribute = $('#true-attribute').val().trim().replace(/[^A-Za-z0-9.\-]/g, '');
    var newvalue = convertString($('#true-value').val());

    if (selectedprovider.length > 0 && selectedevent.length > 0 && selectedattribute.length > 0) {
        var configtosend = {events: {}};
        configtosend.events[selectedevent] = {onTrue: {}};
        configtosend.events[selectedevent].onTrue[selectedattribute] = newvalue;
        providers[selectedprovider].configure(configtosend);
    }
    selectEvent();
}

//Envoyer une config de réaction sur événement de condition fausse
function saveFalseReaction() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val().trim().toLowerCase().replace(/[^a-z0-9]/g, '');
    var selectedattribute = $('#false-attribute').val().trim().replace(/[^A-Za-z0-9.\-]/g, '');
    var newvalue = convertString($('#false-value').val());

    if (selectedprovider.length > 0 && selectedevent.length > 0 && selectedattribute.length > 0) {
        var configtosend = {events: {}};
        configtosend.events[selectedevent] = {onFalse: {}};
        configtosend.events[selectedevent].onFalse[selectedattribute] = newvalue;
        providers[selectedprovider].configure(configtosend);
    }
    selectEvent();
}

//Transformer les strings lus en DOM en nombres s'ils contiennent que des nombres
function convertString(value) {
    if (typeof value == 'string')
        value = value.trim();
    if (value.length == 0)
        value = null;
    if ($.isNumeric(value))
        value = Number(value);
    return value;
}
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

function selectService() {
    var selectedprovider = $('#service-provider-select').val();
    var selectedservice = $('#service-name-input').val();
    if (selectedprovider.length > 0 && selectedservice in providers[selectedprovider].services) {
        providers[selectedprovider].services[selectedservice].getServiceConfiguration();
    }
}

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

function selectEvent() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val();
    if (selectedprovider.length > 0 && selectedevent in providers[selectedprovider].events) {
        providers[selectedprovider].events[selectedevent].getEventConfiguration();
    }
}

function selectTrueReaction() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val();
    var selectedtruereaction = $('#true-attribute').val();
    if (selectedprovider.length > 0 && selectedevent in providers[selectedprovider].events) {
        providers[selectedprovider].events[selectedevent].getTrueReactionValue(selectedtruereaction);
    }
}

function selectFalseReaction() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val();
    var selectedfalsereaction = $('#false-attribute').val();
    if (selectedprovider.length > 0 && selectedevent in providers[selectedprovider].events) {
        providers[selectedprovider].events[selectedevent].getFalseReactionValue(selectedfalsereaction);
    }
}

function clearServiceEditor() {
    $('#service-provider-select').val('');
    $('#service-name-input').val('');
    $('#service-type-select').val('');
    $('#service-datalist').empty();
    $('#service-config-list').empty();
    $('#service-value-list').empty();
}

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

function saveCondition() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val().trim().toLowerCase().replace(/[^a-z0-9]/g, '');
    var newcondition = convertString($('#event-condition-input').val());

    if (selectedprovider.length > 0 && selectedevent.length > 0 && newcondition != null) {
        var configtosend = {events: {}};
        configtosend.events[selectedevent] = {condition: newcondition};
        providers[selectedprovider].configure(configtosend);
    }
}


function saveTrueReaction() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val().trim().toLowerCase().replace(/[^a-z0-9]/g, '');
    var selectedattribute = $('#true-attribute').val().trim().toLowerCase().replace(/[^a-z0-9.]/g, '');
    var newvalue = convertString($('#true-value').val());

    if (selectedprovider.length > 0 && selectedevent.length > 0 && selectedattribute.length > 0) {
        var configtosend = {events: {}};
        configtosend.events[selectedevent] = {onTrue: {}};
        configtosend.events[selectedevent].onTrue[selectedattribute] = newvalue;
        providers[selectedprovider].configure(configtosend);
    }
}

function saveFalseReaction() {
    var selectedprovider = $('#event-provider-select').val();
    var selectedevent = $('#event-name-input').val().trim().toLowerCase().replace(/[^a-z0-9]/g, '');
    var selectedattribute = $('#false-attribute').val().trim().toLowerCase().replace(/[^a-z0-9.]/g, '');
    var newvalue = convertString($('#false-value').val());

    if (selectedprovider.length > 0 && selectedevent.length > 0 && selectedattribute.length > 0) {
        var configtosend = {events: {}};
        configtosend.events[selectedevent] = {onFalse: {}};
        configtosend.events[selectedevent].onFalse[selectedattribute] = newvalue;
        providers[selectedprovider].configure(configtosend);
    }
}


function convertString(value) {
    if (typeof value == 'string')
        value = value.trim();
    if (value.length == 0)
        value = null;
    if ($.isNumeric(value))
        value = Number(value);
    return value;
}
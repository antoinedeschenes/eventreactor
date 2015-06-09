AUTOBAHN_DEBUG = false;

var connectionurl = "ws://a.antoinedeschenes.com:8080/ws";

var providers = {};
var servicesNode;
var serviceEditNode;
var eventsNode;
var eventEditNode;

var connection;

var configstrings = {
    type: {
        1: 'i/o pin',
        2: 'thermometer',
        3: 'thermoelectric plate',
        4: 'time',
        5: 'variable'
    },
    mode: {
        I: 'input',
        O: 'output'
    },
    sensorType: {
        0: 'mcp9808 (direct)',
        1: 'tmp007 (ir)'
    }
};

var suffixdict = {
    temp: "°C",
    power: "W",
    voltage: "V",
    current: "A",
    duty: "%",
    time: "s"
};

var serviceconfigvalues = {
    1: {
        pin: {type:"enum", values:[5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]},
        mode: {type:"enum", values:['I', 'O']}
    },
    2: {
        sensorType: {type:"enum", values:[0, 1]},
        address: {type:"range", min:0, max:127}
    },
    3: {
        max_current: {type:"enum", values:[8.5]},
        max_voltage: {type:"enum", values:[14.0]}
    },
    4: {},
    5: {
        initial: {type:"text"}
    }
};
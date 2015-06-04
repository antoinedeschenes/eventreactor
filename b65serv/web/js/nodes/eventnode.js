/**
 * Created by Antoine on 2015-04-04.
 */
function EventNode(parent, name) {
    this.parent = parent;
    this.name = name;
    this.node = $('<tr>').appendTo(eventsNode);
    $('<td>').text(parent.name + '.' + name).appendTo(this.node);

    this.conditiontd = $('<td>').appendTo(this.node);
    var reactiontd = $('<td>').appendTo(this.node);
    $('<h4>').text('On True:').appendTo(reactiontd);
    this.ontruenode = $('<ul>').appendTo(reactiontd);
    $('<h4>').text('On False:').appendTo(reactiontd);
    this.onfalsenode = $('<ul>').appendTo(reactiontd);

    this.refresh();
};

EventNode.prototype.refresh = function () {
    var caller = this;
    connection.session.call(this.parent.name + ".evt." + this.name).then(function(data) {

        caller.conditiontd.text(data.condition);

        caller.ontruenode.empty();
        caller.onfalsenode.empty();

        for (var key in data.onTrue){
            $('<li>').text(key + ":" + data.onTrue[key]).appendTo(caller.ontruenode);
        }
        for (var key in data.onFalse){
            $('<li>').text(key + ":" + data.onFalse[key]).appendTo(caller.onfalsenode);
        }
    });
};

EventNode.prototype.erase = function() {
    this.node.remove();
    this.node = undefined;
};
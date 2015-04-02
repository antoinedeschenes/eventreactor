function Provider(name) {
    console.log(name);
    this.name = name;
    this.node = document.createElement("li");
    this.node.appendChild(document.createTextNode(this.name));
    providerDom.appendChild(this.node);
}

Provider.prototype.update = function () {

}

Provider.prototype.removeNode = function () {
    console.log("Delete node");
    providerDom.removeChild(this.node);
}

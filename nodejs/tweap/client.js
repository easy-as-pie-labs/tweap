if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {
    function Client(username, socket) {
        this.username = username;
        this.socket = socket;
        this.connected = true;
        this.authenticated = false;
        this.authToken = undefined;
    }

    return Client;

});
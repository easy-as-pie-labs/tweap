if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {

    function ClientManager() {

        var clients = [];

        this.addClient = function (client) {
            clients.push(client);
            this.showClients();
        };

        this.removeClient = function (client) {
            var index = clients.indexOf(client);
            if (index > -1) {
                clients.splice(index, 1);
                console.log("removed client: " + client.username);
            }
        };

        this.getClientByUsername = function (username, connected) {
            for (var client of clients) {
                if (client.username === username) {
                    if (connected == client.connected || connected == undefined) {
                        return client;
                    }
                }
            }
            return false;
        };

        this.getClientBySocket = function (socket) {
            for (var client of clients) {
                if (client.socket === socket) {
                    return client;
                }
            }
            return false;
        };


        this.showClients = function () {
            console.log(".-------------------------------------------------.");
            console.log("| Clients: " + clients.length + "\t\t\t\t\t  |");
            console.log("|-------------------------------------------------|\n" +
                        "| Username\tSocket\t\t\tconnected |\n" +
                        "|-------------------------------------------------|");
            for (var client of clients) {
                console.log("| " + client.username + "\t\t" + client.socket.id + "\t" + client.connected + "\t  |");
            }
            console.log("|_________________________________________________|");
        };
    }

    return ClientManager;

});

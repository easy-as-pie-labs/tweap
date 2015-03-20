if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {

    function ClientManager() {

        var clients = [];

        this.addClient = function (client) {
            clients.push(client);
            /*
            //add client to conversation rooms
            for (var conversation of getConversationsOfUser(client.username)) {
                client.socket.join(conversation);
            }
            */
        };

        this.removeClient = function (client) {
            var index = clients.indexOf(client);
            if (index > -1) {
                clients.splice(index, 1);
            }
        };

        this.getClientByUsername = function (username) {
            for (var client of
            clients
            )
            {
                if (client.username === username) {
                    return client;
                }
            }
            return false;
        };

        this.getClientBySocket = function (socket) {
            for (var client of
            clients
            )
            {
                if (client.socket === socket) {
                    return client;
                }
            }
            return false;
        };


        this.showClients = function () {
            console.log("\nClients");
            console.log("|------------------------------------------|\n" +
                        "|Username\tSocket\t\tconnected? |\n" +
                        "|------------------------------------------|");
            for (var client of clients) {
                console.log("|" + client.username + "\t\t" + client.socket.id + "\t" + client.connected + "   \t|");
            }
            console.log("|__________________________________________|");
        };
    }

    return ClientManager;

});
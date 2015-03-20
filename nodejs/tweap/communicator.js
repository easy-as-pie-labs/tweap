if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {

    var Client = require('./client.js');

    // this object is only for development and must be replaced by an api to tweap-django!
    var tweap = {
        checkCredentials: function(username, password) {
            return true;
        },
        addMessage: function(message) {
            return true;
        },
        getOrAddConversation: function(userlist) {
            return {'id': 123, 'users': ['tpei', 'shonyyyy', 'googlez', 'jawu']}
        }
    };

    function Communicator(socket, clientManager, io) {
        this.socket = socket;
        this.clientManager = clientManager;
        this.io = io;
        this.client = undefined;

        this.socket.on('auth', function(data) {
            this.authenticate(data)
        });

        this.socket.on('re-auth', function(data) {
            this.reAuthenticate(data)
        });

        this.socket.on('disconnect', function() {
            this.disconnect()
        });

        this.socket.on('message', function(data) {
            this.spreadMessage(data)
        });

        this.socket.on('conversation-request', function(data) {
            this.handleConversation(data)
        });

        // online / offline state requests
    }

    Communicator.prototype.authenticate = function(credentials) {
        if (this.clientManager.getClientBySocket(this.socket)) {
            return;
        }
        if (!tweap.checkCredentials(credentials.username, credentials.password)) {
            //maybe error message to client
            this.socket.disconnect();
            return;
        }

        this.client = new Client(credentials.username, this.socket);
        this.clientManager.addClient(this.client);
    };

    Communicator.prototype.reAuthenticate = function(credentials) {
        this.client = this.clientManager.getClientByUsername(credentials.username);
        if (this.client && !this.client.connected && credentials.reAuthToken == this.client.reAuthToken) {
            this.client.connected = true;
            this.client.socket = this.socket;
        } else {
            //maybe error message to client
            this.socket.disconnect();
        }
    };

    Communicator.prototype.disconnect = function() {
        if (this.client) {
            this.client.connected = false;
        }
    };

    Communicator.prototype.spreadMessage = function(message) {
        if (!this.client) {
            //maybe error message to client
            return;
        } else {
            //check if user is in that room
            message.sender = this.client.username;
            message.timestamp = Date.now();
            this.io.to(message.conversation).emit('message', message);
            tweap.addMessage(message);
        }
    };

    Communicator.prototype.handleConversation = function(userlist) {
        if (!this.client) {
            //maybe error message to client
            return;
        } else {
            var conversation = tweap.getOrAddConversation(userlist.users)
            for (var username of conversation.users) {
                var userClient = this.clientManager.getClientByUsername(username);
                if (userClient) {
                    userClient.socket.join(conversation.id);
                }
            }
            this.socket.emit('conversation-response', conversation);
        }
    };

    return Communicator;

});
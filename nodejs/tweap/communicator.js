if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {

    var Client = require('./client.js');
    var crypto = require('crypto');

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
        },
        getConversationsOfUser: function(username) {
            return ["1234", "432", "1243"];
        }
    };

    function Communicator(socket, clientManager, io) {
        this.socket = socket;
        this.clientManager = clientManager;
        this.io = io;
        this.client = undefined;

        var that = this;

        this.socket.on('auth', function(data) {
            that.authenticate(data)
        });

        this.socket.on('re-auth', function(data) {
            that.reAuthenticate(data)
        });

        this.socket.on('disconnect', function() {
            that.disconnect()
        });

        this.socket.on('message', function(data) {
            that.spreadMessage(data)
        });

        this.socket.on('conversation-request', function(data) {
            that.handleConversation(data)
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
        this.newAuthToken();
        this.addToConversations();
    };

    Communicator.prototype.reAuthenticate = function(credentials) {
        this.client = this.clientManager.getClientByUsername(credentials.username);
        if (this.client && !this.client.connected && (credentials.reAuthToken === this.client.authToken)) {
            this.client.connected = true;
            this.client.socket = this.socket;
            this.newAuthToken();
            this.addToConversations();
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
        if (this.client && (this.socket.rooms.indexOf(message.conversation) !== -1)) {
            message.sender = this.client.username;
            message.timestamp = Date.now();
            this.io.to(message.conversation).emit('message', message);
            tweap.addMessage(message);
        }
    };

    Communicator.prototype.handleConversation = function(userlist) {
        if (this.client) {
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


    /* Tools */

    Communicator.prototype.newAuthToken = function() {
        if (this.client) {
            var hash = (Date.now() * Math.random()) + " ~ " + this.client.username;
            this.client.authToken = crypto.createHash('md5').update(hash).digest('hex');
            this.socket.emit('auth-success', {'token': this.client.authToken});
        }
    };

    Communicator.prototype.addToConversations = function() {
        if (this.client) {
            for (var conversation of tweap.getConversationsOfUser(this.client.username)) {
                this.client.socket.join(conversation);
            }
        }
    };

    return Communicator;

});
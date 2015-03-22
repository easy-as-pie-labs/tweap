if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {

    var Client = require('./client.js');
    var crypto = require('crypto');
    var tweap = require('./tweap-interface.js');

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

        this.socket.on('get-messages', function(data) {
            that.loadMessages(data);
        });

        //test stuff remove later!
        this.socket.on('test', function(data) {
            tweap.makeRequest(JSON.parse(data));
        });
    }

    Communicator.prototype.authenticate = function(credentials) {
        if (this.clientManager.getClientBySocket(this.socket)) {
            return;
        }
        if (!tweap.checkCredentials(credentials.username, credentials.password)) {
            this.socket.disconnect();
            return;
        }

        this.client = new Client(credentials.username, this.socket);
        this.clientManager.addClient(this.client);
        this.generateNewAuthToken();
        this.addToConversations();
    };

    Communicator.prototype.reAuthenticate = function(credentials) {
        this.client = this.clientManager.getClientByUsername(credentials.username, false);
        if (this.client) {
            if (!this.client.connected && (credentials.authToken === this.client.authToken)) {
                this.client.connected = true;
                this.client.socket = this.socket;
                this.generateNewAuthToken();
                this.addToConversations();
                return;
            }
        } else {
            for (var authToken of tweap.getAuthTokensForUser(credentials.username)) {
                if (credentials.authToken === authToken) {
                    this.client = new Client(credentials.username, this.socket);
                    this.clientManager.addClient(this.client);
                    this.generateNewAuthToken();
                    this.addToConversations();
                    return;
                }
            }
        }
        this.socket.disconnect();
    };

    Communicator.prototype.disconnect = function() {
        if (this.client) {
            this.client.connected = false;
            setTimeout(function() {
                if (!this.client.connected) {
                    this.clientManager.removeClient(this.client);
                }
            }.bind(this), 10000);
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

    Communicator.prototype.loadMessages = function(messageRequest) {
        if (this.client && (this.socket.rooms.indexOf(messageRequest.conversation) !== -1)) {
            return tweap.getMessages(messageRequest);
        }
    }


    /* Tools */

    Communicator.prototype.generateNewAuthToken = function() {
        if (this.client) {
            var oldAuthToken = this.client.authToken;
            var hash = (Date.now() * Math.random()) + " ~ " + this.client.username;
            this.client.authToken = crypto.createHash('md5').update(hash).digest('hex');
            tweap.updateAuthToken(this.client.username, this.client.authToken, oldAuthToken);
            this.socket.emit('auth-success', {'authToken': this.client.authToken});
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

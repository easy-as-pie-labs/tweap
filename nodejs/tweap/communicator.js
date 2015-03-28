if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {

    var Client = require('./client.js');
    var crypto = require('crypto');
    var najax = require('../libs/najax.js');

    var tweapUrl = "http://127.0.0.1:8000/chat/api/";

    function Communicator(socket, clientManager, io) {
        this.socket = socket;
        this.clientManager = clientManager;
        this.io = io;
        this.client = undefined;

        var that = this;

        this.socket.on('auth-status', function() {
            that.sendAuthStatus();
        })

        this.socket.on('auth', function(data) {
            that.authenticate(data);
        });

        this.socket.on('re-auth', function(data) {
            that.reAuthenticate(data);
        });

        this.socket.on('disconnect', function() {
            that.disconnect();
        });

        this.socket.on('message', function(data) {
            that.spreadMessage(data);
        });

        this.socket.on('get-conversations', function() {
            that.conversationGetter();
        });

        this.socket.on('conversation-request', function(data) {
            that.conversationRequestHandler(data);
        });

        this.socket.on('get-messages', function(data) {
            that.loadMessages(data);
        });

    }

    Communicator.prototype.sendAuthStatus = function() {
        var status = "UNAUTHENTICATED";
        if (this.client) {
            if (this.client.connected) {
                status = "CONNECTED";
            } else {
                status = "DISCONNECTED";
            }
        }
        this.socket.emit('auth-status', {'status': status});
    };

    Communicator.prototype.authenticate = function(credentials) {
        if (this.clientManager.getClientBySocket(this.socket)) {
            return;
        }
        var data = {
            'action': 'checkCredentials',
            'username': credentials.username,
            'password': credentials.password
        };
        this.makeRequest(data, this.authenticateCB, this);
    };

    Communicator.prototype.authenticateCB = function(data) {
        if (data.status === "OK" && data.authResult === "OK") {
            this.client = new Client(data.username, this.socket);
            this.clientManager.addClient(this.client);
            this.generateNewAuthToken();
            this.addToConversations();
        } else {
            this.socket.disconnect();
            return;
        }
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
            var data = {
                'action': 'checkAuthToken',
                'username': credentials.username,
                'authToken': credentials.authToken
            };
            this.makeRequest(data, this.authenticateCB, this);
        }
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

            var data = {
                 'action': 'addMessage',
                 'message': message
             };
             this.makeRequest(data);
        }
    };

    Communicator.prototype.conversationGetter = function() {
        if (this.client) {
            var data = {
                'action': 'getConversationsOfUser',
                'username': this.client.username
            };
            this.makeRequest(data, this.conversationGetterCB, this);
        }
    };

    Communicator.prototype.conversationGetterCB = function(data) {
        if (data.status === "OK") {
            this.socket.emit('conversation-list', data.conversations);
        }
    }

    Communicator.prototype.conversationRequestHandler = function(userlist) {
        if (this.client) {
            var data = {
                'action': 'getOrAddConversation',
                'userlist': userlist
            };
            this.makeRequest(data, this.conversationRequestHandlerCB, this);
        }
    };

    Communicator.prototype.conversationRequestHandlerCB = function(data) {
        if (data.status === "OK") {
            for (var username of data.conversation.users) {
                var userClient = this.clientManager.getClientByUsername(username);
                if (userClient) {
                    userClient.socket.join(data.conversation.id);
                }
            }
            this.socket.emit('conversation-response', data.conversation);
        }
    };

    Communicator.prototype.loadMessages = function(messageRequest) {
        if (this.client && (this.socket.rooms.indexOf(messageRequest.conversation) !== -1)) {
            var data = {
                'action': 'getMessages',
                'conversation': messageRequest.conversation
            };
            if (messageRequest.messageId != undefined) {
                data.messageId = messageRequest.messageId;
            }
            this.makeRequest(data, this.loadMessagesCB, this);
        }
    };

    Communicator.prototype.loadMessagesCB = function(data) {
        if (data.status === "OK") {
            this.socket.emit('message-response', data.messages);
        }
    };


    /* Tools */

    Communicator.prototype.generateNewAuthToken = function() {
        if (this.client) {
            var oldAuthToken = this.client.authToken;
            var hash = (Date.now() * Math.random()) + " ~ " + this.client.username;
            this.client.authToken = crypto.createHash('md5').update(hash).digest('hex');
            this.socket.emit('auth-success', {'authToken': this.client.authToken});

            var data = {
                'action': 'updateAuthToken',
                'username': this.client.username,
                'newAuthToken': this.client.authToken,
                'oldAuthToken': oldAuthToken
            };
            this.makeRequest(data);
        }
    };

    Communicator.prototype.addToConversations = function() {
        if (this.client) {
            var data = {
                'action': 'getConversationsOfUser',
                'username': this.client.username
            };
            this.makeRequest(data, this.addToConversationsCB, this);
        }
    };

    Communicator.prototype.addToConversationsCB = function(data) {
        if (data.status === "OK") {
            for (var conversation of data.conversations) {
                this.client.socket.join(conversation);
            }
        }
    };

    Communicator.prototype.makeRequest = function(data, callback, communicator) {
         var dat = {};
         dat.request = JSON.stringify(data);

         najax({ url:tweapUrl, type:'POST', data:dat})
             .success(function(resp){
                 if (callback != undefined) {
                     callback.call(communicator, JSON.parse(resp));
                 }
             })
             .error(function(err){
                 console.log(err);
             });
     };

    return Communicator;

});
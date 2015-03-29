ChatManager = function() {
    var username;
    var currentConversation;
    var conversations = [];

    var socket = io('http://dev.tweap.easy-as-pie.de:3000');
    //var socket = io('http://127.0.0.1:3000');

    var that = this;

    /* METHODS FOR COMMUNICATION WITH SERVER */

    var authenticate = function() {
        username = JSON.parse(localStorage.getItem('chat-raw-credentials')).username;
        socket.emit('auth', JSON.parse(localStorage.getItem('chat-raw-credentials')));
    };

    var reAuthenticate = function() {
        username = JSON.parse(localStorage.getItem('chat-credentials')).username;
        socket.emit('re-auth', JSON.parse(localStorage.getItem('chat-credentials')));
    };

    this.sendMessage = function(text) {
        var message = {
            'conversation': currentConversation.id,
            'text': text
        };
        socket.emit('message', message);
    };

    this.requestConversation = function(users) {
        socket.emit('conversation-request', users);
    };

    this.getMessages = function(side) {
        if (side === 'oldest' || side === 'newest') {
            var messageRequest = {
                'side': side,
                'conversation': currentConversation.id,
                'messageId': currentConversation.getMessage(side).id
            };
            socket.emit('get-messages', messageRequest);
        }
    };

    this.requestConversations = function() {
        socket.emit('get-conversations');
    };



    /* METHODS FOR INTERACTING WITH GUI */

    this.changeConversation = function(conversationId) {
        currentConversation = findConversationById(conversationId);
        saveToStorage();
        if (currentConversation.messages.length === 0) {
            this.getMessages('oldest');
        } else {
            this.getMessages('newest');
        }
    };

    this.addConversation = function(conversationId, name) {
        if(!findConversationById(conversationId)) {
            conversations.push(new Conversation(conversationId, [username], name));
            this.changeConversation(conversationId);
        }
    };

    this.closeConversation = function(conversationId) {
        var index = findConversationById(conversationId, true);
        if (index) {
            conversations.splice(index, 1);
        }
        saveToStorage();
    };

    var showMessages = function() {
        chatUi.emptyConversation();
        for (var i = 0; i < currentConversation.messages.length; i++) {
            if (currentConversation.messages[i].sender === username) {
                chatUi.addOwnMessage(currentConversation.messages[i].text, currentConversation.messages[i].timestamp);
            } else {
                chatUi.addPartnerMessage(currentConversation.messages[i].text, currentConversation.messages[i].sender, currentConversation.messages[i].timestamp);
            }
        }
        chatUi.activateChat(currentConversation.id);
    };

    var findConversationById = function(conversationId, index) {
        for (var i = 0; i < conversations.length; i++) {
            if (conversations[i].id == conversationId) {
                if (index === true) {
                    return i;
                } else {
                    return conversations[i];
                }
            }
        }
        return false;
    };


    /* METHODS FOR STORING / LOADING FROM WEBSTORAGE */

    var loadFromStorage = function() {
        if (localStorage.getItem('chat-conversations') !== null) {
            try {
                var saveObject = JSON.parse(localStorage.getItem('chat-conversations'));
                for (var i = 0; i < saveObject.conversations.length; i++) {
                    conversations.push(new Conversation(saveObject.conversations[i].id, saveObject.conversations[i].users, saveObject.conversations[i].name));
                    conversations[conversations.length - 1].messages = saveObject.conversations[i].messages;
                }
                username = saveObject.username;
                currentConversation = findConversationById(saveObject.currentConversationId);
                that.changeConversation(currentConversation.id)
            } catch(err) {
                localStorage.removeItem('chat-conversations');
            }
        }
    };

    var saveToStorage = function() {
        var saveObject = {
            'username': username,
            'conversations': [],
            'currentConversationId': currentConversation.id
        };
        for (var i = 0; i < conversations.length; i++) {
            saveObject.conversations.push(conversations[i]);
        }
        localStorage.setItem('chat-conversations', JSON.stringify(saveObject));
    };


    /* HANDLER */


    socket.on('auth-success', function(data) {
        var chatCredentials = {
            'username': username,
            'authToken': data.authToken
        };
        localStorage.removeItem('chat-raw-credentials');
        localStorage.setItem('chat-credentials', JSON.stringify(chatCredentials));
    });

    socket.on('message', function(message) {
        var conversation = findConversationById(message.conversation);
        if (conversation) {
            conversation.addNewMessage(message);
        } else {
            conversation = new Conversation(message.conversation, [message.sender], message.sender);
            conversations.push(conversation);
            conversation.addNewMessage(message);
        }
        if (conversation === currentConversation) {
            if (message.sender === username) {
                chatUi.addOwnMessage(message.text, message.timestamp);
            } else {
                chatUi.addPartnerMessage(message.text,  message.sender, message.timestamp);
            }
        }
        saveToStorage();
    });

    socket.on('message-response', function(messages) {
        if (messages.length > 0) {
            var conversation = findConversationById(messages[0].conversation);
            if (conversation) {
                conversation.addMessages(messages);
                if (conversation === currentConversation) {
                    showMessages();
                }
            }
            saveToStorage();
        }
    });

    socket.on('conversation-list', function(conversations) {
        var projectConversations = [];
        var personConversations = [];
        for (var i = 0; i < conversations.length; i++) {
            if (conversations[i].name) {
                projectConversations.push(conversations[i]);
            } else {
                personConversations.push(conversations[i]);
            }
        }
        chatUi.addConversationsToOverview(projectConversations, personConversations);
    });

    socket.on('conversation-response', function(conversation) {
        var conversation = findConversationById(conversation.id);
        if (!conversation) {
            conversations.push(new Conversation(conversation.id, conversation.users, conversation.name));
        } else {
            conversation.addUsers(conversation.users);
            conversation.addName(conversation.name);
        }
        saveToStorage();
    });


    /* initial stuff */
    loadFromStorage();
    if (localStorage.getItem('chat-raw-credentials') === null) {
        reAuthenticate();
    } else if(localStorage.getItem('chat-credentials') === null) {
        authenticate();
    } else {
        console.log("No chat credentials please relogin!");
    }

};

function Conversation(id, users, name) {
    this.id = id;
    this.users = users;
    this.name = name;
    this.messages = [];

    if (this.name == null) {
        chatUi.addNewPersonChatButton(id, this.users);
    } else {
        chatUi.addNewGroupChatButton(id, name);
    }

    this.getMessage = function(side) {
        if (this.messages.length > 0) {
            if (side === 'oldest') {
               return this.messages[0];
            } else if (side === 'newest') {
                return this.messages[this.messages.length-1];
            }
        } else {
            return {'id': ''};
        }
    };

    this.addMessages = function(messages) {
        if (messages.length > 0) {
            if ((this.messages.length > 0) && (messages[0].id > this.messages[this.messages.length-1].id)) {
                for (var i = 0; i < messages.length; i++) {
                    this.messages.push(messages[i]);
                }
            } else {
                for (var i = 0; i < messages.length; i++) {
                    this.messages.unshift(messages[i]);
                }
            }
        }
    };

    this.addNewMessage = function(newMessage) {
        this.messages.push(newMessage);
    };

    this.addUsers = function(newUsers) {
        this.users = newUsers;
    };

    this.addName = function(name) {
        this.name = name;
    }
}
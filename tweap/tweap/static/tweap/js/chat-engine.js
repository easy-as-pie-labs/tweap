ChatManager = function() {
    var username;
    var currentConversation;
    var conversations = [];

    var socket = io('http://dev.tweap.easy-as-pie.de:3000');

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

    this.getMessages = function() {
        if (!currentConversation.allMessages) {
            var messageRequest = {
                'conversation': currentConversation.id,
                'direction': 'older',
                'messageTimeStamp': currentConversation.getOldestMessage().timestamp
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
        currentConversation.unreadMessages = 0;
        saveToStorage();
        if (currentConversation.messages.length === 0) {
            this.getMessages();
        } else {
            showMessages();
        }
    };

    this.addConversation = function(conversationId, name) {
        if(!findConversationById(conversationId)) {
            conversations.push(new Conversation(conversationId, [username], name));
        }
    };

    this.closeConversation = function(conversationId) {
        var index = findConversationById(conversationId, true);
        if (index) {
            conversations.splice(index, 1);
        }
        // TODO: check if here must be reset currentConversation
        // maybe splice doesn't work correctly
        saveToStorage();
    };

    var showMessages = function() {
        for (var i = 0; i < currentConversation.messages.length; i++) {
            if (currentConversation.messages[i].sender === username) {
                chatUi.addOwnMessage(currentConversation.messages[i].text, currentConversation.messages[i].timestamp);
            } else {
                chatUi.addPartnerMessage(currentConversation.messages[i].text, currentConversation.messages[i].sender, currentConversation.messages[i].timestamp);
            }
        }
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
                setTimeout(function() {
                    chatUi.activateChat(saveObject.currentConversationId);
                }, 10);
            } catch(err) { }
        }
    };

    var saveToStorage = function() {
        var saveObject = {
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
        if (!conversation) {
            conversation = new Conversation(message.conversation, [message.sender], message.sender);
            conversations.push(conversation);
        }
        conversation.addNewMessage(message);
        if (message.sender != username) {
            chatUi.showChatButtonBadge(conversation.id, ++conversation.unreadMessages);
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
                for (var i = 0; i < messages.length; i++) {
                    conversation.addOldMessage(messages[i]);
                    if (messages[i].sender === username) {
                        chatUi.addOwnMessage(messages[i].text, messages[i].timestamp, 'top');
                    } else {
                        chatUi.addPartnerMessage(messages[i].text,  messages[i].sender, messages[i].timestamp, 'top');
                    }
                }
            }
            saveToStorage();
        } else {
            currentConversation.allMessages = true;
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
}

function Conversation(id, users, name) {
    this.id = id;
    this.users = users;
    this.name = name;
    this.messages = [];
    this.unreadMessages = 0;
    this.allMessages = false;

    if (this.name == null) {
        chatUi.addNewPersonChatButton(id, name);
    } else {
        chatUi.addNewGroupChatButton(id, name);
    }

    this.getOldestMessage = function() {
        if (this.messages.length > 0) {
            return this.messages[0];
        } else {
            return {'timestamp': ''};
        }
    };

    this.addNewMessage = function(newMessage) {
        this.messages.push(newMessage);
    };

    this.addOldMessage = function(oldMessage) {
        this.messages.unshift(oldMessage);
    };

    this.addUsers = function(newUsers) {
        this.users = newUsers;
    };

    this.addName = function(name) {
        this.name = name;
    };
}
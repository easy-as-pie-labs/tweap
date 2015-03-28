ChatManager = function() {
    var username;
    var currentConversation;
    var conversations = [];

    var socket = io('http://dev.tweap.easy-as-pie.de:3000');

    var that = this;

    /* METHODS FOR COMMUNICATION WITH SERVER */

    var getAuthStatus = function() {
        socket.emit('auth-status');
    };

    var authenticate = function(username, password) {
        socket.emit('auth', {'username': 'jawu', 'password': 'test'});
    };

    var reAuthenticate = function() {
        /*
        var fakeCreds = {
            'username': 'jawu',
            'authToken': 'a8d48d3ff5a205fb0da5481940d63b63'
        };
        localStorage.setItem('chat-creds', JSON.stringify(fakeCreds));
        */

        socket.emit('re-auth', JSON.parse(localStorage.getItem('chat-creds')));
        username = JSON.parse(localStorage.getItem('chat-creds')).username;
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

    this.getOldMessages = function() {
        var messageRequest = {
            'conversation': currentConversation.id,
            'messageId': currentConversation.getOldestMessage().id
        };
        socket.emit('get-messages', messageRequest);
    };

    this.requestConversations = function() {
        socket.emit('get-conversations');
    };



    /* METHODS FOR INTERACTING WITH GUI */

    this.changeConversation = function(conversationId) {
        currentConversation = findConversationById(conversationId);
        saveToStorage();
        if (currentConversation.messages.length === 0) {
            this.getOldMessages();
        } else {
            showMessages();
        }
    };

    this.addConversation = function(conversationId, name) {
        conversations.push(new Conversation(conversationId, [username], name));
        this.changeConversation(conversationId);
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
        if (localStorage.getItem('chat_conversations') !== null) {
            var saveObject = JSON.parse(localStorage.getItem('chat_conversations'));
            for (var i = 0; i < saveObject.conversations.length; i++) {
                conversations.push(new Conversation(saveObject.conversations[i].id, saveObject.conversations[i].users, saveObject.conversations[i].name));
                conversations[conversations.length-1].messages = saveObject.conversations[i].messages;
            }
            username = saveObject.username;
            currentConversation = findConversationById(saveObject.currentConversationId);
            that.changeConversation(currentConversation.id)
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
        localStorage.setItem('chat_conversations', JSON.stringify(saveObject));
    };


    /* HANDLER */

    socket.on('auth-status', function(data) {
        console.log("current auth status: " + data.status);
        if (data.status === "UNAUTHENTICATED") {
            reAuthenticate();
        }
    });

    socket.on('auth-success', function(data) {
        console.log("auth-success");
        var chatCreds = JSON.parse(localStorage.getItem('chat-creds'));
        chatCreds.authToken = data.authToken;
        localStorage.setItem('chat-creds', JSON.stringify(chatCreds));
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
                conversation.addOldMessages(messages);
                if (conversation === currentConversation) {
                    showMessages();
                }
            }
        }
        saveToStorage();
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
    getAuthStatus();

}

function Conversation(id, users, name) {
    this.id = id;
    this.users = users;
    this.name = name;
    this.messages = [];

    console.log(this.name);
    if (this.name == null) {
        chatUi.addNewPersonChatButton(id, this.users);
    } else {
        chatUi.addNewGroupChatButton(id, name);
    }


    this.getOldestMessage = function() {
        if (this.messages.length > 0) {
            return this.messages[0];
        } else {
            return {'id': ''};
        }
    };

    this.getMessages = function() {
        return this.messages;
    };

    this.addOldMessages = function(oldMessages) {
        for (var i = 0; i < oldMessages.length; i++) {
            this.messages.unshift(oldMessages[i]);
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
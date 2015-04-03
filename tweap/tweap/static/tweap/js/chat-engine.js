var GROUP_TYPE = "group";

ChatManager = function() {
    var username;
    var currentConversation;
    var conversations = [];

    var socket = io('http://dev.tweap.easy-as-pie.de:3000');
    //var socket = io('http://127.0.0.1:3000');

    var self = this;

    /* METHODS FOR COMMUNICATION WITH SERVER */

    var authenticate = function() {
        username = JSON.parse(localStorage.getItem('chat-raw-credentials')).username;
        socket.emit('auth', JSON.parse(localStorage.getItem('chat-raw-credentials')));
    };

    var reAuthenticate = function() {
        username = JSON.parse(localStorage.getItem('chat-credentials')).username;
        socket.emit('re-auth', JSON.parse(localStorage.getItem('chat-credentials')));
    };

    var getConversationInfo = function(conversationId) {
        var conversationInfoRequest = {
            'conversation': conversationId
        };
        socket.emit('get-conversation-info', conversationInfoRequest);
    };

    this.sendMessage = function(text) {
        var message = {
            'conversation': currentConversation.id,
            'text': text
        };
        socket.emit('message', message);
    };

    this.requestConversation = function(user) {
        var users = [user, username];
        socket.emit('conversation-request', users);
    };

    this.getMessages = function(direction) {
        if (currentConversation) {
            if (!currentConversation.allMessages) {
                var messageRequest = {
                    'conversation': currentConversation.id,
                    'direction': direction
                };
                if (direction === 'newer') messageRequest['messageTimeStamp'] = currentConversation.getNewestMessage().timestamp;
                else messageRequest['messageTimeStamp'] = currentConversation.getOldestMessage().timestamp;
                socket.emit('get-messages', messageRequest);
            }
        }
    };

    this.requestConversations = function() {
        socket.emit('get-conversations');
    };


    /* METHODS FOR INTERACTING WITH GUI */


    this.changeConversation = function(conversationId) {
        currentConversation = findConversationById(conversationId);
        if (currentConversation) {
            currentConversation.unreadMessages = 0;
            saveToStorage();
            this.getMessages('older');
            this.getMessages('newer');
            showMessages();
        }
    };

    this.addConversation = function(conversationId, name, type) {
        if (!findConversationById(conversationId)) {
            conversations.push(new Conversation(conversationId, [username], name, type));
        }
    };

    this.closeConversation = function(conversationId) {
        var index = findConversationById(conversationId, true);
        if (index >= 0) conversations.splice(index, 1);
        currentConversation = undefined;
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
                if (index) return i;
                else return conversations[i];
            }
        }
        if (index) return -1;
        else return false;
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
                    if (saveObject.currentConversationId) chatUi.activateChat(saveObject.currentConversationId);
                }, 10);
            } catch(err) { }
        }
    };

    var saveToStorage = function() {
        var saveObject = {
            'conversations': [],
            'currentConversationId': (currentConversation ? currentConversation.id : false)
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
            conversation = new Conversation(message.conversation, [], "", "UNKNOWN");
            conversations.push(conversation);
            getConversationInfo(message.conversation);
        }
        conversation.addNewMessage(message);
        conversation.unreadMessages++;
        if ((message.sender != username) && (conversation.type != "UNKNOWN") && (conversation != currentConversation)) {
            chatUi.showChatButtonBadge(conversation.id, conversation.unreadMessages);
        }
        if (conversation === currentConversation) {
            if (message.sender === username) {
                chatUi.addOwnMessage(message.text, message.timestamp);
            } else {
                chatUi.addPartnerMessage(message.text,  message.sender, message.timestamp);
            }
        }
        saveToStorage();
        chatUi.showBadge();
    });

    socket.on('message-response', function(messages) {
        if (messages.length) {
            var conversation = findConversationById(messages[0].conversation);
            if (conversation) {
                //newer messages
                if (conversation.messages.length && conversation.messages[conversation.messages.length-1].timestamp < messages[0].timestamp) {
                    for (var i = 0; i < messages.length; i++) {
                        conversation.addNewMessage(messages[i]);
                        if (messages[i].sender === username) {
                            chatUi.addOwnMessage(messages[i].text, messages[i].timestamp);
                        } else {
                            chatUi.addPartnerMessage(messages[i].text, messages[i].sender, messages[i].timestamp);
                            chatUi.showChatButtonBadge(conversation.id, ++conversation.unreadMessages);
                        }
                    }
                //older messages
                } else {
                    for (var i = 0; i < messages.length; i++) {
                        conversation.addOldMessage(messages[i]);
                        if (messages[i].sender === username) {
                            chatUi.addOwnMessage(messages[i].text, messages[i].timestamp, 'top');
                        } else {
                            chatUi.addPartnerMessage(messages[i].text, messages[i].sender, messages[i].timestamp, 'top');
                        }
                    }
                }
            }
        } else {
            currentConversation.allMessages = true;
        }
         saveToStorage();
    });

    socket.on('conversation-list', function(conversations) {
        var projectConversations = [];
        var personConversations = [];
        for (var i = 0; i < conversations.length; i++) {
            if (conversations[i].name) projectConversations.push(conversations[i]);
            else {
                var ownIndex = conversations[i].users.indexOf(username);
                conversations[i].name = ownIndex === 0 ? conversations[i].users[1] : conversations[i].users[0];
                personConversations.push(conversations[i]);
            }
        }
        chatUi.addConversationsToOverview(projectConversations, personConversations);
    });

    socket.on('conversation-response', function(conversation) {
        var localConversation = findConversationById(conversation.id);
        console.log(localConversation);
        if (!localConversation) {
            if (!conversation.name) conversation.name = conversation.users[0];
            conversations.push(new Conversation(conversation.id, conversation.users, conversation.name, SINGLE_TYPE));
        } else {
            localConversation.addUsers(conversation.users);
            localConversation.addName(conversation.name);
        }
        self.changeConversation(conversation.id);
        saveToStorage();
    });

    socket.on('conversation-info', function(conversation) {
        var localConversation = findConversationById(conversation.id);
        localConversation.setUsers(conversation.users);
        if (conversation.name) {
            localConversation.setType(GROUP_TYPE);
        } else {
            var ownIndex = conversation.users.indexOf(username);
            conversation.name = ownIndex === 0 ? conversation.users[1] : conversation.users[0];
            localConversation.setType(SINGLE_TYPE);
        }
        localConversation.setName(conversation.name);
        localConversation.addToGui();
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

function Conversation(id, users, name, type) {
    this.id = id;
    this.users = users;
    this.name = name;
    this.type = type;
    this.messages = [];
    this.unreadMessages = 0;
    this.allMessages = false;

    this.addToGui = function() {
        if (this.type != GROUP_TYPE) {
            chatUi.addNewPersonChatButton(this.id, this.name);
        } else {
            chatUi.addNewGroupChatButton(this.id, this.name);
        }
        if (this.unreadMessages > 0) chatUi.showChatButtonBadge(this.id, this.unreadMessages);
    };

    this.getOldestMessage = function() {
        if (this.messages.length) {
            return this.messages[0];
        } else {
            return {'timestamp': ''};
        }
    };

    this.getNewestMessage = function() {
        if (this.messages.length) {
            return this.messages[this.messages.length-1];
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

    this.setUsers = function(users) {
        this.users = users;
    };

    this.setName = function(name) {
        this.name = name;
    };

    this.setType = function(type) {
        this.type = type;
    };

    if (type != "UNKNOWN") {
        this.addToGui();
    }
}
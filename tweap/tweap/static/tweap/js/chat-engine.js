function ChatManager() {
    var username = undefined;
    var currentConversation = undefined;
    var conversations = [];

    var socket = io('http://127.0.0.1:3000');

    this.getAuthStatus = function() {
      socket.emit('auth-status');
    };

    this.reAuthenticate = function() {

        var fakeCreds = {
            'username': 'jawu',
            'authToken': 'a8d48d3ff5a205fb0da5481940d63b63'
        };
        localStorage.setItem('chat-creds', JSON.stringify(fakeCreds));

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
        this.socket.emit('get-messages', messageRequest);
    };

    this.changeConversation = function(conversationId) {
        currentConversation = this.findConversationById(conversationId);
    };

    var findConversationById = function(conversationId) {
        for (var i = 0; i < conversations.length; i++) {
            if (conversations[i].id == conversationId) {
                return conversations[i];
            }
        }
        return false;
    };

    socket.on('auth-status', function(data) {
        console.log("current auth status: " + data.status);
    });

    socket.on('auth-success', function(data) {
        var chatCreds = JSON.parse(localStorage.getItem('chat-creds'));
        chatCreds.authToken = data.authToken;
        localStorage.setItem('chat-creds', JSON.stringify(chatCreds));
    });

    socket.on('message', function(message) {
        var conversation = findConversationById(message.conversation);
        if (conversation) {
            conversation.addNewMessage(message);
            // add badge to conv on gui
        } else {
            conversation = new Conversation(message.conversation, [message.sender], message.sender);
            conversations.push(conversation);
            conversation.addNewMessage(message);
            // add conv to gui
            // add badge to conv on gui
        }
        if (conversation === currentConversation) {
            if (message.sender === username) {
                addOwnMessage(message.text, message.sender, message.timestamp);
            } else {
                addPartnerMessage(message.text, message.timestamp);
            }
        }
    });

    socket.on('message-response', function(messages) {
        if (messages.length > 0) {
            var conversation = findConversationById(message[0].conversation);
            if (conversation) {
                conversation.addOldMessages(messages);
            }
        }
    });

    socket.on('conversation-response', function(conversation) {
        var conversation = findConversationById(conversation.id);
        if (!conversation) {
            conversations.push(new Conversation(conversation.id, conversation.users, conversation.name));
        } else {
            conversation.addUsers(conversation.users);
            conversation.addName(conversation.name);
        }
    });


    /* initial stuff */
    this.getAuthStatus();
    this.reAuthenticate();
    this.getAuthStatus();
    conversations.push(new Conversation(19, ['jawu'], 'test-Conv'));
    currentConversation = findConversationById(19);

}

function Conversation(id, users, name) {
    this.id = id;
    this.users = users;
    this.name = name;
    this.messages = [];

    addNewPersonChatButton(id, name);

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
        this.messages.unshift(oldMessages);
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
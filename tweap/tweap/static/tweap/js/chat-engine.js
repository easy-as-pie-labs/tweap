function ChatManager() {
    var username = undefined;
    var currentConversation = undefined;
    var conversations = [];

    var socket = io('http://127.0.0.1:3000');

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
            'conversation': currentConversation.getId(),
            'text': text
        };
        socket.emit('message', message);
    };

    this.requestConversation = function(users) {
        socket.emit('conversation-request', users);
    };

    this.getOldMessages = function() {
        var messageRequest = {
            'conversation': currentConversation.getId(),
            'messageId': currentConversation.getOldestMessage().id
        };
        this.socket.emit('get-messages', messageRequest);
    };

    this.changeConversation = function(conversationId) {
        currentConversation = this.findConversationById(conversationId);
    };

    var findConversationById = function(conversationId) {
        for (var i = 0; i < conversations.length; i++) {
            if (conversations[i].getId() == conversationId) {
                return conversations[i];
            }
        }
        return false;
    };

    socket.on('auth-success', function(data) {
        var chatCreds = JSON.parse(localStorage.getItem('chat-creds'));
        chatCreds.authToken = data.authToken;
        localStorage.setItem('chat-creds', JSON.stringify(chatCreds));
    });

    socket.on('message', function(message) {
        var conversation = findConversationById(message.conversation);
        if (conversation) {
            conversation.addNewMessage(message, username);
            // add badge to conv on gui
        } else {
            conversation = new Conversation(message.conversation, [message.sender, username]);
            conversations.push(conversation);
            conversation.addNewMessage(message, username);
            // add conv to gui
            // add badge to conv on gui
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
            conversations.push(new Conversation(conversation.id, conversation.users));
        } else {
            conversation.addUsers(conversation.users);
        }
    });


    /* initial stuff */
    this.reAuthenticate();
    conversations.push(new Conversation(19, ['jawu']));
    currentConversation = findConversationById(19);

}

function Conversation(id, users) {
    var id = id;
    var users = users;
    var messages = [];

    addNewPersonChatButton(id, id);

    this.getOldestMessage = function() {
        if (messages.length > 0) {
            return messages[0];
        } else {
            return {'id': ''};
        }
    };

    this.showMessages = function(username) {
        for (var i = 0; i < messages.length; i++) {
            if (messages[i].sender === username) {
                addOwnMessage(messages[i].text, messages[i].sender, messages[i].timestamp);
            } else {
                addPartnerMessage(messages[i].text, messages[i].timestamp);
            }
        }
    };

    this.addOldMessages = function(oldMessages) {
        messages.unshift(oldMessages);
    };

    this.addNewMessage = function(newMessage, username) {
        messages.push(newMessage);
        if (newMessage.sender === username) {
            addOwnMessage(newMessage.text, newMessage.sender, newMessage.timestamp);
        } else {
            addPartnerMessage(newMessage.text, newMessage.timestamp);
        }
    };

    this.addUsers = function(newUsers) {
        users = newUsers;
    };

    this.getId = function() {
        return id;
    };
}
function ChatManager() {
    var username = undefined;
    var currentConversation = undefined;
    var conversations = [];

    var socket = io('http://127.0.0.1:3000');
    reAuthenticate();


    var reAuthenticate = function() {
        socket.emit('re-auth', localStorage.getItem('chat-creds'));
        username = JSON.parse(localStorage.getItem('chat-creds')).username;
        console.log("send re-auth");
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
        for (var i = 0; i < this.conversations.length; i++) {
            if (this.conversations[i].id == conversationId) {
                return conversation[i];
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
            conversation.addMessage(message);
            // add badge to conv on gui
        } else {
            conversations.push(new Conversation(message.conversation, [message.sender, username]));
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

}

function Conversation(id, users) {
    var id = id;
    var users = users;
    var messages = [];

    this.getOldestMessage = function() {
        if (messages.length > 0) {
            return messages[0];
        } else {
            return {'id': ''};
        }
    };

    this.getMessages = function() {
        return messages;
    };

    this.addOldMessages = function(oldMessages) {
        messages.unshift(oldMessages);
    };

    this.addNewMessage = function(newMessage) {
        messages.push(newMessage);
    };

    this.addUsers = function(newUsers) {
        users = newUsers;
    }
}
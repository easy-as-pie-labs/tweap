function ChatManager() {
    this.conversations = [];
    this.socket = io('http://127.0.0.1:3000');

    //authenticate
    //load messages

    this.sendMessage = function(message) {

    };

    this.requestConversation = function(users) {

    };

    this.getMessages = function() {

    };

    this.socket.on('placeholder', function(data) {

    });
}

function Conversation(id) {
    this.id = id;
    this.messages = [];

    this.addMessages = function(messages) {
        //add to Messages
    }
}

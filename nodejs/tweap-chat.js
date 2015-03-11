
/* SOCKET */

var io = require('socket.io')(3000);
console.log("tweap-chat running on port 3000...");


io.on('connection', function(socket) {

  // receiving login
  socket.on('login', function(user) {
    //authenticate here
    var auth = true;
    if (auth) {
      clientManager.addClient(new User(user, this));
    } else {
      this.client.disconnect();
    }
  });

  // receiving a message
  socket.on('message', function(msg) {
    io.to(msg.conversation).emit('message', msg);
    // add message via tweap to db
    // tweap.addMessage(msg);
  });

  // receiving request to start new conversation
  socket.on('startNewConversation', function(requestConv) {
    // var conv = tweap.getOrAddConversation(conv);
    // dev placeholder for testing
    var conv = {'id': 157, 'users': ['jawu', 'thomas']};
    for (var user of conv.users) {
      var sock = clientManager.getSocketOfUser(user);
      if (sock) {
        clientManager.getSocketOfUser(user).join(conv.id);
        console.log(user + " is connected and added");
      } else {
        console.log(user + " is not connected");
      }
    }
    this.emit('conversationId', conv);
  });

  // receiving disconnect
  socket.on('disconnect', function() {
    console.log('disconnected: ' + this.id);
  });

});




/* LOGIC */

var clientManager = new ClientManager();

function ClientManager() {
  var clients = [];

  this.addClient = function(user) {
    clients.push(user);
    //add client to conversation rooms
    for (var conversation of getConversationsOfUser(user.name)) {
      user.socket.join(conversation);
    }
  }

  this.getSocketOfUser = function(username) {
    for (var client of clients) {
      if (client.name == username) {
        return client.socket;
      }
    }
    return false;
  }
}


function User(name, socket) {
  this.name = name;
  this.socket = socket;
}

var getConversationsOfUser = function(user) {
  // get them from database!
  return ['123', '124'];
}

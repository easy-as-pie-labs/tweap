
/* SOCKET */

var io = require('socket.io')(3000);
console.log("tweap-chat running on port 3000...");


io.on('connection', function(socket) {

  var authenticated = false;

  console.log("new client connected");

  setTimeout(function() {
    if (!authenticated) {
      console.log("no authentication in 1000ms -> disconnect");
      socket.client.disconnect();
    }
  }, 1000);

  socket.on('auth', function(request) {
    //authenticate here
    if (!clientManager.getBySocket(this)) {
      var authen = true;
      if (authen) {
        clientManager.add(new Client(request.username, this));
        console.log("correct authentication!");
        authenticated = true;
      } else {
        console.log("wrong authentication -> disconnect");
        this.client.disconnect();
      }
    } else {
      console.log("double auth -> no action");
    }

  });

  socket.on('reauth', function(request) {
    var client = clientManager.getByName(request.username);
    if (client && !client.connected && request.reAuthToken == client.reAuthToken) {
          client.connected = true;
          client.socket = this;
          console.log("correct reauth");
          authenticated = true;
    } else {
      console.log("wrong reauth -> disconnect");
      this.client.disconnect();
    }
  });



  // receiving a message
  socket.on('message', function(msg) {
    if (auth) {
      io.to(msg.conversation).emit('message', msg);
    // add message via tweap to db
    // tweap.addMessage(msg);
    console.log("message sended");
  } else {
    console.log("not authenticated -> no message");
  }
  });

  // receiving request to start new conversation
  socket.on('startNewConversation', function(requestConv) {
    // var conv = tweap.getOrAddConversation(conv);
    // dev placeholder for testing
    var conv = {'id': 157, 'users': ['jawu', 'thomas']};
    for (var username of conv.users) {
      var client = clientManager.getByName(username);
      if (client) {
        client.socket.join(conv.id);
        console.log(user + " is connected and added");
      } else {
        console.log(user + " is not connected");
      }
    }
    this.emit('conversationId', conv);
  });

  // receiving disconnect
  socket.on('disconnect', function() {
    var client = clientManager.getBySocket(this);
    if (client) {
      client.connected = false;
      setTimeout(function() {
          //here must socket be the parameter
          clientManager.removeBySocket(this);
      }, 10000);
    }

    console.log('disconnected: ' + this.id);
  });

});




/* LOGIC */

var clientManager = new ClientManager();

setInterval(function() {
  clientManager.showClients();
}, 1000);

function ClientManager() {
  var clients = [];

  this.add = function(client) {
    clients.push(client);
    //add client to conversation rooms
    for (var conversation of getConversationsOfUser(client.name)) {
      client.socket.join(conversation);
    }
  };

  this.removeBySocket = function(socket) {
    console.log("called remove with " + socket.id);
    for (var i = 0; i < clients.length; i++) {
      if (clients[i].socket == socket) {
        clients.splice(i, 1);
        console.log("removed because of no reauth");
        return;
      }
    }
  }

  this.getByName = function(username) {
    for (var client of clients) {
      if (client.username == username) {
        return client;
      }
    }
    return false;
  };

  this.getBySocket = function(socket) {
    for (var client of clients) {
      if (client.socket == socket) {
        return client;
      }
    }
    return false;
  }

  this.showClients = function() {
    console.log("Client-List.....");
    for (var client of clients) {
        console.log(client.username + " - " + client.socket.id + " - " + client.connected);
    }
  }
}


function Client(name, socket) {
  this.username = name;
  this.socket = socket;
  this.connected = true;
  this.reAuthToken = "ra";
}

var getConversationsOfUser = function(user) {
  // get them from database!
  return ['123', '124'];
}

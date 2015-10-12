/*  require needed js files
    start socket.io on configured port
    create ClientManager
    forward connections to a new instance of Communicator
 */

var PORT = 3000;

var io = require('socket.io')(PORT);
var ClientManager = require('./tweap/client-manager.js');
var clientManager = new ClientManager();
var Communicator = require('./tweap/communicator.js');

console.log("tweap-chat running on port 3000...");

io.on('connection', function(socket) {
    new Communicator(socket, clientManager, io);
});
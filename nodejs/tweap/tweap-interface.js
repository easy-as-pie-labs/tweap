if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {

     var tweap = {
        checkCredentials: function(username, password) {
            return true;
        },
        addMessage: function(message) {
            return true;
        },
        getOrAddConversation: function(userlist) {
            return {'id': 123, 'users': ['tpei', 'shonyyyy', 'googlez', 'jawu']}
        },
        getConversationsOfUser: function(username) {
            return ["1234", "432", "1243"];
        }
    };

    return tweap;

});
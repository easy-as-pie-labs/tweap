if (typeof define !== 'function') {
    var define = require('amdefine')(module);
}

define(function() {

    var tweapUrl = "http://127.0.0.1:8000/chat/api/";

    var najax = require('../libs/najax.js');

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
        },

         updateAuthToken: function(username, newAuthToken, oldAuthToken) {
            return true;
         },

         makeRequest: function(action, data, cb) {
             data = {
                 'action': action,
                 'data': data
             };
             najax({ url:tweapUrl, type:'POST', data:JSON.stringify(data) })
                .success(function(resp){
                    console.log(resp.data);
                    console.log("success");
                })
                .error(function(err){
                    console.log(err);
                    console.log("error");
                });
         }
    };

    return tweap;

});
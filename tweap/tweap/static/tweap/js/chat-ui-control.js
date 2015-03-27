$(document).ready(function(){
    addBadge();
    updateBadge("22");

    //Loads Active Chats. This is the way it has to be treated
    var activeChatArray = new Array();
    activeChatArray.push(new ActiveChat(1, "jawu", "person"));
    activeChatArray.push(new ActiveChat(2, "tpei", "person"));
    activeChatArray.push(new ActiveChat(77, "iLab", "group"));
    activeChatArray.push(new ActiveChat(4, "goggelz", "person"));

    localStorage.setItem("activeChats", JSON.stringify(activeChatArray));
    //End of active Chatssaving

    //Initialization of Chat
    var child = $('#chat-panel').children().first();
    var chatIcon = child.children().first();
    var chatBody = $('#chat-panel .panel-body');

    if(localStorage.getItem("chatToggleStatus") == "true") {
        chatIcon.removeClass('fa-chevron-right');
        chatIcon.addClass('fa-chevron-down');
        chatBody.show();
        chatPanelToggleUpCycle();
    }

    var chatManager = new ChatManager();

});

$(document).on('click', '#send-message', function (e) {
    writeMessage();
});

$(document).on('keydown', '#message-text', function(e) {
    if (e.which == 13) {
        writeMessage();
    }
});

//All active Chats are saved as an Object of this kind in an Array
ActiveChat = function(id, chatname, chatType) {
    this.id = id;
    this.chatname = chatname;
    this.chatType = chatType;
}

//Called on every toggleevent(toggle down)
function addBadge() {
    /*
    * Should only be executed, when there are any unread Messages!
    * Please extend this Method for this constraint
     */
    var panelHeading = $("#chat-panel").children().first();
    panelHeading.append('<span class="badge">30</span>');
}

//Called on every toggleevent (toggle up)
function removeBadge() {
    $('.badge').remove();
}

function updateBadge(val) {
    $('.badge').html(val);
}

function addPartnerMessage(msg, username, timestamp) {
    var msgString = '<div class="row">' +
        '<div class="col-md-12">' +
        '<div class="chat-partner-bubble">' +
        '<div class="chat-info">' + username + ' at ' + timestamp + ' :</div>' + msg + '</div>' +
        '</div>' +
        '</div>';

    $('#chat-content').append(msgString);
    updateScroll();
}

function addOwnMessage(msg, timestamp) {
    var msgString = '<div class="row">' +
        '<div class="col-md-12">' +
        '<div class="chat-own-bubble">' +
        '<div class="chat-info">You at ' + timestamp + ' :</div>' + msg + '</div>' +
        '</div>' +
        '</div>';

    $('#chat-content').append(msgString);
    updateScroll();
}

function addNewPersonChatButton(chatId, name) {
    var chatButtonString = '<div class="btn-group" role="group">' +
        '<button type="button" class="btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
        '<span class="fa fa-user"></span>' + name +
        '</button>' +
        '</div>';

    $('#chat-buttons').append(chatButtonString);
    $('#chat-buttons').find("[data-chat-id='" + chatId + "']").click(function(){
        activateChat(chatId);
    });
}

function addNewGroupChatButton(chatId, name) {
    var chatButtonString = '<div class="btn-group" role="group">' +
        '<button type="button" class="btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
        '<span class="fa fa-users"></span>' + name +
        '</button>' +
        '</div>';

    $('#chat-buttons').append(chatButtonString);
    $('#chat-buttons').find("[data-chat-id='" + chatId + "']").click(function(){
        activateChat(chatId);
    });
}

function writeMessage() {
    //Code for backend to write a message here:

    var msg = $('#message-text').val();
    if(msg != "") {
        var date = new Date();
        var h = date.getHours();
        var m = date.getMinutes();

        var time = h + ":" + m;

        addOwnMessage(msg, time);
        $('#message-text').val("");
    }
}

function updateScroll(){
    var chatContent = document.getElementById("chat-content");
    chatContent.scrollTop = chatContent.scrollHeight;
}

function emptyContents() {
    $('#chat-content').empty();
    $('#chat-buttons').empty();
}

function activateChat(chatId) {
    emptyContents();

    if(localStorage.getItem("activeChats") === null) {
        activateOverview();
    } else {
        var openChats = JSON.parse(localStorage.getItem("activeChats"));
        for (var i = 0; i < openChats.length; i++) {
            var addChatId = openChats[i].id;
            var chatName = openChats[i].chatname;

            if (openChats[i].chatType == "person") {
                addNewPersonChatButton(addChatId, chatName);
            } else {
                addNewGroupChatButton(addChatId, chatName);
            }
        }
        var elements = $('.chat-btn');
        elements.removeClass('btn-primary');
        elements.removeClass('btn-default');
        elements.addClass('btn-default');

        var element = $(document).find("[data-chat-id='" + chatId + "']");
        element.addClass('btn-primary');
        localStorage.setItem("activeChatId", chatId);

        //TODO: get Data array or anything else and use addOwnMessage() and addPartnerMessage()
        addPartnerMessage("Hi Jonas", "shony", "12:00");
        addOwnMessage("Na, wie gehts?", "12:01");
        addPartnerMessage("Kann mich nicht beklagen und dir so?", "shony", "12:01");
        addOwnMessage("Ditooooo :) was gibts ?", "12:03");
        addPartnerMessage("Jaja kein smalltalk, gleich zu Sache haha, ok ;)", "shony", "12:04");
        addPartnerMessage("Also: Könntest du mir freitag beim Umzug helfen?", "shony", "12:04");
    }
}

//TODO: Hier Dictionary für Ausgabe beachten
function activateOverview() {
    var overViewHtmlString = '<h1>Chats</h1>';
    $('#chat-content').empty().append(overViewHtmlString);
    localStorage.setItem("overView", false);
}

function chatPanelToggleUpCycle() {
    removeBadge();
    updateScroll();
    if(localStorage.getItem("overView") != "True") {
        activateChat(localStorage.getItem("activeChatId"));
    } else {
        activateOverview();
    }
    localStorage.setItem("chatToggleStatus", true);
}

function appendPossibleGroupChat() {

}

function chatPanelToggleDownCycle() {
    addBadge();
    localStorage.setItem("chatToggleStatus", false);
}

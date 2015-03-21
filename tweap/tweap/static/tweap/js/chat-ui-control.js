$(document).ready(function(){
    addBadge();
    updateBadge("22");

    addNewPersonChatButton(1, "jawu");
    addNewPersonChatButton(2, "tpei");
    addNewPersonChatButton(3, "goggelz");
    addNewGroupChatButton(6, "iLab");
    addNewPersonChatButton(7, "shony");

    addPartnerMessage("Hi Jonas", "shony", "12:00");
    addOwnMessage("Na, wie gehts?", "12:01");
    addPartnerMessage("Kann mich nicht beklagen und dir so?", "shony", "12:01");
    addOwnMessage("Ditooooo :) was gibts ?", "12:03");
    addPartnerMessage("Jaja kein smalltalk, gleich zu Sache haha, ok ;)", "shony", "12:04");
    addPartnerMessage("Also: Könntest du mir freitag beim Umzug helfen?", "shony", "12:04");

    var child = $('#chat-panel').children().first();
    var chatIcon = child.children().first();
    var chatBody = $('#chat-panel .panel-body');

    if(localStorage.getItem("chatToggleStatus") == "true") {
        chatIcon.removeClass('fa-chevron-right');
        chatIcon.addClass('fa-chevron-down');
        chatBody.show();
        chatPanelToggleUpCycle();
    }

});

$(document).on('click', '#send-message', function (e) {
    writeMessage();
});

$(document).on('click', '.chat-btn', function (e) {
    var chatId = $(this).attr('data-chat-id');
    activateChat(chatId);
});

$(document).on('keydown', '#message-text', function(e) {
    if (e.which == 13) {
        writeMessage();
    }
});

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
}

function addNewGroupChatButton(chatId, name) {
    var chatButtonString = '<div class="btn-group" role="group">' +
        '<button type="button" class="btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
        '<span class="fa fa-users"></span>' + name +
        '</button>' +
        '</div>';

    $('#chat-buttons').append(chatButtonString);
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

function activateChat(chatId) {
    var elements = $('.chat-btn');//.find("[data-chat-id='" + chatId + "']");
    elements.removeClass('btn-primary');
    elements.removeClass('btn-default');
    elements.addClass('btn-default');

    var element = $(document).find("[data-chat-id='" + chatId + "']");
    element.addClass('btn-primary');
    localStorage.setItem("activeChatId", chatId);

    //get Data array or anything else and use addOwnMessage() and addPartnerMessage()
}

function chatPanelToggleUpCycle() {
    removeBadge();
    updateScroll();
    activateChat(localStorage.getItem("activeChatId"));
    localStorage.setItem("chatToggleStatus", true);
}

function chatPanelToggleDownCycle() {
    addBadge();
    localStorage.setItem("chatToggleStatus", false);
}

var chatManager;

$(document).ready(function(){

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

    chatManager = new ChatManager();

});

$(document).on('click', '#send-message', function (e) {
    writeMessage();
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
    panelHeading.append('<span class="badge">0</span>');
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
    var msg = $('#message-text').val();
    if(msg != "") {
        chatManager.sendMessage($('#message-text').val());
        $('#message-text').val("");
    }
}

function updateScroll(){
    var chatContent = document.getElementById("chat-content");
    chatContent.scrollTop = chatContent.scrollHeight;
}

function emptyConversation() {
    $('#chat-content').empty();
}

function activateChat(chatId) {
    emptyConversation();
    chatManager.changeConversation(chatId);


    var elements = $('.chat-btn');
    elements.removeClass('btn-primary');
    elements.removeClass('btn-default');
    elements.addClass('btn-default');

    var element = $(document).find("[data-chat-id='" + chatId + "']");
    element.addClass('btn-primary');
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
    if(localStorage.getItem("overView") == "True") {
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

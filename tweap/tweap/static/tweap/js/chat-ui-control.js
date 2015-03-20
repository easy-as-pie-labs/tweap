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
});

function addBadge() {
    /*
    * Should only be executed, when there are any unread Messages!
    * Please extend this Method for this constraint
     */
    var panelHeading = $("#chat-panel").children().first();
    panelHeading.append('<span class="badge">30</span>');
}

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
}

function addOwnMessage(msg, timestamp) {
    var msgString = '<div class="row">' +
        '<div class="col-md-12">' +
        '<div class="chat-own-bubble">' +
        '<div class="chat-info">You at ' + timestamp + ' :</div>' + msg + '</div>' +
        '</div>' +
        '</div>';

    $('#chat-content').append(msgString);
}

function addNewPersonChatButton(chatId, name) {
    var chatButtonString = '<div class="btn-group" role="group">' +
        '<button type="button" class="btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
        '<span class="fa fa-user"></span>' + name +
        '</button>' +
        '</div>';
    console.log("done");
    $('#chat-buttons').append(chatButtonString);
}

function addNewGroupChatButton(chatId, name) {
    var chatButtonString = '<div class="btn-group" role="group">' +
        '<button type="button" class="btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
        '<span class="fa fa-users"></span>' + name +
        '</button>' +
        '</div>';
    console.log("done");
    $('#chat-buttons').append(chatButtonString);
}


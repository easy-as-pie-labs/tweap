
$(document).ready(function() {

    chatUi = new ChatUi();
    chatManager = new ChatManager();

    //Initialization of Chat
    var child = $('#chat-panel').children().first();
    var chatIcon = child.children().first();
    var chatBody = $('#chat-panel .panel-body');

    if(localStorage.getItem("chatToggleStatus") == "true") {
        chatIcon.removeClass('fa-chevron-right');
        chatIcon.addClass('fa-chevron-down');
        chatBody.show();
        chatUi.chatPanelToggleUpCycle();
    }

});

$(document).on('click', '#send-message', function (e) {
    chatUi.writeMessage();
});

$(document).on('keydown', '#message-text', function(e) {
    if (e.which == 13) {
        chatUi.writeMessage();
    }
});

$(document).on('click', '#all-chats', function (e) {
    chatUi.activateOverview();
});

ChatUi = function() {

    var that = this;

    //Called on every toggleevent(toggle down)
    this.addBadge = function() {
        /*
        * Should only be executed, when there are any unread Messages!
        * Please extend this Method for this constraint
         */
        var panelHeading = $("#chat-panel").children().first();
        panelHeading.append('<span class="badge">0</span>');
    }

    //Called on every toggleevent (toggle up)
    this.removeBadge = function() {
        $('.badge').remove();
    }

    this.updateBadge = function(val) {
        $('.badge').html(val);
    }

    this.addPartnerMessage = function(msg, username, timestamp) {
        var msgString = '<div class="row">' +
            '<div class="col-md-12">' +
            '<div class="chat-partner-bubble">' +
            '<div class="chat-info">' + username + ' at ' + timestamp + ' :</div>' + msg + '</div>' +
            '</div>' +
            '</div>';

        $('#chat-content').append(msgString);
        this.updateScroll();
    }

    this.addOwnMessage = function(msg, timestamp) {
        var msgString = '<div class="row">' +
            '<div class="col-md-12">' +
            '<div class="chat-own-bubble">' +
            '<div class="chat-info">You at ' + timestamp + ' :</div>' + msg + '</div>' +
            '</div>' +
            '</div>';

        $('#chat-content').append(msgString);
        this.updateScroll();
    }

    this.addNewPersonChatButton = function(chatId, name) {
        var chatButtonString = '<div class="btn-group" role="group">' +
            '<button type="button" class="btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
            '<span class="fa fa-user"></span>' + name +
            '<span class="fa fa-close pull-right"></span>' +
            '</button>' +
            '</div>';

        $('#chat-buttons').append(chatButtonString);

        this.appendListenerToChatButtons(chatId);
    }

    this.addNewGroupChatButton = function(chatId, name) {
        var chatButtonString = '<div class="btn-group" role="group">' +
            '<button type="button" class="btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
            '<span class="fa fa-users"></span>' + name +
            '<span class="fa fa-close pull-right"></span>' +
            '</button>' +
            '</div>';

        $('#chat-buttons').append(chatButtonString);
        this.appendListenerToChatButtons(chatId);
    }

    this.appendListenerToChatButtons = function(chatId) {
        var recentylAddedButton = $('#chat-buttons').find("[data-chat-id='" + chatId + "']");
        recentylAddedButton.click(function(){
            that.activateChat(chatId);
        });

        recentylAddedButton.children(".fa-close").click(function(){
            that.closeChat(chatId);
        });
    }

    this.writeMessage = function() {
        var msg = $('#message-text').val();
        if(msg != "") {
            chatManager.sendMessage($('#message-text').val());
            $('#message-text').val("");
        }
    }

    this.updateScroll = function(){
        var chatContent = document.getElementById("chat-content");
        chatContent.scrollTop = chatContent.scrollHeight;
    }
    
    this.emptyConversation = function() {
        $('#chat-content').empty();
        $('#chat-message').empty();
    }

    //TODO: Hier Dictionary für Ausgabe beachten

    this.appendChatMessageInput = function() {
        var htmlString = '<input id="message-text" type="text" class="form-control" placeholder="Your Message" aria-describedby="sizing-addon2">' +
            '<span id="send-message" class="input-group-addon btn">' +
            '<span class="fa fa-send fa-lg"></span>' +
            '</span>';
        $('#chat-message').append(htmlString);
    }

    this.activateChat = function(chatId) {
        this.emptyConversation();
        //chatManager.setCurrentConversation(chatId);
        this.appendChatMessageInput();
        chatManager.changeConversation(chatId);

        var elements = $('.chat-btn');
        elements.removeClass('btn-primary');
        elements.removeClass('btn-default');
        elements.addClass('btn-default');

        var element = $(document).find("[data-chat-id='" + chatId + "']");
        element.addClass('btn-primary');
        localStorage.setItem("overView", false);
    }

    this.closeChat = function(chatId) {
        var element = $(document).find("[data-chat-id='" + chatId + "']");
        element.parent().remove();
        chatManager.closeConversation(chatId);
    }

    //TODO: Hier Dictionary für Ausgabe beachten
    this.activateOverview = function() {

        this.emptyConversation();
        chatManager.requestConversations();

        var overViewHtmlString = '<h2>Open Projectchat</h2>' +
            '<ul id="group-chats" class="nav nav-pills"></ul>' +
            '<h2>Open Chat with a single person</h2>' +
            '<ul id="person-chats" class="nav nav-pills"></ul>';
        $('#chat-content').append(overViewHtmlString);
        localStorage.setItem("overView", true);
    }

    this.addConversationsToOverview = function(projects, users) {
        for(var i = 0; projects.length>i; i++) {
            this.appendPossibleChatButton(projects[i].name, "group", projects[i].id);
        }

        for(var i = 0; users.length>i; i++) {
            this.appendPossibleChatButton(users[i].name, "user", users[i].id);
        }
    }

    this.appendPossibleChatButton = function(chatname, chatType, chatId) {
        if(chatType == "group") {
            var buttonHtmlString = '<li role="presentation" class="active psbl-chat-btn"><a href="#">' +
                '<span class="fa fa-users"></span>'
                + chatname +
                '</a></li>';
            var element = $('#group-chats').append(buttonHtmlString);
            element.click(function(){
                chatManager.addConversation(chatId, chatname);
            });
        } else {
            var buttonHtmlString = '<li role="presentation" class="active psbl-chat-btn"><a href="#">' +
                '<span class="fa fa-user"></span>'
                + chatname +
                '</a></li>';
            var element = $('#person-chats').append(buttonHtmlString);
            element.click(function(){
                chatManager.addConversation(chatId, chatname);
            });
        }

    }

    this.chatPanelToggleUpCycle = function() {
        this.removeBadge();
        this.updateScroll();
        localStorage.setItem("chatToggleStatus", true);
    }

    this.chatPanelToggleDownCycle = function() {
        this.addBadge();
        localStorage.setItem("chatToggleStatus", false);
    }

}

var chatManager;

$(document).ready(function(){
    chatUi = new chatUi;
    chatUi.addNewGroupChatButton(12, "iLab");
    chatUi.addNewPersonChatButton(2, "shony");
    chatUi.addNewPersonChatButton(4, "jawu");
    chatUi.addNewPersonChatButton(5, "goggelz");

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

    chatManager = new ChatManager();

});

$(document).on('click', '#send-message', function (e) {
    this.writeMessage();
});

$(document).on('keydown', '#message-text', function(e) {
    if (e.which == 13) {
        this.writeMessage();
    }
});

chatUi = function() {

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
    }

    this.activateChat = function(chatId) {
        this.emptyConversation();
        //chatManager.setCurrentConversation(chatId);

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

        chatManager.requestConversations();

        var overViewHtmlString = '<h2>Open Projectchat</h2>' +
            '<ul id="group-chats" class="nav nav-pills"></ul>' +
            '<h2>Open Chat with a single person</h2>' +
            '<ul id="person-chats" class="nav nav-pills"></ul>';
        $('#chat-content').empty().append(overViewHtmlString);
        localStorage.setItem("overView", true);
    }

    this.addConversationsToOverview = function(groups, users) {
        for(var i = 0;groups.length>i;i++) {
            this.appendPossibleChatButton(groups[i].name, "group", groups[i].id);
        }

        for(var i = 0;users.length>i;i++) {
            this.appendPossibleChatButton(userss[i].name, "user", users[i].id);
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
        if(localStorage.getItem("overView") != "true") {
            this.activateChat(localStorage.getItem("activeChatId"));
        } else {
            this.activateOverview();
        }
        localStorage.setItem("chatToggleStatus", true);
    }

    this.chatPanelToggleDownCycle = function() {
        this.addBadge();
        localStorage.setItem("chatToggleStatus", false);
    }

}


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
    var overviewState = false;
    /**
     * Called on every toggleevent(toggle down)
     */
    this.addBadge = function() {
        /*
        * Should only be executed, when there are any unread Messages!
        * Please extend this Method for this constraint
         */
        var panelHeading = $("#chat-panel").children().first();
        panelHeading.append('<span class="badge">0</span>');
    };

    /**
     * Called on every toggleevent (toggle up) - removes the Badge
     */
    this.removeBadge = function() {
        $('.badge').remove();
    };

    /**
     * Called on every toggleevent (toggle down) - updates the Badgevalue
     * @param val = number to be shown inside the badge as String
     */
    this.updateBadge = function(val) {
        $('.badge').html(val);
    };

    /**
     * Adds a Message from your partner on the left side of the chat-content
     * @param msg = the Message as String
     * @param username = the username to be shown as String
     * @param timestamp = the timestamp to be shown as String
     */
    this.addPartnerMessage = function(msg, username, timestamp) {
        if(!overviewState) {
            var msgString = '<div class="row">' +
            '<div class="col-md-12">' +
            '<div class="chat-partner-bubble">' +
            '<div class="chat-info">' + username + ' at ' + formatTime(timestamp) + ' </div>' + msg + '</div>' +
            '</div>' +
            '</div>';

            $('#chat-content').append(msgString);
            this.updateScroll();
        }
    };

    /**
     * Adds a Message from yourself on the right side of the chat-content
     * @param msg = the Message as String
     * @param timestamp = the timestamp to be shown as String
     */
    this.addOwnMessage = function(msg, timestamp) {
        if(!overviewState) {
            var msgString = '<div class="row">' +
                '<div class="col-md-12">' +
                '<div class="chat-own-bubble">' +
                '<div class="chat-info">You at ' + formatTime(timestamp) + ' </div>' + msg + '</div>' +
                '</div>' +
                '</div>';

            $('#chat-content').append(msgString);
            this.updateScroll();
        }
    };

    /**
     * Adds a new "Tab" in top of the chatwindow with a user-icon
     * @param chatId = chatId of the chat as Integer
     * @param name = name of the conversation to be shown as String
     */
    this.addNewPersonChatButton = function(chatId, name) {
        var chatButtonString = '<div class="btn-group" role="group">' +
            '<button type="button" class="btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
            '<span class="fa fa-user"></span>' + name +
            '<span class="fa fa-close pull-right"></span>' +
            '</button>' +
            '</div>';

        $('#chat-buttons').append(chatButtonString);

        this.appendListenerToChatButtons(chatId);
    };

    /**
     * Adds a new "Tab" in top of the chatwindow with a group-icon
     * @param chatId = chatId of the chat as Integer
     * @param name = name of the conversation to be shown as String
     */
    this.addNewGroupChatButton = function(chatId, name) {
        var chatButtonString = '<div class="btn-group" role="group">' +
            '<div type="button" class="clearfix btn btn-default chat-btn" data-chat-id="' + chatId + '">' +
            '<span class="chat-button-content"><span class="fa fa-users"></span>' + name +
            '<span class="chat-button-badge badge"></span></span>' +
            '<span class="fa fa-close pull-right"></span>' +
            '</div>' +
            '</div>';

        $('#chat-buttons').append(chatButtonString);
        this.appendListenerToChatButtons(chatId);
    };

    /**
     * Adds a Badge to a certain Chatbutton
     * @param chatId = id for which button the badge should be shown in Integer
     * @param amount = number to be shown inside the badge as String
     */
    this.showChatButtonBadge = function(chatId, amount) {
        var button = $('#chat-buttons').find("[data-chat-id='" + chatId + "']");
        var element = button.find('.badge');
        element.html(amount);
    };

    /**
     * Empties a Badge of a certain Chatbutton is called in this.activateChat()
     * @param chatId = id for which button the badge should be emptified in Integer
     */
    this.emptyChatButtonBadge = function(chatId) {
        var button = $('#chat-buttons').find("[data-chat-id='" + chatId + "']");
        var element = button.find('.badge');
        element.empty();
    };

    /**
     * Appends clickListener to the "Tabs" and is called inside addNewGroupChatButton() and addNewPersonChatButton
     * @param chatId = id for which chatbutton the Listener should be appended as Integer
     */
    this.appendListenerToChatButtons = function(chatId) {
        var recentylAddedButton = $('#chat-buttons').find("[data-chat-id='" + chatId + "']");

        recentylAddedButton.click(function(){
            that.activateChat(chatId);
        });

        var children = recentylAddedButton.children(".fa-close");
        children.each(function(){
            $(this).click(function(e){
                that.closeChat(chatId);
                e.preventDefault();
                return false;
            });
        });
    };

    /**
     * Function for Clicklistener of chat-message inputfield. This function is used when the user send a message
     */
    this.writeMessage = function() {
        var msg = $('#message-text').val();
        if(msg != "") {
            chatManager.sendMessage($('#message-text').val());
            $('#message-text').val("");
        }
    }

    /**
     * Scrolls the chatfield to the bottom
     */
    this.updateScroll = function(){
        var chatContent = document.getElementById("chat-content");
        chatContent.scrollTop = chatContent.scrollHeight;
    }

    /**
     * clears chat-content and the message-inputfield
     */
    this.emptyConversation = function() {
        $('#chat-content').empty();
        $('#chat-message').empty();
    };

    /**
     * Appends the inputfield for chatmessages to the chatwindow
     */
    //TODO: Hier Dictionary für Ausgabe beachten
    this.appendChatMessageInput = function() {
        var htmlString = '<input id="message-text" type="text" class="form-control" placeholder="Your Message" aria-describedby="sizing-addon2">' +
            '<span id="send-message" class="input-group-addon btn">' +
            '<span class="fa fa-send fa-lg"></span>' +
            '</span>';
        $('#chat-message').append(htmlString);
        $('#send-message').click(function(){
           that.writeMessage();
        });
    };

    /**
     * removes all
     * @param elements
     */
    var removeButtonClasses = function() {
        var elements = $('.chat-btn');
        elements.removeClass('btn-primary');
        elements.removeClass('btn-default');
        elements.addClass('btn-default');
    };

    /**
     * activates the chatbutton by highlighting it
     * @param chatId = id for which chat should be activated as Integer
     */
    this.activateChat = function(chatId) {
        this.emptyConversation();
        overviewState = false;
        chatManager.changeConversation(chatId); //calls emptyConversation and
        this.appendChatMessageInput();
        this.emptyChatButtonBadge(chatId);

        removeButtonClasses();

        var element = $(document).find("[data-chat-id='" + chatId + "']");
        element.removeClass('btn-default');
        element.addClass('btn-primary');
    };

    /**
     * Used as clicklistener, closes an active chat
     * @param chatId = id for which chat should be closed as Integer
     */
    this.closeChat = function(chatId) {
        console.log("closed");
        var element = $(document).find("[data-chat-id='" + chatId + "']");
        element.parent().remove();
        chatManager.closeConversation(chatId);
        if($('#chat-buttons').children().length < 1) {
            this.activateOverview();
        }
    };

    /**
     * deletes chat-content and sets it with chatoverview DOM
     */
    //TODO: Hier Dictionary für Ausgabe beachten
    this.activateOverview = function() {

        this.emptyConversation();
        overviewState = true;
        removeButtonClasses();
        chatManager.requestConversations();

        var overViewHtmlString = '<h2>Open Projectchat</h2>' +
            '<ul id="group-chats" class="nav nav-pills"></ul>' +
            '<h2>Open Chat with a single person</h2>' +
            '<ul id="person-chats" class="nav nav-pills"></ul>';
        $('#chat-content').append(overViewHtmlString);

    };

    /**
     * Calls appendPossibleChatButton for every Item in the given arrays
     * @param projects = Object-Array which contains projectchats
     * @param users = Object-Array which contains single userchats
     */
    this.addConversationsToOverview = function(projects, users) {
        for(var i = 0; projects.length>i; i++) {
            this.appendPossibleChatButton(projects[i].name, "group", projects[i].id);
        }

        for(var i = 0; users.length>i; i++) {
            this.appendPossibleChatButton(users[i].name, "user", users[i].id);
        }
    };

    /**
     * Appends a conversation Button to chatOverview
     * @param chatname = chatname to be shown as String
     * @param chatType = "group" or anything else
     * @param chatId = Integer
     */
    this.appendPossibleChatButton = function(chatname, chatType, chatId) {
        if(chatType == "group") {
            var buttonHtmlString = '<li role="presentation" class="active psbl-chat-btn"><a href="#">' +
                '<span class="fa fa-users"></span>'
                + chatname +
                '</a></li>';
            var element = $('#group-chats').append(buttonHtmlString);
            element.click(function(){
                chatManager.addConversation(chatId, chatname);
                that.activateChat(chatId);
            });
        } else {
            var buttonHtmlString = '<li role="presentation" class="active psbl-chat-btn"><a href="#">' +
                '<span class="fa fa-user"></span>'
                + chatname +
                '</a></li>';
            var element = $('#person-chats').append(buttonHtmlString);
            element.click(function(){
                chatManager.addConversation(chatId, chatname);
                that.activateChat(chatId);
            });
        }

    };

    /**
     * Routine when Chatwindow is toggled up
     */
    this.chatPanelToggleUpCycle = function() {
        this.removeBadge();
        this.updateScroll();
        localStorage.setItem("chatToggleStatus", true);
    };

    /**
     * Routine when Chatwindow is toggled down
     */
    this.chatPanelToggleDownCycle = function() {
        this.addBadge();
        localStorage.setItem("chatToggleStatus", false);
    };

    var formatTime = function(timestamp) {
        var now = new Date();
        var time = new Date(timestamp);
        var formatedTimestamp;
        if ((time.getDate() == now.getDate()) && (time.getMonth() == now.getMonth()) && (time.getFullYear() == now.getFullYear())) {
            formatedTimestamp = ("0" + time.getHours()).slice(-2) + ":" + ("0" + time.getMinutes()).slice(-2);
        } else {
            formatedTimestamp = time.getDate() + "." + (time.getMonth()+1) + "." + time.getFullYear() + " " + formatedTimestamp;
        }
        return formatedTimestamp;
    };

};


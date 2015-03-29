// toggle box and indicator icons
$(document).on('click', '.toggle_header', function() {
    if($(this).parent().attr('id') == "chat-panel") {
        chatToggle($(this));
    } else {
        $(this).next('.toggle_content').slideToggle();

        var iconHolderFirst = $(this).children().first();
        var iconHolderLast = $(this).children().last();

        if(iconHolderFirst.hasClass('fa-chevron-right') || iconHolderFirst.hasClass('fa-chevron-down')) {
            toggleIcon(iconHolderFirst);
        } else {
            toggleIcon(iconHolderLast);
        }
    }
});

/**
 * changes toggle indicator icon (open / closed) for given jquery element
 * @param iconHolder element with
 */
function toggleIcon(iconHolder) {
    if(iconHolder.hasClass('fa-chevron-right')) {
        iconHolder.removeClass('fa-chevron-right');
        iconHolder.addClass('fa-chevron-down');
    }
    else if(iconHolder.hasClass('fa-chevron-down')) {
        iconHolder.removeClass('fa-chevron-down');
        iconHolder.addClass('fa-chevron-right');
    }
}

/**
 * chatToggle function
 * @param chatHeader chatHeader bar
 */
function chatToggle(chatHeader) {
    var iconHolderFirst = chatHeader.children().first();

    if(iconHolderFirst.hasClass('fa-chevron-right')) {
        chatHeader.next('.toggle_content').slideToggle();
        toggleIcon(iconHolderFirst);
        chatUi.chatPanelToggleUpCycle();

    }else if(iconHolderFirst.hasClass('fa-chevron-down')) {
        // if we're minimizing it, we only want the new messages badge AFTER the transition is complete
        chatHeader.next('.toggle_content').slideToggle(function(){
            toggleIcon(iconHolderFirst);
            chatUi.chatPanelToggleDownCycle();
        });
    }
}

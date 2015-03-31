// toggle box and indicator icons
$(document).on('click', '.toggle_header', function() {

    var header = $(this);
    if($(this).parent().attr('id') == "chat-panel") {
        chatToggle($(this));
    } else {

        if(header.hasClass('rounded-bottom-border') && header.hasClass('list-group-item')) {
            header.removeClass('rounded-bottom-border');
        }

        $(this).next('.toggle_content').slideToggle(function() {
            var iconHolderFirst = header.children().first();
            var iconHolderLast = header.children().last();

            if(iconHolderFirst.hasClass('fa-chevron-right') || iconHolderFirst.hasClass('fa-chevron-down')) {
                toggleIcon(iconHolderFirst);
            } else {
                toggleIcon(iconHolderLast);
            }

            //If togglecontent is list-group and not panel
            if(header.hasClass('list-group-item')) {
                var iconHolderLast = header.children().last();
                if (iconHolderLast.hasClass('fa-chevron-down')) {
                    // togglein and add rounded corners
                    header.removeClass('rounded-bottom-border');
                    header.addClass('no-rounded-bottom-border');
                } else if(header.hasClass('list-group-item') && iconHolderLast.hasClass('fa-chevron-right')){
                    // toggleout remove rounded corners
                    header.removeClass('no-rounded-bottom-border');
                    header.addClass('rounded-bottom-border');
                }
            }
        });
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

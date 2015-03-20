// toggle box and indicator icons
$(document).on('click', '.toggle_header', function() {
    $(this).next('.toggle_content').slideToggle();

    var iconHolderFirst = $(this).children().first();
    var iconHolderLast = $(this).children().last();

    if(iconHolderFirst.hasClass('fa-chevron-right') || iconHolderFirst.hasClass('fa-chevron-down')) {
        toggleIcon(iconHolderFirst, $(this));
    } else {
        toggleIcon(iconHolderLast, $(this));
    }

});

/**
 * changes toggle indicator icon (open / closed) for given jquery element
 * @param iconHolder
 */
function toggleIcon(iconHolder, element){
    if(iconHolder.hasClass('fa-chevron-right')) {
        iconHolder.removeClass('fa-chevron-right');
        iconHolder.addClass('fa-chevron-down');
        if(element.parent().attr('id') == "chat-panel") {
            removeBadge();
        }
    }
    else if(iconHolder.hasClass('fa-chevron-down')){
        iconHolder.removeClass('fa-chevron-down');
        iconHolder.addClass('fa-chevron-right');
        if(element.parent().attr('id') == "chat-panel") {
            addBadge();
        }
    }
}

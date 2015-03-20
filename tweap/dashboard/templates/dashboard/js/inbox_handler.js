{% load i18n %}
$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});

$(document).on('click', '#clearAllNotifications', function() {
    data = {};

    $.post("{% url 'notification_center:mark_all_seen' %}", data, function(result){

        var notificationElements = $('.notification-item');

        var invitationItems = $('.invitation-item');
        if(invitationItems.length == 0) {

            $('#inbox').parent().parent().slideUp(function() {
                notificationElements.remove();
            })
        }
        else {
            notificationElements.slideUp(function() {
                notificationElements.remove();
            });
        }
    });
});

//Notificationhandling
$(document).on('click', '.markNotificationSeen', function(){

    var notificationId = $(this).attr('data-notification-id');
    var data = {
        notificationId:notificationId
    };

    $.post("{% url 'notification_center:mark_seen' %}", data, function(output){
        manageNotificationAjaxRequest(output, notificationId)
    });
});

function manageNotificationAjaxRequest(output, notificationId){
    console.log("ajax request");
    if(output['state'] == true) {
        console.log(notificationId);
        $('#notification_container_id_' + notificationId).hide('slow', function() {
            $('#notification_container_id_' + notificationId).remove();
        });
    }

    if ($('#inbox-inner').children().length <= 1){
        removeInboxContainer();
    }
}

//Invitationhandling
$(document).on('click', '.acceptInvitation', function() {
    var invitationId = $(this).attr('data-invitation-id');
    var data = {
        action:"accept",
        invitation_id:invitationId
    };

    $.post("{% url 'project_management:invitation_handler' %}", data, function(output){
        manageInvitationAjaxRequest(output, invitationId)
    });
});

$(document).on('click', '.rejectInvitation', function() {
    var invitationId = $(this).attr('data-invitation-id');
    var data = {
        action: "reject",
        invitation_id: invitationId
    };

    $.post("{% url 'project_management:invitation_handler' %}", data, function(output){
        manageInvitationAjaxRequest(output, invitationId)
    })
});

function manageInvitationAjaxRequest(output, invitationId){
    if(output['url'] != ""){
        //Accepted
       var  url = output['url'];
        window.location.href = url;
    } else{
        $('#invitation_container_id_'+invitationId).hide('slow', function() {
            $('#invitation_container_id_' + invitationId).remove();
        });

        if ($('#inbox-inner').children().length <= 1){
            removeInboxContainer();
        }
    }
}

function removeInboxContainer(){
    var inbox = $('#inbox');
    inbox.parent().parent().hide('slow', function(){
        inbox.parent().parent().remove();
    });
}

{% load i18n %}
$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});

$(document).on('click', '.acceptInvitation', function() {
    var invitationId = $(this).attr('data-invitation-id');
    var data = {
        action:"accept",
        invitation_id:invitationId
    };

    $.post("{% url 'project_management:invitation_handler' %}", data, function(output){
        manageInvitationAjaxRequest(output)
    })
});

$(document).on('click', '.rejectInvitation', function() {
    var InvitationId = $(this).attr('data-invitation-id');
    var data = {
        action: "reject",
        invitation_id: InvitationId
    };

    $.post("{% url 'project_management:invitation_handler' %}", data, function(output){
        manageInvitationAjaxRequest(output)
    })
});

function manageInvitationAjaxRequest(output){
    if(output['url'] != ""){
        //Accepted
       var  url = output['url'];
        window.location.href = url;
    } else{
        var invitationId = output['id'];
        $('#invitation_container_id_'+invitationId).hide('slow', function() {
            $('#invitation_container_id_' + invitationId).remove();
        });

        if ($('#inbox').children().length == 2){
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

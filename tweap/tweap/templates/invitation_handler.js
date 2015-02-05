{% load i18n %}
$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});

$(document).on('click', '.acceptInvitation', function() {
    var id = (this).id
    var data = {
        action:"accept",
        invitation_id:id
    };

    $.post("{% url 'project_management:invitation_handler' %}", data, function(output){
        manageInvitationAjaxRequest(output)
    })
});

$(document).on('click', '.rejectInvitation', function() {
    var id = (this).id
    var data = {
        action: "reject",
        invitation_id: id
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
    }else{
        var invitation_id = output['id'];
        $('#invitation_container_id_'+invitation_id).hide('slow', function() {
            $('#invitation_container_id_' + invitation_id).remove();
        });

        if ($('#invitation_list').children().length == 2){
            removeInvitationContainer();
        }
    }
}

function removeInvitationContainer(){
    var invitationList = $('#invitation_list');
    invitationList.parent().parent().hide('slow', function(){
        invitationList.parent().parent().remove();
    });
}

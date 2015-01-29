{% load i18n %}
$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});

$(document).on('click', '.acceptInvitation', function() {
    id = (this).id
    data = {
        action:"accept",
        invitation_id:id
    };

    $.post("{% url 'project_management:invitation_handler' %}", data, function(output){
        manageInvitationAjaxRequest(output)
    })
});

$(document).on('click', '.rejectInvitation', function() {
    id = (this).id
    data = {
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
        url = output['url'];
        window.location.href = url;
    }else{
        invitation_id = output['id'];
        $('#invitation_container_id_'+invitation_id).remove();
        inviteNavText = $('#invitations_link').text();
        amountOfInvites = parseInt(inviteNavText);
        newAmountOfInvites = amountOfInvites - 1;
        $('#invitations_link').text("" + newAmountOfInvites);
    }
}

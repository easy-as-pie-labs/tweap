$(document).on('click', '.acceptInvitation', function() {
    id = (this).id
    data = {action:"accept", inviation_id:id};
    $.get("{% url 'project_management:invitation_handler' %}", data, function(output){
        manageInvitationAjaxRequest(output)
    })
});

$(document).on('click', '.rejectInvitation', function() {
    id = (this).id
    data = {action:"reject", inviation_id:id};
    $.get("{% url 'project_management:invitation_handler' %}", data, function(output){
        manageInvitationAjaxRequest(output)
    })
});

function manageInvitationAjaxRequest(output){
    console.log(output);
}

{% load i18n %}
var ENTER_KEY = 13;
var SPACE_KEY = 32;
var TAB_KEY = 9;
var highlightedSuggestion;


$(document).ready(function() {
    highlightedSuggestion = null;
    invitationList = new Invitations();

    $('<p id="project_icon"><i id="projectIcon" name="projectIcon" class="{{ project.icon|default:"fa fa-folder-open-o" }} project_icon" data-toggle="modal" data-target="#projectIconModal"></i> {% trans "Click icon to change it" %}</p>')
        .insertAfter('#icon-label');
    $('label[for=id_icon]').attr('for', 'projectIcon');

    var projectIconClass = '{{ project.icon|default:"fa fa-folder-open-o" }}';
    projectIconClass = "." + projectIconClass.split(" ")[1];
    var active = $('#projectIconModal').find(projectIconClass);
    $(active).addClass('project_icon_chosen');

    //removes title warning
    $('#id_name').keydown(function() {
        $('#name_warning').hide('slow');
        $('#id_name').parent().removeClass('has-error');
    });

    //checks if name is missing, prevent form submit and shows warning
    $('#project-form').submit(function() {
        if (!$('#id_name').val()) {
            $('#name_warning').show('slow');
            $('#id_name').parent().addClass('has-error');
            return false;
        }
        else {
            return true;
        }
    });
});

//object for managing invitations
var Invitations = function() {
    this.Invitations = new Array();

    this.add = function(userToAdd) {
        this.Invitations.push(userToAdd);
        $('#invitation-list').append('<p class="tag-outer"><span class="tag"><i class="fa fa-times-circle"></i>' + userToAdd + '</span></p>');
        $('#invitations').val(JSON.stringify(this.Invitations));
    }

    this.remove = function(userToRemove) {
        var index = this.Invitations.indexOf(userToRemove);
        if (index > -1) {
            this.Invitations.splice(index, 1);
        }
        $('#invitations').val(JSON.stringify(this.Invitations));
    }
}

//adds click listener to the icons in modal
$(document).on('click', '.project_icon_choose', function() {
    $('.project_icon_chosen').removeClass('project_icon_chosen');
    $(this).addClass('project_icon_chosen');
    var icon_class = $('.project_icon_chosen').attr('id');
    $('#projectIcon').removeClass().addClass('project_icon ' + icon_class);
    $('input[name=icon]').val(icon_class);
    $('#projectIconModal').modal('hide');
});


//overwrites enter to submit form when typing in user input field and adds text as user
$(document).on('keydown', '#user-input', function(e) {
    if ( e.which == ENTER_KEY || e.which == SPACE_KEY || e.which == TAB_KEY) {
        e.preventDefault();
    }
});

$(document).on('keyup', '#user-input', function(e) {
    var suggestions = $('#suggestions');
    if ( e.which == ENTER_KEY || e.which == SPACE_KEY) {
        if ( highlightedSuggestion == null)
            checkInputFieldAndInviteUser();
        else {
            var username = highlightedSuggestion.attr('id');
            inviteUserFromSuggestion(username);
        }


        highlightedSuggestion = null;
        e.preventDefault();
    } else if (e.which == TAB_KEY ) {

        if ( highlightedSuggestion == null ) {
            highlightedSuggestion = suggestions.children().first();
        } else {
            highlightedSuggestion.children().first().css( "color", "white" );
            id = highlightedSuggestion.attr('id');
            highlightedSuggestion = $('#'+id).next();

            if( highlightedSuggestion.length == 0 ) {
                highlightedSuggestion = suggestions.children().first();
            }
        }
        e.preventDefault();
    }
    else {
        highlightedSuggestion = null;
        typedText = $('#user-input').val();
        data = {search:typedText};
        $.get("{% url 'user_management:user_suggestion' %}", data, function(output){
            manageUserSuggestionAjaxRequest(output)
        })
    }

    if ( highlightedSuggestion != null )
        highlightedSuggestion.children().first().css( "color", "red" );

});

//adds clicked suggestion to invitation-list
$(document).on('click', '.suggestion', function() {
    addUserAndCleanInput($(this).attr('id'));
});

//listener for add tag button
$(document).on('click', '.addUserButton', function() {
    checkInputFieldAndInviteUser();
});


//checks if user input has value and add it as user or show error
function checkInputFieldAndInviteUser() {
    // if input is empty, prevent user adding
    if(!$('#user-input').val()) {
        // focus on empty field and give error class
        $('#user-input').focus();
        $('#user-input').attr("placeholder", "{% trans 'Type in username or email' %}");
        $('#user-input').parent().parent().addClass('has-error');
    }
    else {
         $('#user-input').parent().parent().removeClass('has-error');
        var newUser = $('#user-input').val();
        addUserAndCleanInput(newUser);
    }
}

function inviteUserFromSuggestion(username) {
    $('#user-input').parent().parent().removeClass('has-error');
    addUserAndCleanInput(username);
}

//adds new user to the invitation-list and cleans the user-input
function addUserAndCleanInput(newUser) {
     invitationList.add(newUser);
    $('#user-input').val("");
    $('#user-input').attr("placeholder", "{% trans 'Type in username or email' %}");
    $('#suggestions').empty();
    $('#user-input').focus();
}

//handles ajax response
function manageUserSuggestionAjaxRequest(data) {
    $('#suggestions').empty();
    for(i=0;i<data.length;i++){
        addSuggestionToContent(data[i]);
    }
}
//adds tag suggestion to the suggestions div
function addSuggestionToContent(userSuggestion) {
    $('#suggestions').append(
        '<h3 class="suggestion" id="' + userSuggestion + '"><span class="label label-info focus-pointer">' + userSuggestion + '</span></h3>'
    );
}

//remove user from invitation-list and array when clicked
$(document).on('click', '.tag', function() {
    var userToRemove = $(this).attr('data-tag-name');
    invitationList.remove(userToRemove);
    $(this).parent().remove();
});


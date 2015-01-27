$(document).ready(function(){
   newMembers = new Members();
});

//Adds new Inputfields
$(document).on('click', '.addUserButton', function() {

        // if input is empty, prevent user adding
        if(!$(this).prev().val()) {

            // focus on empty field and give error message
            $(this).prev().focus();
            $(this).prev().attr("placeholder", "Bitte Username oder Email ausfüllen");
            $(this).parent().parent().addClass('has-error');
        }

        // if input is there add new field, make old field uneditable and removable
        else {

            $('.addUserButton').addClass('removeUserButton');
            $('.addUserButton').removeClass('addUserButton');

            $('.removeUserButton').children().first().removeClass('glyphicon-plus-sign');
            $('.removeUserButton').children().first().addClass('glyphicon-minus-sign');

            $('.removeUserButton').prev().attr("disabled", true);

            $('.removeUserButton').parent().parent().removeClass('has-error');

            $('#newInputs').prepend(
                    "<div class='form-group'><div class='input-group date'><input id='users' type='text' placeholder='Username oder Email angeben' class='form-control member'><span class='input-group-addon addUserButton focus-pointer'><i class='glyphicon glyphicon-plus-sign'></i></span></div></div>"
            );

            $('.removeUserButton').click(function(){
                $(this).parent().parent().remove();
            })
        }
    });

//Ajax-Request for Usersuggestions
$(document).on('keyup', '#users', function(){
    typedText = (this).value
    //xml-request:
    data = {search:typedText};
    $.get("./../../users/user_suggestion", data, function(output){
        manageUserSuggestionAjaxRequest(output)
    })

});

//Puts the ID of an Suggestionelement into the value of the first inputelement in #newInputs
$(document).on('click', '.suggestion', function() {
    suggestionId = $(this).attr('id');
    firstInput = $('#newInputs').find('input[type=text]').filter(':visible:first')
    firstInput.val(suggestionId);
});

function manageUserSuggestionAjaxRequest(data){
    $('#suggestions').empty();
    for(i=0;i<data.length;i++){
        addSuggestionToContent(data[i]);
    }
}

function addSuggestionToContent(id) {
    $('#suggestions').append(
        '<h3 class="suggestion" id="' + id + '"><span class="label label-info focus-pointer">' + id + '</span></h3>'
    );
}

function insertHiddenValues(){
    inputMemberArr = $("#newInputs .member");

    for(i=0;i<inputMemberArr.length;i++){
        newMembers.addUser(inputMemberArr.eq(i).val());
    }

    console.log(newMembers.getUsersString());
}

var Members = function(){
    this.Users = new Array();

    this.addUser = function(added_user){
        this.Users.push(added_user)
    }

    this.getUsersString = function() {
        return JSON.stringify(this.Users);
    }
}
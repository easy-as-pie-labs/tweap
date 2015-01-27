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
                    "<div class='form-group'><div class='input-group date'><input id='users' type='text' placeholder='Username oder Email angeben' class='form-control'><span class='input-group-addon addUserButton focus-pointer'><i class='glyphicon glyphicon-plus-sign'></i></span></div></div>"
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
        addSuggestionToContent(output);
    })

});

//Puts the ID of an Suggestionelement into the value of the first inputelement in #newInputs
$(document).on('click', '.suggestion', function() {
    suggestionId = $(this).attr('id');
    firstInput = $('#newInputs').find('input[type=text]').filter(':visible:first')
    console.log(firstInput);
    firstInput.val(suggestionId);
});

function addSuggestionToContent(id){
    $('#suggestions').append(
                    '<h3 class="suggestion" id="' + id + '"><span class="label label-info focus-pointer">' + id + '</span></h3>'
            );
}

var Members = function(){
    this.Users = new Array();

    this.addUser = function(added_user){
        this.Users.push(added_user)
    }

    this.print_users = function(){
        for(i=0;i<this.Users.length;i++){
            console.log(this.Users[i]);
        }
    }
}
{% load i18n %}

//Adds new Inputfields
$(document).on('click', '.addTagButton', function() {

    // if input is empty, prevent user adding
    if(!$(this).prev().val()) {
        // focus on empty field and give error message
        $(this).prev().focus();
        $(this).prev().attr("placeholder", "{% trans 'Add Tag' %}");
        $(this).parent().parent().addClass('has-error');
    }
    else {
        addTagInput();
    }
});

// if input is there add new field, make old field uneditable and removable
function addTagInput(){
    $('.addTagButton').addClass('removeTagButton');
    $('.addTagButton').removeClass('addTagButton');

    $('.removeTagButton').children().first().removeClass('glyphicon-plus-sign');
    $('.removeTagButton').children().first().addClass('glyphicon-minus-sign');

    $('.removeTagButton').prev().attr("disabled", true);

    $('.removeTagButton').parent().parent().removeClass('has-error');

    $('#newInputs').prepend(
        "<div class='form-group'><div class='input-group symbol'><input id='tags' type='text' placeholder='{% trans "Add Tag" %}' class='form-control tag'><span class='input-group-addon addTagButton focus-pointer'><i class='glyphicon glyphicon-plus-sign'></i></span></div></div>"
    );

    $('#suggestions').remove();
    $('#newInputs div:first-child').after("<div id='suggestions'></div>");

    $('.removeTagButton').click(function(){
        $(this).parent().parent().remove();
    })
}

//Ajax-Request for Usersuggestions
$(document).on('keyup', '#tags', function(){
    typedText = (this).value
    //AJAX-Request:
    data = {search:typedText, project_id:"{{ project.id }}"};
    $.get("{% url 'project_management:tag_suggestion' %}", data, function(output){
        manageTagSuggestionAjaxRequest(output)
    })

});

//Puts the ID of an Suggestionelement into the value of the first inputelement in #newInputs and adds a new inputField
$(document).on('click', '.suggestion', function() {
    suggestionId = $(this).attr('id');
    firstInput = $('#newInputs').find('input[type=text]').filter(':visible:first')
    firstInput.val(suggestionId);
    addTagInput();
});

/*
is called on an AjaxRequest - deletes all #suggestion-HTMLElements
and calls addSuggestionsToContent. Adding of the HTMLElements is done for each
User inside the data-Array.
 */
function manageTagSuggestionAjaxRequest(data){
    $('#suggestions').empty();
    for(i=0;i<data.length;i++){
        addSuggestionToContent(data[i]);
    }
}

/*
adds #suggestions-HTMLElements over the inputs.
 */
function addSuggestionToContent(id) {
    $('#suggestions').append(
        '<h3 class="suggestion" id="' + id + '"><span class="label label-info focus-pointer">' + id + '</span></h3>'
    );
}

//Adds Userarray-JSONString to Hiddenfield
function insertHiddenValues(){
    inputTagArr = $("#newInputs .tag");

    for(i=0;i<inputTagArr.length;i++){
        newTags.addTag(inputTagArr.eq(i).val());
    }

    $('#hiddenValues').val(newTags.getTagsString());
}

//Object is initialized on the very Beginning of this document
var Tags = function(){
    this.Tags = new Array();

    //Adds new Userstring to Users-Array (Attribute)
    this.addTag = function(added_user){
        this.Tags.push(added_user)
    }

    //Stringifies the Users-Arrayattribute and returns it
    this.getTagsString = function() {
        return JSON.stringify(this.Tags);
    }
}

$(document).ready(function(){
   newTags = new Tags();
    $('#due_date_warning').hide();

    $('#due_date').change(function() {
        var dueDate = new Date($('#due_date').val());
        var today = new Date();
        if (dueDate < today) {
            $('#due_date_warning').show('slow');
        } else {
            $('#due_date_warning').hide('slow');
        }
    });
});

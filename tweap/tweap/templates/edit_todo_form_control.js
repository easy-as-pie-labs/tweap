{% load i18n %}

//Listener for add tag button
$(document).on('click', '.addTagButton', function() {
    // if input is empty, prevent user adding
    if(!$(this).prev().val()) {
        // focus on empty field and give error message
        $(this).prev().focus();
        $(this).prev().attr("placeholder", "{% trans 'Add Tag' %}");
        $(this).parent().parent().addClass('has-error');
    }
    else {
        $(this).parent().parent().removeClass('has-error');
        addTagInput();
    }
});

// adds tag from input to tag-list, cleans tag input field, refreshes tag-array
function addTagInput(){
    var newTagName = $('#tag-input').val();
    tagList.add(newTagName);
    $('#tag-list').append('<span class="tweap-tag label label-primary" id="' + newTagName + '"><i class="fa fa-tag"></i> ' + newTagName + '</span>');
    $('#tag-input').val("");
    $('#tag-input').attr("placeholder", "{% trans 'Add Tag' %}");
}

//adds clicked suggestion to tag-list
$(document).on('click', '.suggestion', function() {
    var newTagName = $(this).attr('id');
    tagList.add(newTagName);
    $('#tag-list').append('<span class="tweap-tag label label-primary" id="' + newTagName + '"><i class="fa fa-tag"></i> ' + newTagName + '</span>');
    $('#suggestions').empty();
    $('#tag-input').val("");
    $('#tag-input').attr("placeholder", "{% trans 'Add Tag' %}");
});

//Ajax-Request for TagSuggestions
$(document).on('keyup', '#tag-input', function(){
    typedText = (this).value
    //AJAX-Request:
    data = {search:typedText, project_id:"{{ project.id }}"};
    $.get("{% url 'project_management:tag_suggestion' %}", data, function(output){
        manageTagSuggestionAjaxRequest(output)
    })
});

/*
is called on an AjaxRequest - Response
deletes all suggestions and adds the suggestions from the response
 */
function manageTagSuggestionAjaxRequest(data){
    $('#suggestions').empty();
    for(i=0;i<data.length;i++){
        addSuggestionToContent(data[i]);
    }
}

/*
adds #suggestions-HTMLElements under the inputs.
 */
function addSuggestionToContent(newTagName) {
    $('#suggestions').append(
        '<h3 class="suggestion" id="' + newTagName + '"><span class="label label-info focus-pointer">' + newTagName + '</span></h3>'
    );
}

//removes tags when clicked from tag-list and Array
$(document).on('click', '.tweap-tag', function() {
    var tagToRemove = $(this).attr('id');
    tagList.remove(tagToRemove);
    $(this).remove();
});


//Object is initialized on the very Beginning of this document
var Tags = function(){
    this.Tags = new Array();

    //Adds new Userstring to Users-Array (Attribute)
    this.add = function(tagToAdd){
        this.Tags.push(tagToAdd);
        $('#tags').val(JSON.stringify(this.Tags));
    }

    this.remove = function(tagToRemove){
        this.Tags.pop(tagToRemove);
        $('#tags').val(JSON.stringify(this.Tags));
    }
}

$(document).ready(function(){
    tagList = new Tags();

    //add existing tags to tagList
    $('.tweap-tag').each(function() {
       tagList.add($(this).attr('id'));
    });

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

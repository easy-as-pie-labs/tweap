{% load i18n %}

//listener for add tag button
$(document).on('click', '.addTagButton', function() {
    checkInputFieldAndAddTag();
});

$(document).on('keydown', '#tag-input', function() {
    $('#tag-input').parent().parent().removeClass('has-error');
});

//overwrites enter to submit form when typing in tag input field and adds text as tag
$(document).on('keydown', '#tag-input', function(e) {
    if ( e.which == 13 ) {
        checkInputFieldAndAddTag();
        e.preventDefault();
    }
});

//adds clicked suggestion to tag-list
$(document).on('click', '.suggestion', function() {
    addTagAndCleanInput($(this).attr('id'));
});

//remove tag from tag-list and array when clicked
$(document).on('click', '.tag', function() {
    var tagToRemove = $(this).attr('data-tag-name');
    tagList.remove(tagToRemove);
    $(this).parent().remove();
});

//checks if tag input has value and add it as tag or show error
function checkInputFieldAndAddTag() {
    // if input is empty, prevent user adding
    if(!$('#tag-input').val()) {
        // focus on empty field and give error class
        $('#tag-input').focus();
        $('#tag-input').attr("placeholder", "{% trans 'Add Tag' %}");
        $('#tag-input').parent().parent().addClass('has-error');
    }
    else {
         $('#tag-input').parent().parent().removeClass('has-error');
        var newTagName = $('#tag-input').val();
        //remove special chars
        newTagName = newTagName.replace(/[<>\/|]/g, '').trim();
        if (newTagName == "") {
             $('#tag-input').val("");
            checkInputFieldAndAddTag();
            return;
        }
        addTagAndCleanInput(newTagName);
    }
}

//adds a new tag to the tag-list and cleans the tag-input
function addTagAndCleanInput(newTagName) {
    tagList.add(newTagName);
    $('#tag-input').val("");
    $('#tag-input').attr("placeholder", "{% trans 'Add Tag' %}");
    $('#suggestions').empty();
    $('#tag-input').focus();
}

//ajax request for getting tag suggestions
$(document).on('keyup', '#tag-input', function(e) {
    typedText = (this).value;
    data = {search:typedText, project_id:"{{ project.id }}"};
    $.get("{% url 'project_management:tag_suggestion' %}", data, function(output){
        manageTagSuggestionAjaxRequest(output)
    })
});

//handles ajax response
function manageTagSuggestionAjaxRequest(data) {
    $('#suggestions').empty();
    for(i=0;i<data.length;i++){
        addSuggestionToContent(data[i]);
    }
}
//adds tag suggestion to the suggestions div
function addSuggestionToContent(newTagName) {
    $('#suggestions').append(
        '<h3 class="suggestion" id="' + newTagName + '"><span class="label label-info focus-pointer">' + newTagName + '</span></h3>'
    );
}

//object for managing tags
var Tags = function(){
    this.Tags = new Array();

    //for adding existing tags to array
    this.addInit = function(tagToAdd) {
        this.Tags.push(tagToAdd);
        $('#tags').val(JSON.stringify(this.Tags));
    }

    //Adds new Userstring to Users-Array (Attribute)
    this.add = function(tagToAdd) {
        this.Tags.push(tagToAdd);
        $('#tag-list').append('<p class="tag-outer"><span class="tag" data-tag-name="' + tagToAdd + '"><i class="fa fa-tag"></i>' + tagToAdd + '</span></p>');
        $('#tags').val(JSON.stringify(this.Tags));
    }

    this.remove = function(tagToRemove) {
        var index = this.Tags.indexOf(tagToRemove);
        if (index > -1) {
            this.Tags.splice(index, 1);
        }
        $('#tags').val(JSON.stringify(this.Tags));
    }
}

//initial stuff
$(document).ready(function(){
    tagList = new Tags();

    //add existing tags to tagList
    $('.tag').each(function() {
       tagList.addInit($(this).attr('data-tag-name'));
    });

    $('#title_warning').hide();

    $('#due_date_warning').hide();

    $('.input-group.date').datetimepicker({
        format: "YYYY-MM-DD"
    });

    var dueDatePicker = $('.input-group.date').data('DateTimePicker');

    $('#due_date').click(function() {
        dueDatePicker.toggle();
    });


    //checks if due date lies in past and show hint
    $('.input-group.date').on("dp.change",function () {
        var dueDate = new Date($('#due_date').val());
        var today = new Date();
        today = today.setDate(today.getDate() - 1);
        if (dueDate < today) {
            $('#due_date_warning').show('slow');
        } else {
            $('#due_date_warning').hide('slow');
        }
    });

    //removes title warning
    $('#title-input').keydown(function() {
        $('#title_warning').hide('slow');
        $('#title-input').parent().removeClass('has-error');
    });

    //checks if title is missing, prevent form submit and shows warning
    $('#todo-form').submit(function() {
        if(!$('#title-input').val()) {
            $('#title_warning').show('slow');
            $('#title-input').parent().addClass('has-error');
            return false;
        }
        else {
            return true;
        }
    });
});

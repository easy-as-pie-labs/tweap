{% load i18n %}
var ENTER_KEY = 13;
var SPACE_KEY = 32;
var TAB_KEY = 9;
var highlightedSuggestion;

//listener for add tag button
$(document).on('click', '.addTagButton', function() {
    checkInputFieldAndAddTag();
});

$(document).on('keydown', '#tag-input', function() {
    $('#tag-input').parent().parent().removeClass('has-error');
});

//overwrites enter to submit form when typing in tag input field and adds text as tag
$(document).on('keydown', '#tag-input', function(e) {
    if (e.which == ENTER_KEY || e.which == SPACE_KEY || e.which == TAB_KEY) {
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

function addTagFromSuggestion(tagname) {
    $('#tag-input').parent().parent().removeClass('has-error');
    addTagAndCleanInput(tagname);
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
    var suggestions = $('#suggestions');
    if ( e.which == ENTER_KEY || e.which == SPACE_KEY ) {
        if ( highlightedSuggestion == null ) {
            checkInputFieldAndAddTag();
        }
        else {
            var tagname = highlightedSuggestion.attr('id');
            addTagFromSuggestion(tagname);
        }

        highlightedSuggestion = null;
        e.preventDefault();
    } else if (e.which == TAB_KEY ) {

        if ( highlightedSuggestion == null ) {
            highlightedSuggestion = suggestions.children().first();
        } else {
            highlightedSuggestion.children().first().css( "color", "white" );
            var id = highlightedSuggestion.attr('id');

            // because the tag name is the id
            // and $(id) with special characters in the id isn't supported
            id = "p[id='"+id+"']";
            highlightedSuggestion = $(id).next();
            if( highlightedSuggestion.length == 0 ) {
                highlightedSuggestion = suggestions.children().first();
            }
        }
        e.preventDefault();
    }
    else {
        highlightedSuggestion = null;
        var typedText = $('#tag-input').val();
        var data = {search:typedText, project_id:"{{ project.id }}"};
        $.get("{% url 'project_management:tag_suggestion' %}", data, function(output){
            manageTagSuggestionAjaxRequest(output)
        })
    }

    if ( highlightedSuggestion != null )
        highlightedSuggestion.children().first().css( "color", "red" );

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
        '<p class="tag-outer-no-hover suggestion" id="'+newTagName+'"><span class="tag-no-hover" data-tag-name="'+newTagName+'"><i class="fa fa-tag"></i> '+newTagName+'</span></p>'
    );
}

//object for managing tags
var Tags = function(){
    this.Tags = [];

    //for adding existing tags to array
    this.addInit = function(tagToAdd) {
        this.Tags.push(tagToAdd);
        $('#tags').val(JSON.stringify(this.Tags));
    };

    //Adds new Userstring to Users-Array (Attribute)
    this.add = function(tagToAdd) {
        this.Tags.push(tagToAdd);
        $('#tag-list').append('<p class="tag-outer"><span class="tag" data-tag-name="' + tagToAdd + '"><i class="fa fa-tag"></i>' + tagToAdd + '</span></p>');
        $('#tags').val(JSON.stringify(this.Tags));
    };

    this.remove = function(tagToRemove) {
        var index = this.Tags.indexOf(tagToRemove);
        if (index > -1) {
            this.Tags.splice(index, 1);
        }
        $('#tags').val(JSON.stringify(this.Tags));
    }
};

//initial stuff
$(document).ready(function(){
    tagList = new Tags();

    //add existing tags to tagList
    $('.tag').each(function() {
       tagList.addInit($(this).attr('data-tag-name'));
    });

    $('.input-group.date').datetimepicker({
        format: "YYYY-MM-DD",
        stepping: 5,
        useCurrent: false,
        showClear: true,
        icons: {
            time: "fa fa-clock-o",
            date: "fa fa-calendar",
            up: "fa fa-arrow-up",
            down: "fa fa-arrow-down"
        }
    });


    $('#due_date').click(function() {
        $('.input-group.date').data('DateTimePicker').toggle();
    });

    //checks if due date lies in past and show hint
    $('.input-group.date').on("dp.change",function () {

        var pickedDate = $('.input-group.date').data('DateTimePicker').date();

        // if picked date day lies before right now day
        if (pickedDate.startOf('day').isBefore(moment().startOf('day'))) {
            $('#due_date_warning').show('slow');
        }
        else {
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

    $(document).on('click', '#assign_all', function() {
        if(this.checked) {
            // Iterate each checkbox
            $(':checkbox').each(function() {
                if(!this.disabled)
                    this.checked = true;
            });
        }
        else {
            $(':checkbox').each(function() {
                if(!this.disabled)
                    this.checked = false;
            });
        }
    });
});
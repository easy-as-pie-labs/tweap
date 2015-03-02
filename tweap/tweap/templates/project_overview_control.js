{% load i18n %}
//Ajax-Setup
$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});

$(document).ready(function () {
    $('.fa-square-o').hover(function () {
        $(this).removeClass('fa-square-o');
        $(this).addClass('fa-check-square-o');
    }, function () {
        $(this).removeClass('fa-check-square-o');
        $(this).addClass('fa-square-o')
    });
});

//Listener for all Done/Undone buttons of every Todoh
$(document).on('click', '.changeStateTodo', function(e) {
    var child = $(this).children('i');
    var todo_id = $(this).attr('data-todo-id');

    if(child.hasClass("fa-refresh")){
        sendChangeStateTodoAjaxRequest("unclear", todo_id, child);
    }else{
        sendChangeStateTodoAjaxRequest("clear", todo_id, child);
    }

    e.stopPropagation();
});

$(document).on('click', '.toggle_header', function() {
    $(this).next('.toggle_content').slideToggle();
});

//Actual Ajax-Request
function sendChangeStateTodoAjaxRequest(action, todo_id, child) {
    var data = {
        todo_id: todo_id
    };

    if(action == "clear") {
        $.post("{% url 'todo:mark_done' %}", data, function(output){
            changeStateToClear(output, child)
        })
    }

    if(action == "unclear") {
        $.post("{% url 'todo:mark_undone' %}", data, function(output){
            changeStateToUnclear(output, child)
        })
    }
}

//Changes Button and Todoh-Text to Clear-Status (Button is on repeat and Text is in <del></del>)
function changeStateToClear(output, child) {
    if(output['state'] == true) {
        var todo_item = child.parent().parent().parent();

        child.removeClass('fa fa-fw fa-square-o fa-lg');
        child.addClass('fa fa-fw fa-check-square-o fa-lg');

        todo_item.fadeOut(function() {
            todo_item.remove();
            $('#todo_closed_box').append(todo_item);

            child.removeClass('fa fa-fw fa-check-square-o fa-lg');
            child.addClass('fa fa-fw fa-refresh fa-lg');

            var panel_header = todo_item.first();
            panel_header.children().first().next('.toggle_content').hide();

            panel_header.removeClass("panel-danger");
            panel_header.removeClass("panel-warning");
            panel_header.addClass("panel-default");

            todo_item.fadeTo('default', 0.4);
        });
    }
}

//Changes Button and Todoh-Text to Unclear-Status (Button is on ok and Text is not in <del></del>)
function changeStateToUnclear(output, child) {
    if(output['state'] == true) {
        var todo_item = child.parent().parent().parent();

        todo_item.fadeOut(function() {
            todo_item.remove();
            $('#todo_rest_box').append(todo_item);
            // TODO: check due_date and give color accordingly?

            var panel_header = todo_item.first();
            panel_header.children().first().next('.toggle_content').hide();

            child.removeClass('fa fa-fw fa-refresh fa-lg');
            child.addClass('fa fa-fw fa-square-o fa-lg');

            todo_item.fadeTo('default', 1);

            child.hover(function () {
                $(this).removeClass('fa-square-o');
                $(this).addClass('fa-check-square-o');
            }, function () {
                $(this).removeClass('fa-check-square-o');
                $(this).addClass('fa-square-o')
            });
        });
    }
}
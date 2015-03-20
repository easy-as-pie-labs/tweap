{% load i18n %}
//Ajax-Setup
$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});

$(document).ready(function () {

    addHoverClassChange($('.hover-change'), 'fa-square-o', 'fa-check-square-o');

    addHoverClassChange($('.hover-reopen'), 'fa-check-square-o', 'fa-refresh');

});

$(document).on('click', '#quickTodo', function(e) {
    e.stopPropagation();
});

$(document).on('click', '#quickTodoButton', function(e) {
    var title = $('#quickTodo').val();
    quickAddTodo(title);
    e.stopPropagation();
});

$(document).on('keydown', '#quickTodo', function(e) {
    if ( e.which == 13 ) {
        var title = $('#quickTodo').val();
        quickAddTodo(title);
    }
});

var quickAddTodo = function(title) {
    console.log("add todo with title: " + title);

    // TODO: get current project differently (currently from url substring)

    var url = document.URL;
    var project_id = url.substr(url.lastIndexOf('/') + 1);

    var data = {
        project_id: project_id,
        title: title
    };

    $.post("{% url 'todo:quick_add' %}", data, function(output){
        console.log(output);

        // clear entered text if success
        if(output['success'] == true) {
            $('#quickTodo').val('')
        }
    })
};

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

//Actual Ajax-Request
function sendChangeStateTodoAjaxRequest(action, todo_id, child) {
    var data = {
        todo_id: todo_id
    };

    if(action == "clear") {
        $.post("{% url 'todo:mark_done' %}", data, function(output){
            changeStateToClear(output, child);
        })
    }

    if(action == "unclear") {
        $.post("{% url 'todo:mark_undone' %}", data, function(output){
            changeStateToUnclear(output, child);
        })
    }
}

//Changes Button and Todoh-Text to Clear-Status (Button is on repeat and Text is in <del></del>)
function changeStateToClear(output, child) {
    if(output['state'] == true) {
        var todo_item = child.parent().parent().parent();

        todo_item.fadeOut(function() {
            todo_item.remove();
            $('#todo_closed_box').append(todo_item);

            var panel_header = todo_item.first();

            // close open togglebox and change icon
            panel_header.children().first().next('.toggle_content').hide();
            panel_header.children().first().children().first().removeClass('fa-chevron-down');
            panel_header.children().first().children().first().addClass('fa-chevron-right');

            panel_header.removeClass("panel-danger");
            panel_header.removeClass("panel-warning");
            panel_header.addClass("panel-default");

            child.removeClass('fa fa-fw fa-square-o fa-lg');
            child.addClass('fa fa-fw fa-check-square-o fa-lg');

            todo_item.fadeTo('default', 0.4);

            addHoverClassChange(child, 'fa-check-square-o', 'fa-refresh');
        });
    }
}

//Changes Button and Todoh-Text to Unclear-Status (Button is on ok and Text is not in <del></del>)
function changeStateToUnclear(output, child) {
    if(output['state'] == true) {
        var todo_item = child.parent().parent().parent();

        todo_item.fadeOut(function() {
            todo_item.remove();

            //Get due_date from span of todoh
            var due_date = todo_item.find('.due-date');
            due_date = due_date.attr('data-date');
            due_date = new Date(due_date);

            //Get current date
            var currentDate = new Date();
            currentDate.setHours(1, 0, 0);


            //comparing due_date with current date to choose a color for todoh
            if(currentDate.getDate() === due_date.getDate() &&
                currentDate.getMonth() === due_date.getMonth() &&
                currentDate.getYear() === due_date.getYear()
            ) {
                todo_item.addClass("panel panel-warning");
                $('#todo_today_box').append(todo_item);
            }else if(currentDate > due_date) {
                todo_item.addClass("panel panel-danger");
                $('#todo_overdue_box').append(todo_item);
            }else {
                $('#todo_rest_box').append(todo_item);
            }




            var panel_header = todo_item.first();
            // close open togglebox and change icon
            panel_header.children().first().next('.toggle_content').hide();
            panel_header.children().first().children().first().removeClass('fa-chevron-down');
            panel_header.children().first().children().first().addClass('fa-chevron-right');

            child.removeClass('fa fa-fw fa-refresh fa-lg');
            child.addClass('fa fa-fw fa-square-o fa-lg');

            todo_item.fadeTo('default', 1);

            addHoverClassChange(child, 'fa-square-o', 'fa-check-square-o');
        });
    }
}

/**
 * adds jquery hover event
 * @param element jquery element
 * @param baseClass class shown on default
 * @param hoverClass class shown on hover
 */
function addHoverClassChange(element, baseClass, hoverClass) {
    element.hover(function () {
        $(this).removeClass(baseClass);
        $(this).addClass(hoverClass);
    }, function () {
        $(this).removeClass(hoverClass);
        $(this).addClass(baseClass);
    });
}
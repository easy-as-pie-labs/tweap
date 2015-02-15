{% load i18n %}
//Ajax-Setup
$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});

//Listener for all Done/Undone buttons of every Todoh
$(document).on('click', '.changeStateTodo', function() {
    var child = $(this).children('span');
    var todo_id = $(this).attr('data-todo-id');

    if(child.attr('class') == "glyphicon glyphicon-repeat"){
        sendChangeStateTodoAjaxRequest("unclear", todo_id, child);
    }else{
        sendChangeStateTodoAjaxRequest("clear", todo_id, child);
    }
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
        child.removeClass('glyphicon glyphicon-ok');
        child.addClass('glyphicon glyphicon-repeat');

        todoTd = child.parent().parent().prev().prev();
        todoTdText = todoTd.html();
        todoTd.html('<del>' + todoTdText + '</del>');
    }
}

//Changes Button and Todoh-Text to Unclear-Status (Button is on ok and Text is not in <del></del>)
function changeStateToUnclear(output, child) {
    if(output['state'] == true) {
        child.removeClass('glyphicon glyphicon-repeat');
        child.addClass('glyphicon glyphicon-ok');

        todoTd = child.parent().parent().prev().prev();
        todoTdText = todoTd.children().html();
        todoTd.html(todoTdText);
    }
}
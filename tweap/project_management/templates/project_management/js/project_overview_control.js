{% load i18n %}
//Ajax-Setup
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
});

var ENTER_KEY_CODE = 13;
var COMPLETED_TODO_LIMIT = 3;
var ASSIGN_ME_ICON = 'fa-star';
var UNASSIGN_ME_ICON = 'fa-star-o';
var todoState = 'hidden';

$(document).ready(function () {

    addHoverClassChange($('.hover-change'), 'fa-square-o', 'fa-check-square-o');

    addHoverClassChange($('.hover-reopen'), 'fa-check-square-o', 'fa-refresh');

    hideClosedTodos();

    addAssigmentActions();

});

var addAssigmentActions = function() {
    var assign_user = $('.'+ASSIGN_ME_ICON);
    var unassign_user = $('.'+UNASSIGN_ME_ICON);

    addAssignmentHover(assign_user, ASSIGN_ME_ICON, UNASSIGN_ME_ICON);
    addAssignmentHover(unassign_user, UNASSIGN_ME_ICON, ASSIGN_ME_ICON);
    // click on opposite icon, because of hover effect
    addAssignmentClick(unassign_user, "assign");
    addAssignmentClick(assign_user, "unassign");
};

/**
 * classchange on hover over element
 * @param element to change class of
 * @param from base clase
 * @param to hover class
 */
var addAssignmentHover = function(element, from, to){
    element.hover(function () {
        $(this).removeClass(from);
        $(this).addClass(to);
    }, function () {
        if($(this).attr('data-changed-state') == 'false') {
            $(this).removeClass(to);
            $(this).addClass(from);
        }
        else {
            // except if the user clicked
            $(this).attr('data-changed-state', 'true');

            // change hover effect
            addAssignmentHover($(this), to, from);
        }
    });
};

/**
 * adds assign / unassign click listener to element
 * @param element to add click listener to
 * @param type ["assign"|"unassign"] determines action to take
 */
var addAssignmentClick = function(element, type) {
    element.click(function() {
        var todoId = $(this).attr('data-todo-id');
        var that = this;

        if(type == "assign"){
            $.post("{% url 'todo:quick_assign' %}", { 'todo_id': todoId }, function (output) {
                if(output['success']) {
                    updateAssigned(output, that);
                }
            });
        }
        else if (type == "unassign") {
            $.post("{% url 'todo:quick_unassign' %}", { 'todo_id': todoId }, function (output) {
                if(output['success']) {
                    updateAssigned(output, that);
                }
            });
        }
    });
};

var updateAssigned = function(output, that){
    var id = output['id'];
    var users = output['users'];
    var tags = output['tags'];
    var title = output['title'];
    var assignment = output['assignment'];
    var year = output['year'];
    var month = output['month'];
    var day = output['day'];

    //Get current date
    var currentDate = new Date();
    currentDate.setHours(0, 0, 0);

    var due_date = new Date(year, month-1, day, 0, 0, 0, 0);

    var element = "";
    if(year == null){
        element = generateTodoDomElement(id, title, users, tags, assignment, "", 'default', 'open');
    } else if (currentDate.getDate() === due_date.getDate() &&
        currentDate.getMonth() === due_date.getMonth() &&
        currentDate.getYear() === due_date.getYear()
    ) {
        element = generateTodoDomElement(id, title, users, tags, assignment, due_date, 'warning', 'open');
    } else if (currentDate > due_date) {
        element = generateTodoDomElement(id, title, users, tags, assignment, due_date, 'danger', 'open');
    }

    $(that).parentsUntil($('.panel')).parent().replaceWith(element);

    var newElement = $('#element-' + id);
    var toggleIcon = newElement.find($('.toggle_header')).children().first();
    toggleIcon.removeClass('fa-chevron-right');
    toggleIcon.addClass('fa-chevron-down');

    newElement.show();
    newElement.find($('.toggle_content')).show();
    addAssigmentActions();
};

$(document).on('click', '#quickTodo', function (e) {
    e.stopPropagation();
});

$(document).on('click', '#quickTodoButton', function (e) {
    var title = $('#quickTodo').val();
    quickAddTodo(title);
    e.stopPropagation();
});

$(document).on('keydown', '#quickTodo', function (e) {
    if (e.which == ENTER_KEY_CODE) {
        var title = $('#quickTodo').val();
        quickAddTodo(title);
    }
});

/**
 * hides all closed todos (except the first x)
 * and shows a "show more todos" clickable text
 */
var hideClosedTodos = function() {
    $('#show-all').remove();
    $('#show-less').remove();
    var box = $('#todo_closed_box');
    var todos = box.children();
    for(var i = 0; i < todos.length; i++){
        if(i >= COMPLETED_TODO_LIMIT) {
            $(todos[i]).hide();
        }
    }

    if(todos.length >= COMPLETED_TODO_LIMIT){
        var surplus = todos.length - COMPLETED_TODO_LIMIT;
        box.append('<span id="show-all" class="noselect hover-underline cursor-pointer" style="margin: 10px;">show ' + surplus + ' more completed todos</span>');
        $('#show-all').click(function() {
            showClosedTodos();
        });
    }

    todoState = 'hidden';
};

/**
 * shows all closed todos and offers option to hide them again
 */
var showClosedTodos = function() {
    $('#show-all').remove();
    $('#show-less').remove();

    var box = $('#todo_closed_box');
    var todos = box.children();
    for(var i = 0; i < todos.length; i++){
        $(todos[i]).show();
    }

    if(todos.length >= COMPLETED_TODO_LIMIT){
        var surplus = todos.length - COMPLETED_TODO_LIMIT;
        box.append('<span id="show-less" class="noselect hover-underline cursor-pointer" style="margin: 10px;">{% trans "hide completed todos" %}</span>')
        $('#show-less').click(function(){
            hideClosedTodos();
        });
    }

    todoState = 'shown';
};

/**
 * toggled when the user hits enter or the plus button
 * in quick add todo box
 * @param title of new todoitem
 */
var quickAddTodo = function (title) {

    // TODO: get current project differently (currently from url substring)

    var url = document.URL;
    var project_id = url.substr(url.lastIndexOf('/') + 1);

    var data = {
        project_id: project_id,
        title: title
    };

    $.post("{% url 'todo:quick_add' %}", data, function (output) {

        // clear entered text if success
        if (output['success'] == true) {
            $('#quickTodo').val('');

            var id = output['id'];
            var users = output['users'];
            var tags = output['tags'];
            var title = output['title'];
            var assignment = output['assignment'];

            var element = generateTodoDomElement(id, title, users, tags, assignment, "", "default", "closed");

            $('#todo_rest_box').prepend(element);
            var newElement = $('#element-' + id);
            newElement.fadeIn();
            var hoverChange = $('#toggle-' + id);
            addHoverClassChange(hoverChange, 'fa-square-o', 'fa-check-square-o');
        }
    })
};

/**
 * generates todoelement
 * @param id - db id of element
 * @param title - title of todoelement
 * @param users - assigned users
 * @param tags - added tags
 * @param assignment - assignment string (you|none|someone)
 * @param due_date - due date
 * @param type - css header class ["default"|"warning"|"danger"]
 * @param toggleState - ["open"|"closed"]
 * @returns {string} - todoelement
 */
var generateTodoDomElement = function (id, title, users, tags, assignment, due_date, type, toggleState) {

    var monthNames = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"
        ];

    var url = "../todo/edit/" + id;

            var element = '<div class="panel panel-';
            element += type + '" style="margin: 7px; display: none" id="element-' + id + '">' +
                '<div class="panel-heading noselect toggle_header">' +
                    '<i class="fa fa-chevron-right"></i> ' + title +
                    ' <span data-todo-id="' + id + '" class="changeStateTodo pull-right">' +
                        '<i id="toggle-' + id + '"class="fa fa-fw fa-square-o fa-lg hover-change"></i>'+
                '</span>';

            if(assignment == "none") {
                element += '<span data-todo-id="'+id+'" class="assignee-marker pull-right"><i title="no one is currently working on this todo" class="fa fa-fw fa-exclamation fa-lg"></i></span>'
            }
            else if (assignment == "you") {
                element += '<span data-todo-id="'+id+'" class="assignee-marker pull-right"><i title="no one is currently working on this todo" class="fa fa-fw fa-eye fa-lg"></i></span>'
            }

            element +=
                '</div>' +
                '<div class="panel-body toggle_content hide-alert">' +
                    '<div class="todo-table">' +
                        '<div>' +
                            '<div>' +
                                '<i class="fa fa-fw fa-file-text-o"></i>' +
                            '</div>' +
                            '<div>' +
                                '{% trans "No description" %}' +
                            '</div>' +
                        '</div>' +
                        '<div class="todo-table-spacer"></div>' +
                            '<div>' +
                                '<div>' +
                                    '<i class="fa fa-fw fa-calendar"></i>' +
                            '</div>' +
                            '<div>';
    if (due_date == "")
        element += '{% trans "No due date" %}';
    else {
        element += monthNames[due_date.getMonth()] + " " + due_date.getDate() + ", " + due_date.getFullYear();
    }

    element +=
                            '</div>' +
                        '</div>' +
                        '<div class="todo-table-spacer"></div>' +
                            '<div>' +
                                '<div>' +
                                    '<i class="fa fa-fw fa-users"></i>' +
                                '</div>' +
                                '<div>';
            if (users.length == 0)
                element += '{% trans "No assigned users" %}';
            else {
                users.forEach(function (user) {
                    element += '<a href="../../users/profile/' + user + '" class="tag-outer"><span class="tag-no-interactive"><i class="fa fa-user"></i>' + user + '</span></a>';
                });
            }

            element +=
                '</div>' +
                '</div>' +
                '<div class="todo-table-spacer"></div>' +
                    '<div>' +
                        '<div>' +
                            '<i class="fa fa-fw fa-tags"></i>' +
                        '</div>' +
                        '<div>';

            if (tags.length == 0)
                element += '{% trans "No tags" %}';
            else {
                tags.forEach(function (tag) {
                    element += '<span class="tag-outer"><span class="tag-no-interactive" data-tag-name="' + tag + '"><i class="fa fa-tag"></i>' + tag + '</span></span>';
                });
            }

            element +=
                '</div>' +
                '</div>' +
                '</div>' +
                    '<hr style="margin-top:5px;margin-bottom:10px;">' +
                    '<span class="pull-right"><a href="' + url + '"><i style="color: #337AB7;" class="fa fa-lg fa-pencil-square-o"></i></a></span>';

            if(assignment == "you") {
                element += '<span class="unassignme-maker pull-right cursor-pointer noselect" style="margin-right: 5px;">'+
                                '<i data-changed-state="false" data-todo-id="'+id+'" style="color: #337AB7;" title="unassign yourself from this todo" class="fa fa-fw fa-star fa-lg"></i>'+
                            '</span>';
            }
            else {
                element += '<span class="assignme-marker pull-right cursor-pointer noselect" style="margin-right: 5px;">'+
                                '<i data-changed-state="false" data-todo-id="'+id+'" style="color: #337AB7;" title="assign yourself to this todo" class="fa fa-fw fa-star-o fa-lg"></i>'+
                            '</span>';
            }


            element +=
                '</div>' +
                '</div>';

    return element;

};

//Listener for all Done/Undone buttons of every Todoh
$(document).on('click', '.changeStateTodo', function (e) {
    var child = $(this).children('i');
    var todo_id = $(this).attr('data-todo-id');

    if (child.hasClass("fa-refresh")) {
        sendChangeStateTodoAjaxRequest("unclear", todo_id, child);
    } else {
        sendChangeStateTodoAjaxRequest("clear", todo_id, child);
    }

    e.stopPropagation();
});

//Actual Ajax-Request
function sendChangeStateTodoAjaxRequest(action, todo_id, child) {
    var data = {
        todo_id: todo_id
    };

    if (action == "clear") {
        $.post("{% url 'todo:mark_done' %}", data, function (output) {
            changeStateToClear(output, child);
        })
    }

    if (action == "unclear") {
        $.post("{% url 'todo:mark_undone' %}", data, function (output) {
            changeStateToUnclear(output, child);
        })
    }
}

//Changes Button and Todoh-Text to Clear-Status (Button is on repeat and Text is in <del></del>)
function changeStateToClear(output, child) {
    if (output['state'] == true) {
        var todo_item = child.parent().parent().parent();


        todo_item.fadeOut(function () {
            todo_item.remove();

            // hide assignment marker
            todo_item.find('.assignee-marker').hide();

            $('#todo_closed_box').prepend(todo_item);

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

            if(todoState == 'hidden')
                hideClosedTodos();
        });
    }
}

//Changes Button and Todoh-Text to Unclear-Status (Button is on ok and Text is not in <del></del>)
function changeStateToUnclear(output, child) {
    if (output['state'] == true) {
        var todo_item = child.parent().parent().parent();

        todo_item.fadeOut(function () {
            todo_item.remove();

            // show assignment marker
            todo_item.find('.assignee-marker').show();

            //Get due_date from span of todoh
            var due_date = todo_item.find('.due-date');
            due_date = due_date.attr('data-date');
            due_date = new Date(due_date);

            //Get current date
            var currentDate = new Date();
            currentDate.setHours(1, 0, 0);


            //comparing due_date with current date to choose a color for todoh
            if (currentDate.getDate() === due_date.getDate() &&
                currentDate.getMonth() === due_date.getMonth() &&
                currentDate.getYear() === due_date.getYear()
            ) {
                todo_item.addClass("panel panel-warning");
                $('#todo_today_box').prepend(todo_item);
            } else if (currentDate > due_date) {
                todo_item.addClass("panel panel-danger");
                $('#todo_overdue_box').prepend(todo_item);
            } else {
                $('#todo_rest_box').prepend(todo_item);
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

            if(todoState == 'hidden'){
                showClosedTodos();
                hideClosedTodos();
            }
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
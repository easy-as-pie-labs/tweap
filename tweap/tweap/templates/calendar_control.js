{% load i18n %}
$(document).ready(function() {

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        eventDrop: function(event, delta, revertFunc) {

            updateCalendarEntry(event);

            if (!confirm("Are you sure about this change?")) {
                revertFunc();
            }
        },
        eventResize: function(event, delta, revertFunc) {

            updateCalendarEntry(event);

            if (!confirm("is this okay?")) {
                revertFunc();
            }

        },
        events: [
            {% for event in events %}
            {
                title: '{{ event.title }}',
                start: '{{ event.get_start_for_cal }}',
                end: '{{ event.get_end_for_cal }}',
                url: '{% url "cal:edit" event.id %}',
                id: '{{ event.id }}'
            },
            {% endfor %}
        ],
    });

    var updateCalendarEntry = function(event){
        console.log(event.id + " now from " + event.start + " to " + event.end)

        var invitationId = $(this).attr('data-invitation-id');
        var data = {
            action: "change",
            event_id: event.id,
            start: event.start,
            end: event.end
        };
        /*
        $.post("{% url 'project_management:invitation_handler' %}", data, function(output){
            manageInvitationAjaxRequest(output, invitationId)
        });*/
    };

});
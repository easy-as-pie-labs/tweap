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
            updateCalendarEntry(event, revertFunc);
        },
        eventResize: function(event, delta, revertFunc) {
            updateCalendarEntry(event, revertFunc);
        },
        dayClick: function(date, jsEvent, view) {
            // trigger create event modal with date data pre-filled

            // start date from clicked datetime
            startDate = date;

            // end date one hour later
            endDate = moment(date).add(1, 'h');

            // pre-fill data and trigger modal
            $('#start_date').val(startDate.format("YYYY-MM-DD hh:mm A"));
            $('#end_date').val(endDate.format("YYYY-MM-DD hh:mm A"));
            $('#new_cal_modal').modal('show');
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

    var updateCalendarEntry = function(event, revertFunc){
        var start= event.start.format().replace('T', ' ');
        var end = event.end.format().replace('T', ' ');

        var data = {
            event_id: event.id,
            start: start,
            end: end
        };

        $.post("{% url 'cal:ui_update' %}", data, function(result){
            console.log(result)
            if(result['success'] == 'true'){
                // TODO: Toast style notification to inform the user that their change was successful
                console.log('success');
            }
            else {
                revertFunc();
            }
        });
    };
});
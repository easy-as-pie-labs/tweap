{% load i18n %}
$(document).ready(function() {
		
		$('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,agendaWeek,agendaDay'
			},
			defaultDate: '2015-02-12',
			editable: false,
			eventLimit: true, // allow "more" link when too many events
			events: [
				{% for event in events %}
				{
					title: '{{ event.title }}',
					start: '{{ event.get_start_for_cal }}',
					end: '{{ event.get_end_for_cal }}',
					url: '{% url "cal:edit" event.id %}'
				},
				{% endfor %}
			]
		});
		
	});
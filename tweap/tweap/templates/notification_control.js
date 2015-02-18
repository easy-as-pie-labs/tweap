{% load i18n %}
$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});



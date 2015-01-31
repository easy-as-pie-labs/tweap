from django import template

register = template.Library()

@register.filter(name='addcssandtabindex')
def addcssandtabindex(value, arg):
    return value.as_widget(attrs={'class': arg, 'tabindex': '1'})

@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addtabindex')
def addtabindex(value, arg):
    return value.as_widget(attrs={'tabindex': arg})
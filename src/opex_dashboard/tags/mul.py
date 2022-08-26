from django import template

register = template.Library()

@register.filter
def mul(value, factor):
    return value * factor;


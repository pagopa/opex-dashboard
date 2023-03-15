from django.template import Library

register = Library()


@register.filter
def add_str(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

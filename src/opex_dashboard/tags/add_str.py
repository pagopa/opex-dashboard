from django.template import Library

register = Library()


@register.filter
def add_str(arg1: str, arg2: str) -> str:
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

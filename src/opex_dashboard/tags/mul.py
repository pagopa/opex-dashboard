from django import template

register = template.Library()

@register.filter
def mul(value: int, factor: int) -> int:
    """Multiply an integer with a factor

    Returns:
        int -> The prodict object
    """
    return value * factor;


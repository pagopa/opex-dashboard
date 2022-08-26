import re

from django.template import Library

register = Library()


@register.filter
def stringify(value: object) -> str:
    """Serialize an object in a string and wrap it inside double quote

    Returns:
        str -> The serialized object
    """
    escaped = re.sub("(?<!\\\\)\"", "\\\"", repr(value))
    return escaped.replace("'", "\"")

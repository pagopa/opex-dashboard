import re

from django.template import Library

register = Library()


@register.filter
def uri_to_regex(value: object) -> str:
    """Translate path parameters of a URI to a generic version thanks to regex

    Returns:
        str -> The serialized object
    """
    return re.sub("{[^/]+}", "[^/]+", str(value)) + "($|\\?)"

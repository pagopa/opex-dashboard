class ParseError(Exception):
    """
    Throw when a parsing error occurs
    """
    pass

class RenderError(Exception):
    """
    Throw when it is impossible to render a template
    """
    pass

class PlaceholderError(Exception):
    """
    Throw when a substitution has no placeholder to replace
    """
    pass

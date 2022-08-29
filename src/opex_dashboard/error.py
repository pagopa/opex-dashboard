class FileError(Exception):
    """Throw when a filesystem related error occurs
    """
    pass


class ParseError(Exception):
    """Throw when a parsing error occurs
    """
    pass


class InvalidBuilderError(Exception):
    """Throw when is impossible to instantiate a builder
    """
    pass

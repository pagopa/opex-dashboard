import re

from .error import PlaceholderError, RenderError

class Builder:
    _template: str

    def __init__(self, path: str) -> None:
        fin = open(path, "rt")
        self._template = fin.read()
        fin.close()

    def apply(self, placeholder: str, value: str) -> None:
        """Substitute a string like ${placeholder} with value

        Returns:
            None

        Raises:
            PlaceholderError: If given placeholder missed
        """
        if not self.hasplaceholder(placeholder):
            raise PlaceholderError(f"Missing placeholder error: {placeholder}")

        self._template = self._template.replace(f"${{{placeholder}}}", value)

    def hasplaceholder(self, placeholder: str) -> bool:
        """Check existance of specifice placeholder inside the template

        Returns:
            bool: Placeholder existance
        """
        return f"${{{placeholder}}}" in self._template

    def render(self) -> str:
        """Return current state of the template

        Returns:
            str: The template with eventually values applied

        Raises:
            RenderError: If any placeholder left
        """
        placeholders = [ph for ph in re.findall(r"\$\{\w*\}", self._template)]
        if (any(placeholders)):
            raise RenderError(f"Render error: unset {placeholders}")

        return self._template

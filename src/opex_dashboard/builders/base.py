import os

from typing import Dict, Any

from opex_dashboard.template import Template
from opex_dashboard.util import override_with


class Builder:
    _properties: Dict[str, Any]
    _template: Template

    def __init__(self, template: str, base_properties: Dict[str, Any] = {}) -> None:
        """Create a Builder object
        """
        self._properties = base_properties
        self._template = Template(template)

    def props(self) -> Dict[str, Any]:
        """Get all base properties
        """
        return self._properties

    def produce(self, values: Dict[str, Any] = {}) -> str:
        """Render the template by merging base properties and given values

        Returns:
            str: The rendered template
        """
        return self._template.render(override_with(self._properties, values))

    def package(self, path: str, values: Dict[str, Any] = {}) -> None:
        """Save the rendered template on filesystem
        """
        filepath = os.path.join(path, self._template.getname())
        with open(filepath, "w") as file:
            file.write(self.produce(values))

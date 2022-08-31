from typing import Dict, Any

from src.opex_dashboard.template import Template


class Builder:
    _properties: Dict[str, Any]
    _template: Template

    def __init__(self, template: str, base_properties: Dict[str, Any] = {}) -> None:
        """Create a Builder object
        """
        self._properties = base_properties
        self._template = Template(template)

    def produce(self, values: Dict[str, Any] = {}) -> str:
        """Render the template by merging base properties and given values

        Returns:
            str: The rendered template
        """
        return self._template.render(self._properties | values)

from typing import Dict, Any

from opex_dashboard.template import Template


class Builder:
    _properties: Dict[str, Any]
    _template: Template

    def __init__(self, template: str, base_properties: Dict[str, Any] = {}) -> None:
        self._properties = base_properties
        self._template = Template(template)

    def produce(self, values: Dict[str, Any] = {}) -> str:
        return self._template.render(self._properties | values)

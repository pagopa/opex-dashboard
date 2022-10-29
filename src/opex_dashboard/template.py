from django.template import Engine, Template as DTemplate, Context
from django.template.exceptions import TemplateDoesNotExist
from typing import Dict, Any

from opex_dashboard.error import FileError

TEMPLATES_DIRS = ["src/opex_dashboard/templates"]


class Template:
    engine = Engine(
        TEMPLATES_DIRS,
        autoescape=False,
        libraries={
            'mul': 'opex_dashboard.tags.mul',
            'stringify': 'opex_dashboard.tags.stringify',
            'uri_to_regex': 'opex_dashboard.tags.uri_to_regex',
        }
    )

    _template: DTemplate
    _name: str

    def __init__(self, template_file: str) -> None:
        """Create a Template object

        Raises:
            FileError: If template file missed
        """
        try:
            self._name = template_file
            self._template = self.engine.get_template(template_file)
        except TemplateDoesNotExist:
            raise FileError(f"Template file missing error: {template_file}")

    def render(self, tags: Dict[str, Any]) -> str:
        """Elaborate the template and return its representation

        Returns:
            str: The template with given tags applied
        """
        context = Context(tags, autoescape=False, use_l10n=False, use_tz=False)
        return self._template.render(context)

    def getname(self) -> str:
        """Return the name of the template file

        Returns:
            str: The template filename
        """
        return self._name

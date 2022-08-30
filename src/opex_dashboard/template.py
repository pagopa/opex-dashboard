from os.path import dirname, join
from django.template import Engine, Template as DTemplate, Context
from django.template.exceptions import TemplateDoesNotExist
from typing import Dict, Any

from .error import FileError

TEMPLATES_DIRS = [join(dirname(__file__), "templates")]


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

    def __init__(self, template_file: str) -> None:
        """Create a Template object

        Raises:
            FileError: If template file missed
        """
        try:
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

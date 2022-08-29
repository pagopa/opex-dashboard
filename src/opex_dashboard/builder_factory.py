from typing import Any, Optional

from opex_dashboard.error import InvalidBuilderError
from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_builder import AzDashboardBuilder


class BuilderFactory:
    @classmethod
    def create_builder(self, template: str, **args: Optional[Any]) -> Optional[Builder]:
        try:
            if template == "azure-dashboard":
                return AzDashboardBuilder(args["resolver"])
            elif template == "base":
                return Builder(args["template_name"], args.get("base_properties", {}))
            else:
                return None
        except KeyError as e:
            raise InvalidBuilderError(f"Invalid builder error: {e} is mandatory with {template}")

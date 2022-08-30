from typing import Any, Optional

from opex_dashboard.util import normalize_params
from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.error import InvalidBuilderError
from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_dashboard_builder import AzDashboardBuilder


class BuilderFactory:
    @classmethod  # TODO remove from the class
    def create_builder(self, template: str, **args: Optional[Any]) -> Optional[Builder]:
        try:
            if template == "azure-dashboard":
                inputs = normalize_params(args, {
                    "resolver": OA3Resolver,
                    "name": str,
                    "location": str,
                    "resources": list,
                    })
                return AzDashboardBuilder(inputs["resolver"], inputs["name"], inputs["location"], inputs["resources"])
            elif template == "base":
                inputs = normalize_params({"base_properties": {}} | args, {
                    "template_name": str,
                    "base_properties": dict,
                    })
                return Builder(inputs["template_name"], inputs["base_properties"])
            else:
                return None
                # raise InvalidBuilderError(f"Invalid builder error: unknown {template}")
        except KeyError as e:
            raise InvalidBuilderError(f"Invalid builder error: {e} is mandatory with {template}")
        except TypeError as e:
            raise InvalidBuilderError(f"Invalid builder error: {e}")

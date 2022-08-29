from typing import Any, Optional

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.error import InvalidBuilderError
from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_builder import AzDashboardBuilder


class BuilderFactory:
    @classmethod
    def create_builder(self, template: str, **args: Optional[Any]) -> Optional[Builder]:
        try:
            if template == "azure-dashboard":
                if not isinstance(args["resolver"], OA3Resolver):
                    raise TypeError("'resolver' must be an OA3Resolver")
                return AzDashboardBuilder(args["resolver"])
            elif template == "base":
                base_properties = args.get("base_properties", {})
                if not isinstance(args["template_name"], str):
                    raise TypeError("'template_name' must be a string")
                if not isinstance(base_properties, dict):
                    raise TypeError("'base_properties' must be a dict")
                return Builder(args["template_name"], base_properties)
            else:
                return None
                # raise InvalidBuilderError(f"Invalid builder error: unknown {template}")
        except KeyError as e:
            raise InvalidBuilderError(f"Invalid builder error: {e} is mandatory with {template}")
        except TypeError as e:
            raise InvalidBuilderError(f"Invalid builder error: {e}")

from typing import Any, Optional

from opex_dashboard.util import normalize_params
from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.error import InvalidBuilderError
from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_dashboard_builder import AzDashboardBuilder


def create_builder(template: str, **args: Optional[Any]) -> Optional[Builder]:
    """Factory method for Builder

    Returns:
        Optional[Builder]: The Builder if template exists, None otherwise
    """
    try:
        if template == "azure-dashboard":
            inputs = normalize_params(args, {
                "resolver": OA3Resolver,
                "name": str,
                "location": str,
                "timespan": str,
                "resources": list,
                })
            return AzDashboardBuilder(
                    inputs["resolver"],
                    inputs["name"],
                    inputs["location"],
                    inputs["timespan"],
                    inputs["resources"])
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

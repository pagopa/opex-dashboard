from typing import Any, Optional

from opex_dashboard.util import normalize_params
from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.error import InvalidBuilderError
from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_dashboard_raw_builder import AzDashboardRawBuilder
from opex_dashboard.builders.azure_dashboard_builder import AzDashboardBuilder


def create_azure_terraform_builder(**args: Optional[Any]) -> Optional[Builder]:
    inputs = normalize_params(args, {
        "name": str,
        "location": str,
        "timespan": str,
        "data_source_id": str,
        "action_groups_ids": list,
        })
    inputs["dashboard_builder"] = create_azure_raw_builder(**args)
    return AzDashboardBuilder(**inputs)


def create_azure_raw_builder(**args: Optional[Any]) -> Optional[Builder]:
    inputs = normalize_params(args, {
        "resolver": OA3Resolver,
        "name": str,
        "location": str,
        "timespan": str,
        "resources": list,
        })
    return AzDashboardRawBuilder(**inputs)


def create_base_builder(**args: Optional[Any]) -> Optional[Builder]:
    inputs = normalize_params({"base_properties": {}} | args, {
        "template": str,
        "base_properties": dict,
        })
    return Builder(**inputs)


def create_builder(template_type: str, **args: Optional[Any]) -> Optional[Builder]:
    """Factory method for Builder

    Returns:
        Optional[Builder]: The Builder if template exists, None otherwise
    """
    try:
        builders = {
            "azure-dashboard": create_azure_terraform_builder,
            "azure-dashboard-raw": create_azure_raw_builder,
            "base": create_base_builder
        }
        return builders.get(template_type, lambda **_: None)(**args)
        # raise InvalidBuilderError(f"Invalid builder error: unknown {template}")
    except KeyError as e:
        raise InvalidBuilderError(f"Invalid builder error: {e} is mandatory with {template_type}")
    except TypeError as e:
        raise InvalidBuilderError(f"Invalid builder error: {e}")

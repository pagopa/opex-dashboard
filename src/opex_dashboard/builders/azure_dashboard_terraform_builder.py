import json

from typing import Dict, Any

from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_dashboard_builder import AzDashboardBuilder


class AzDashboardTerraformBuilder(Builder):
    _builder: AzDashboardBuilder

    def __init__(self,
                 dashboard_builder: AzDashboardBuilder,
                 name: str,
                 location: str) -> None:
        """Create an AzDashbordTerraformBuilder object
        """
        self._builder = dashboard_builder
        super().__init__(
            template="azure_dashboard_terraform.tf",
            base_properties={
                "name": name,
                "location": location,
            }
        )

    def produce(self, values: Dict[str, Any] = {}) -> str:
        """Render the template by merging base properties with given and extracted values from AzDashboardBuilder

        Returns:
            str: The rendered template to create an Azure Dashboard with Terraform
        """
        dashboard = json.loads(self._builder.produce(values))
        return super().produce({
            "dashboard_properties": json.dumps(dashboard["properties"], indent=2),
            "hosts": self._builder.props()["hosts"],
            "endpoints": self._builder.props()["endpoints"],
            "timespan": self._builder.props()["timespan"],
        })

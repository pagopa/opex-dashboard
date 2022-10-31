import os
import shutil
import json

from typing import Dict, Any

from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_dashboard_raw_builder import AzDashboardRawBuilder


class AzDashboardBuilder(Builder):
    _builder: AzDashboardRawBuilder

    def __init__(self,
                 dashboard_builder: AzDashboardRawBuilder,
                 name: str,
                 location: str,
                 timespan: str,
                 data_source_id: str) -> None:
        """Create an AzDashbordTerraformBuilder object
        """
        self._builder = dashboard_builder
        super().__init__(
            template="azure_dashboard_terraform.tf",
            base_properties={
                "name": name,
                "location": location,
                "timespan": timespan,
                "data_source_id": data_source_id,
            }
        )

    def produce(self, values: Dict[str, Any] = {}) -> str:
        """Render the template by merging base properties with given and extracted values from AzDashboardRawBuilder

        Returns:
            str: The rendered template to create an Azure Dashboard with Terraform
        """
        dashboard = json.loads(self._builder.produce(values))
        self._properties["dashboard_properties"] = json.dumps(dashboard["properties"], indent=2)
        self._properties["hosts"] = self._builder.props()["hosts"]
        self._properties["endpoints"] = self._builder.props()["endpoints"]
        return super().produce(values)

    def package(self, path: str, values: Dict[str, Any] = {}) -> None:
        """Save the rendered template on filesystem with PagoPA Terraform project conventions
        """
        filepath = os.path.join(path, "01_opex.tf")
        with open(filepath, "w") as file:
            file.write(self.produce(values))

        assets_path = os.path.join(os.path.dirname(__file__), "../assets/terraform")
        for obj in os.listdir(assets_path):
            obj_path = os.path.join(assets_path, obj)
            if os.path.isdir(obj_path):
                shutil.copytree(obj_path, os.path.join(path, obj))
            else:
                shutil.copy(obj_path, os.path.join(path, obj))

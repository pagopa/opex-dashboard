import os
import shutil
import json

from typing import Dict, Any, List

from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_dashboard_raw_builder import AzDashboardRawBuilder


class AzDashboardBuilder(Builder):
    _builder: AzDashboardRawBuilder

    def __init__(self,
                 dashboard_builder: AzDashboardRawBuilder,
                 name: str,
                 resource_type: str,
                 location: str,
                 timespan: str,
                 evaluation_frequency: int,
                 evaluation_time_window: int,
                 event_occurrences: int,
                 data_source_id: str,
                 action_groups_ids: List[str]) -> None:
        """Create an AzDashbordTerraformBuilder object
        """
        self._builder = dashboard_builder
        super().__init__(
            template="azure_dashboard_terraform.tf",
            base_properties={
                "name": name.replace(" ", "_"),
                "resource_type": resource_type,
                "location": location,
                "timespan": timespan,
                "evaluation_frequency": evaluation_frequency,
                "evaluation_time_window": evaluation_time_window,
                "event_occurrences": event_occurrences,
                "data_source_id": data_source_id,
                "action_groups_ids": action_groups_ids,
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

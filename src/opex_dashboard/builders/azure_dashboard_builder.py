from typing import Dict, List, Any

from opex_dashboard.builders.base import Builder
from opex_dashboard.resolver import OA3Resolver


class AzDashboardBuilder(Builder):
    _oa3_spec: Dict[str, Any]

    def __init__(self, resolver: OA3Resolver, name: str, location: str, resources: List[str]) -> None:
        """Create an AzDashbordBuilder object
        """
        self._oa3_spec = resolver.resolve()  # TODO base_properties from resolver?
        super().__init__(
            template="azure_dashboard.json",
            base_properties={
                "name": name,
                "location": location,
                "resource_ids": resources,
            }
        )

    def produce(self, values: Dict[str, Any] = {}) -> str:
        """Render the template by merging base properties, given values, and information extracted form OA3 spec

        Returns:
            str: The rendered template to create an Azure Dashboard json
        """
        if "servers" in self._oa3_spec:
            hosts = [h["url"] for h in self._oa3_spec["servers"]]
        else:
            hosts = [self._oa3_spec["host"]]
        self._properties["hosts"] = hosts

        base_path = self._oa3_spec["basePath"]
        self._properties["endpoints"] = [f"{base_path}/{endpoint[1:]}" for endpoint in self._oa3_spec["paths"].keys()]

        return super().produce(values)

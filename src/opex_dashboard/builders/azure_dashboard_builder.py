from typing import Dict, Any

from opex_dashboard.builders.base import Builder
from opex_dashboard.resolver import OA3Resolver


class AzDashboardBuilder(Builder):
    _oa3_spec: Dict[str, Any]

    def __init__(self, resolver: OA3Resolver, name, location, resources) -> None:
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
        if "servers" in self._oa3_spec:
            hosts = [h["url"] for h in self._oa3_spec["servers"]]
        else:
            hosts = [self._oa3_spec["host"]]
        self._properties["hosts"] = hosts

        base_path = self._oa3_spec["basePath"]
        self._properties["endpoints"] = [f"{base_path}/{endpoint[1:]}" for endpoint in self._oa3_spec["paths"].keys()]

        return super().produce(values)

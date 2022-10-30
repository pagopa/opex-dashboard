from typing import Dict, List, Any
from urllib.parse import urlparse

from opex_dashboard.builders.base import Builder
from opex_dashboard.resolver import OA3Resolver


class AzDashboardRawBuilder(Builder):
    _oa3_spec: Dict[str, Any]

    def __init__(self,
                 resolver: OA3Resolver,
                 name: str,
                 location: str,
                 timespan: str,
                 resources: List[str]) -> None:
        """Create an AzDashbordBuilder object
        """
        self._oa3_spec = resolver.resolve()
        super().__init__(
            template="azure_dashboard.json",
            base_properties={
                "name": name,
                "location": location,
                "timespan": timespan,
                "resource_ids": resources,
            }
        )

    def produce(self, values: Dict[str, Any] = {}) -> str:
        """Render the template by merging base properties with given and extracted values from OA3 spec

        Returns:
            str: The rendered template to create an Azure Dashboard json
        """
        if "servers" in self._oa3_spec:
            self._properties["hosts"] = []
            self._properties["endpoints"] = []
            for server in self._oa3_spec["servers"]:
                url = urlparse(server["url"])
                self._properties["hosts"].append(url.netloc)
                for p in list(self._oa3_spec["paths"].keys()):
                    self._properties["endpoints"].append(f"{url.path}/{p[1:]}")
            self._properties["endpoints"] = [*set(self._properties["endpoints"])]
        else:
            base_path = self._oa3_spec["basePath"]
            self._properties["hosts"] = [self._oa3_spec["host"]]
            self._properties["endpoints"] = [f"{base_path}/{p[1:]}" for p in self._oa3_spec["paths"].keys()]

        return super().produce(values)

from re import sub
from typing import Dict, List, Any
from urllib.parse import urlparse

from opex_dashboard.builders.base import Builder
from opex_dashboard.resolver import OA3Resolver


class AzDashboardRawBuilder(Builder):
    _oa3_spec: Dict[str, Any]

    def __init__(self,
                 resolver: OA3Resolver,
                 name: str,
                 resource_type: str,
                 location: str,
                 timespan: str,
                 evaluation_frequency: int,
                 evaluation_time_window: int,
                 event_occurrences: int,
                 resources: List[str]) -> None:
        """Create an AzDashbordBuilder object
        """
        self._oa3_spec = resolver.resolve()
        super().__init__(
            template="azure_dashboard_raw.json",
            base_properties={
                "name": name,
                "resource_type": resource_type,
                "location": location,
                "timespan": timespan,
                "evaluation_frequency": evaluation_frequency,
                "evaluation_time_window": evaluation_time_window,
                "event_occurrences": event_occurrences,
                "resource_ids": resources,
            }
        )

    def __collect(self, hosts: List[str], paths: Dict[str, Any]) -> None:
        """Build base properties from given parameters
        """
        endpoint_default_values = {
            "availability_threshold": 0.99,
            "availability_evaluation_frequency":  self.props()["evaluation_frequency"],
            "availability_evaluation_time_window":  self.props()["evaluation_time_window"],
            "availability_event_occurrences": self.props()["event_occurrences"],
            "response_time_threshold": 1,
            "response_time_evaluation_frequency": self.props()["evaluation_frequency"],
            "response_time_evaluation_time_window": self.props()["evaluation_time_window"],
            "response_time_event_occurrences": self.props()["event_occurrences"],
        }

        self._properties["hosts"] = []
        self._properties["endpoints"] = {}
        for host in hosts:
            if host.startswith("http"):
                url = urlparse(host)
            else:
                url = urlparse(f"//{host}")

            self._properties["hosts"].append(url.netloc)
            for p in list(paths.keys()):
                path = sub("/+", "/", f"{url.path}/{p[1:]}")
                self._properties["endpoints"][path] = endpoint_default_values

    def produce(self, values: Dict[str, Any] = {}) -> str:
        """Render the template by merging base properties with given and extracted values from OA3 spec

        Returns:
            str: The rendered template to create an Azure Dashboard json
        """
        if "servers" in self._oa3_spec:
            hosts = [s["url"] for s in self._oa3_spec["servers"]]
        else:
            hosts = [f"{self._oa3_spec['host']}{self._oa3_spec['basePath']}"]
        self.__collect(hosts, self._oa3_spec["paths"])

        return super().produce(values)

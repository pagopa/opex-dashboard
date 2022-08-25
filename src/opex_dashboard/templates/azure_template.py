import json

from ..builder import Builder

TEMPLATE_BASE_PATH = "./src/opex_dashboard/templates/azure_template"

# TODO this should be an initial setting
GRAPH_COLSPAN = 6
GRAPH_ROWSPAN = 4
GRAPH_SCOPES = ["azure/resource/id"]
GRAPH_TIME_RANGE = "PT4H"
GRAPH_TITLE = "APIs Profile Availability (5min)"
GRAPH_SUBTITLE = "io-d-appgateway"
GRAPH_X_LABEL = "TimeGenerated"
GRAPH_Y_LABEL = "Availability"
GRAPH_SPLIT_BY = []
GRAPH_AGGREGATION = "Sum"

class AZTemplate:
    _template: Builder

    def __init__(self, name: str, location: str) -> None:
        self._template = Builder(f"{TEMPLATE_BASE_PATH}/template.json")
        self._template.apply("name", name)
        self._template.apply("location", location)

    def availability(self, hosts: list, endpoint: str, raw: bool = True) -> str:
        normalized_hosts = [f"\"{host}\"" for host in hosts]

        builder = Builder(f"{TEMPLATE_BASE_PATH}/availability-query.kusto")
        builder.apply("hosts", ", ".join(normalized_hosts))
        builder.apply("endpoint", endpoint)

        query = builder.render()
        if raw:
            query = repr(query).replace("\"","\\\"").replace("'", "")

        return query

    def response_codes(self, hosts: list, endpoint: str, raw: bool = True) -> str:
        normalized_hosts = [f"\"{host}\"" for host in hosts]

        builder = Builder(f"{TEMPLATE_BASE_PATH}/response-codes-query.kusto")
        builder.apply("hosts", ", ".join(normalized_hosts))
        builder.apply("endpoint", endpoint)

        query = builder.render()
        if raw:
            query = repr(query).replace("\"","\\\"").replace("'", "")

        return query

    def response_time(self, hosts: list, endpoint: str, raw: bool = True) -> str:
        where_clause = [f"originalHost_s == \"{host}\"" for host in hosts]

        builder = Builder(f"{TEMPLATE_BASE_PATH}/response-time-query.kusto")
        builder.apply("hosts", " or ".join(where_clause))
        builder.apply("endpoint", endpoint)

        query = builder.render()
        if raw:
            query = repr(query).replace("\"","\\\"").replace("'", "")

        return query

    def render_part(self, properties: dict) -> str:
        builder = Builder(f"{TEMPLATE_BASE_PATH}/template-part.json")

        for key in properties:
            value = properties[key]
            if isinstance(value, list):
                value = ", ".join([f"\"{v}\"" for v in value])
            builder.apply(key, value)

        return builder.render()

    def render(self, hosts: list, endpoints: list) -> str:
        parts = {}
        for y, endpoint in enumerate(endpoints):
            queries = [
                self.availability(hosts, endpoint),
                self.response_codes(hosts, endpoint),
                self.response_time(hosts, endpoint)
            ]

            properties = {
                "y": str(y * GRAPH_ROWSPAN),
                "colspan": str(GRAPH_COLSPAN),
                "rowspan": str(GRAPH_ROWSPAN),
                "scopes": GRAPH_SCOPES,
                "range": GRAPH_TIME_RANGE,
                "subtitle": GRAPH_SUBTITLE,
                "title": GRAPH_TITLE,
                "x_label": GRAPH_X_LABEL,
                "y_label": GRAPH_Y_LABEL,
                "split_by": GRAPH_SPLIT_BY,
                "aggregation": GRAPH_AGGREGATION,
            }

            for x, query in enumerate(queries):
                properties["x"] = str(x * GRAPH_COLSPAN)
                properties["query"] = query
                parts[y] = self.render_part(properties)

        self._template.apply("parts", json.dumps(parts))

        return self._template.render()


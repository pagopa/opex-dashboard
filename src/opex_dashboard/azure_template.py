import json

from .template import Template

TEMPLATE_BASE_PATH = "./src/opex_dashboard/templates"

class AZTemplate:
    _template: Template

    def __init__(self, name: str, location: str) -> None:
        self._template = Template(f"{TEMPLATE_BASE_PATH}/template.json")
        self._template.apply("name", name)
        self._template.apply("location", location)

    def availability(self, hosts: list, endpoint: str, raw: bool = True) -> str:
        normalized_hosts = [f"\"{host}\"" for host in hosts]

        template = Template(f"{TEMPLATE_BASE_PATH}/availability-query.kusto")
        template.apply("hosts", ", ".join(normalized_hosts))
        template.apply("endpoint", endpoint)

        query = template.render()
        if raw:
            query = repr(query).replace("\"","\\\"").replace("'", "")

        return query

    def response_codes(self, hosts: list, endpoint: str, raw: bool = True) -> str:
        normalized_hosts = [f"\"{host}\"" for host in hosts]

        template = Template(f"{TEMPLATE_BASE_PATH}/response-codes-query.kusto")
        template.apply("hosts", ", ".join(normalized_hosts))
        template.apply("endpoint", endpoint)

        query = template.render()
        if raw:
            query = repr(query).replace("\"","\\\"").replace("'", "")

        return query

    def response_time(self, hosts: list, endpoint: str, raw: bool = True) -> str:
        where_clause = [f"originalHost_s == \"{host}\"" for host in hosts]

        template = Template(f"{TEMPLATE_BASE_PATH}/response-time-query.kusto")
        template.apply("hosts", " or ".join(where_clause))
        template.apply("endpoint", endpoint)

        query = template.render()
        if raw:
            query = repr(query).replace("\"","\\\"").replace("'", "")

        return query

    def render_part(self, properties: dict) -> str:
        template = Template(f"{TEMPLATE_BASE_PATH}/template-part.json")

        for key in properties:
            value = properties[key]
            if isinstance(value, list):
                value = ", ".join([f"\"{v}\"" for v in value])
            template.apply(key, value)

        return template.render()

    def render(self, hosts: list, endpoints: list) -> str:
        parts = {}
        for i, endpoint in enumerate(endpoints):
            parts[i] = self.render_part({
                "x": "0",
                "y": str(i * 4),
                "colspan": "6",
                "rowspan": "4",
                "scopes": [],
                "range": "PT4H",
                "subtitle": endpoint,
                "title": "APIs Profile Availability (5min)",
                "x_label": "TimeGenerated",
                "y_label": "Availability",
                "split_by": [],
                "aggregation": "Sum",
                "query": self.availability(hosts, endpoint),
            })

            parts[i] = self.render_part({
                "x": "6",
                "y": str(i * 4),
                "colspan": "6",
                "rowspan": "4",
                "scopes": [],
                "range": "PT4H",
                "subtitle": endpoint,
                "title": "APIs Message Response Codes (5min)",
                "x_label": "HttpStatus",
                "y_label": "Count",
                "split_by": [],
                "aggregation": "Sum",
                "query": self.response_codes(hosts, endpoint),
            })

            parts[i] = self.render_part({
                "x": "12",
                "y": str(i * 4),
                "colspan": "6",
                "rowspan": "4",
                "scopes": [],
                "range": "PT4H",
                "subtitle": endpoint,
                "title": "APIs Message Response Codes (5min)",
                "x_label": "HttpStatus",
                "y_label": "Count",
                "split_by": [],
                "aggregation": "Sum",
                "query": self.response_time(hosts, endpoint),
            })

        self._template.apply("parts", json.dumps(parts))

        return self._template.render()


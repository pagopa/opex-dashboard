import json

from os.path import dirname, join

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.template import Template
from opex_dashboard.builder_factory import BuilderFactory

DATA_BASE_PATH = join(dirname(__file__), "data")
NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT = 3
RESOURCE_ID = ("/subscriptions/uuid/"
               "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
               "/applicationGateways/io-p-appgateway")
ROW_SPAN = 4
COL_SPAN = 6


def test_produce_the_template():
    """
    GIVEN an Azure Dashboard builder
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
    builder = BuilderFactory.create_builder("azure-dashboard", resolver=resolver)

    spec_dict = resolver.resolve()
    template_dict = json.loads(builder.produce())

    assert template_dict["name"] == "PROD-IO/IO App Availability"
    assert template_dict["location"] == "West Europe"

    parts = template_dict["properties"]["lenses"]["0"]["parts"]
    paths = [spec_dict["basePath"] + path for path in list(spec_dict["paths"].keys())]

    assert len(parts) == len(spec_dict["paths"]) * NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT

    for i, part_index in enumerate(parts):
        assert i == int(part_index)

        part = parts[part_index]
        path = paths[i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]

        assert part["position"]["x"] == i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * COL_SPAN
        assert part["position"]["y"] == i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * ROW_SPAN

        resouce_id = next(e for e in part["metadata"]["inputs"] if e["name"] == "Scope")
        subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
        query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")

        assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
        assert subtitle["value"] == path

        queries = [
            Template("queries/availability.kusto").render({"endpoint": path, "hosts": [spec_dict["host"]]}),
            Template("queries/response_codes.kusto").render({"endpoint": path, "hosts": [spec_dict["host"]]}),
            Template("queries/response_time.kusto").render({"endpoint": path, "hosts": [spec_dict["host"]]}),
        ]

        assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
        assert part["metadata"]["settings"]["content"]["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]

import json

from os.path import dirname, join
from urllib.parse import urlparse

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.template import Template
from opex_dashboard.builder_factory import create_builder

DATA_BASE_PATH = join(dirname(__file__), "data")
NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT = 3
NAME = "PROD-IO/IO App Availability"
LOCATION = "West Europe"
RESOURCE_ID = ("/subscriptions/uuid/"
               "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
               "/applicationGateways/io-p-appgateway")
ROW_SPAN = 4
COL_SPAN = 6


def test_produce_the_template_with_host_and_base_path_options():
    """
    GIVEN a name, a location, a list of resrouces and a OA3 spec with host and basePath
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
    builder = create_builder(
            "azure-dashboard",
            resolver=resolver,
            name=NAME,
            location=LOCATION,
            resources=[RESOURCE_ID]
            )

    spec_dict = resolver.resolve()
    template_dict = json.loads(builder.produce())

    assert template_dict["name"] == NAME
    assert template_dict["location"] == LOCATION

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


def test_produce_the_template_with_servers_option():
    """
    GIVEN a name, a location, a list of resrouces and a OA3 spec with servers
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/selfcare_partyprocess.yaml")
    builder = create_builder(
            "azure-dashboard",
            resolver=resolver,
            name=NAME,
            location=LOCATION,
            resources=[RESOURCE_ID]
            )

    spec_dict = resolver.resolve()
    template_dict = json.loads(builder.produce())

    assert template_dict["name"] == NAME
    assert template_dict["location"] == LOCATION

    parts = template_dict["properties"]["lenses"]["0"]["parts"]
    urls = [urlparse(server["url"]) for server in spec_dict["servers"]]
    hosts = [url.netloc for url in urls]
    paths = []
    for url in urls:
        for path in list(spec_dict["paths"].keys()):
            paths.append(f"{url.path}/{path[1:]}")

    assert len(parts) == len(paths) * NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT

    for i, part_index in enumerate(parts):
        assert i == int(part_index)

        part = parts[part_index]
        resouce_id = next(e for e in part["metadata"]["inputs"] if e["name"] == "Scope")
        subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
        query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")

        assert part["position"]["x"] == i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * COL_SPAN
        assert part["position"]["y"] == i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * ROW_SPAN

        assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
        assert subtitle["value"] in paths

        queries = [
            Template("queries/availability.kusto").render({"endpoint": subtitle["value"], "hosts": hosts}),
            Template("queries/response_codes.kusto").render({"endpoint": subtitle["value"], "hosts": hosts}),
            Template("queries/response_time.kusto").render({"endpoint": subtitle["value"], "hosts": hosts}),
        ]

        assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
        assert part["metadata"]["settings"]["content"]["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]

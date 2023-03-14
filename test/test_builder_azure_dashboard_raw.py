import json

from os.path import dirname, join
from urllib.parse import urlparse

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.template import Template
from opex_dashboard.builder_factory import create_builder

DATA_BASE_PATH = join(dirname(__file__), "data")
NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT = 3
NAME = "PROD-IO/IO App Availability"
SERVICE = "pagopa-io-backend"
IS_INTERNAL = False
LOCATION = "West Europe"
RESOURCE_ID = ("/subscriptions/uuid/"
               "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
               "/applicationGateways/io-p-appgateway")
TIMESPAN = "5m"
ROW_SPAN = 4
COL_SPAN = 6


def test_produce_the_template_with_host_and_base_path_options():
    """
    GIVEN a name, a location, a timespan, a list of resources and a OA3 spec with host and basePath
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
    builder = create_builder(
            "azure-dashboard-raw",
            resolver=resolver,
            name=NAME,
            service=SERVICE,
            is_internal=IS_INTERNAL,
            location=LOCATION,
            timespan=TIMESPAN,
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
        title = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartTitle")
        subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
        query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")

        assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
        assert title["value"].endswith(f"({TIMESPAN})")
        assert subtitle["value"] == path

        query_params = {
            "endpoint": path,
            "hosts": [spec_dict["host"]],
            "timespan": TIMESPAN,
        }

        queries = [
            Template("gateway_queries/availability.kusto").render(query_params),
            Template("gateway_queries/response_codes.kusto").render(query_params),
            Template("gateway_queries/response_time.kusto").render(query_params),
        ]

        assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]

        content = part["metadata"]["settings"]["content"]
        assert content["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
        assert content["PartTitle"].endswith(f"({TIMESPAN})")


def test_the_template_with_host_and_base_path_options_and_hosts_overrides():
    """
    GIVEN a name, a location, a timespan, a list of resources and a OA3 spec with host and basePath
    WHEN the builder produces the template overriding hosts
    THEN the template is rendered with correct hosts
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
    builder = create_builder(
            "azure-dashboard-raw",
            resolver=resolver,
            name=NAME,
            service=SERVICE,
            is_internal=IS_INTERNAL,
            location=LOCATION,
            timespan=TIMESPAN,
            resources=[RESOURCE_ID]
            )

    custom_hosts = ["foo.pagopa.it", "bar.pagopa.it"]
    spec_dict = resolver.resolve()
    template_dict = json.loads(builder.produce({"hosts": custom_hosts}))

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
        title = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartTitle")
        subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
        query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")

        assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
        assert title["value"].endswith(f"({TIMESPAN})")
        assert subtitle["value"] == path

        query_params = {
            "endpoint": path,
            "hosts": custom_hosts,
            "timespan": TIMESPAN,
        }

        queries = [
            Template("gateway_queries/availability.kusto").render(query_params),
            Template("gateway_queries/response_codes.kusto").render(query_params),
            Template("gateway_queries/response_time.kusto").render(query_params),
        ]

        assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]

        content = part["metadata"]["settings"]["content"]
        assert content["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
        assert content["PartTitle"].endswith(f"({TIMESPAN})")


def test_produce_the_template_with_servers_option():
    """
    GIVEN a name, a location, a timespan, a list of resources and a OA3 spec with host and basePath
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/selfcare_party_process.yaml")
    builder = create_builder(
            "azure-dashboard-raw",
            resolver=resolver,
            name=NAME,
            service=SERVICE,
            is_internal=IS_INTERNAL,
            location=LOCATION,
            timespan=TIMESPAN,
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
        title = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartTitle")
        subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
        query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")

        assert part["position"]["x"] == i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * COL_SPAN
        assert part["position"]["y"] == i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * ROW_SPAN

        assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
        assert title["value"].endswith(f"({TIMESPAN})")
        assert subtitle["value"] in paths

        query_params = {
            "endpoint": subtitle["value"],
            "hosts": hosts,
            "timespan": TIMESPAN,
        }

        queries = [
            Template("gateway_queries/availability.kusto").render(query_params),
            Template("gateway_queries/response_codes.kusto").render(query_params),
            Template("gateway_queries/response_time.kusto").render(query_params),
        ]

        assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]

        content = part["metadata"]["settings"]["content"]
        assert content["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
        assert content["PartTitle"].endswith(f"({TIMESPAN})")


def test_the_template_with_servers_option_and_hosts_overrides():
    """
    GIVEN a name, a location, a timespan, a list of resources and a OA3 spec with host and basePath
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/selfcare_party_process.yaml")
    builder = create_builder(
            "azure-dashboard-raw",
            resolver=resolver,
            name=NAME,
            service=SERVICE,
            is_internal=IS_INTERNAL,
            location=LOCATION,
            timespan=TIMESPAN,
            resources=[RESOURCE_ID]
            )

    custom_hosts = ["foo.pagopa.it", "bar.pagopa.it"]
    spec_dict = resolver.resolve()
    template_dict = json.loads(builder.produce({"hosts": custom_hosts}))

    assert template_dict["name"] == NAME
    assert template_dict["location"] == LOCATION

    parts = template_dict["properties"]["lenses"]["0"]["parts"]
    urls = [urlparse(server["url"]) for server in spec_dict["servers"]]
    paths = []
    for url in urls:
        for path in list(spec_dict["paths"].keys()):
            paths.append(f"{url.path}/{path[1:]}")

    assert len(parts) == len(paths) * NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT

    for i, part_index in enumerate(parts):
        assert i == int(part_index)

        part = parts[part_index]
        resouce_id = next(e for e in part["metadata"]["inputs"] if e["name"] == "Scope")
        title = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartTitle")
        subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
        query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")

        assert part["position"]["x"] == i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * COL_SPAN
        assert part["position"]["y"] == i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * ROW_SPAN

        assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
        assert title["value"].endswith(f"({TIMESPAN})")
        assert subtitle["value"] in paths

        query_params = {
            "endpoint": subtitle["value"],
            "hosts": custom_hosts,
            "timespan": TIMESPAN,
        }

        queries = [
            Template("gateway_queries/availability.kusto").render(query_params),
            Template("gateway_queries/response_codes.kusto").render(query_params),
            Template("gateway_queries/response_time.kusto").render(query_params),
        ]

        assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]

        content = part["metadata"]["settings"]["content"]
        assert content["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
        assert content["PartTitle"].endswith(f"({TIMESPAN})")

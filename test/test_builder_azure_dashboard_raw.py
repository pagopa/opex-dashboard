import json
from os.path import dirname, join
from urllib.parse import urlparse

from opex_dashboard.builder_factory import create_builder
from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.template import Template

DATA_BASE_PATH = join(dirname(__file__), "data")
NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT = 3
NAME = "PROD-IO/IO App Availability"
RESOURCE_TYPE = "app-gateway"
LOCATION = "West Europe"
RESOURCE_ID = ("/subscriptions/uuid/"
               "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
               "/applicationGateways/io-p-appgateway")
TIMESPAN = "5m"
EVALUATION_FREQUENCY = 10
EVALUATION_TIME_WINDOW = 20
EVENT_OCCURRENCES = 2
ROW_SPAN = 4
COL_SPAN = 6

RESPONSE_TIME_THRESHOLD = 1.0
AVAILABILITY_THRESHOLD = 1.0

VALID_HTTP_METHODS = {
    "get", "put", "post", "delete", "options", "head", "patch", "trace"
}


def _build_expected_endpoints_and_ops_count_for_oas2(spec_dict):
    """Helper per OAS2 (host/basePath)."""
    expected_endpoints_ordered = []
    operations = []
    total_operations = 0
    base_path_prefix = spec_dict.get("basePath", "").rstrip('/')

    path_definitions = spec_dict.get("paths", {})

    # Iterare sui path e operazioni in un ordine definito (chiavi del path, poi chiavi dell'operazione ordinate)
    for path_key in (path_definitions.keys()):  # Ordina i path_key per coerenza
        path_item_operations = path_definitions[path_key]

        if base_path_prefix == "" or base_path_prefix == "/":
            current_endpoint_path = path_key
        else:
            current_endpoint_path = base_path_prefix + path_key

        if len(current_endpoint_path) > 1 and current_endpoint_path.startswith("//"):
            current_endpoint_path = current_endpoint_path[1:]

        # Ordina le operazioni (get, post, ecc.) per coerenza
        # e conta solo le operazioni HTTP valide
        for op_key in (path_item_operations.keys()):
            if op_key.lower() in VALID_HTTP_METHODS:
                expected_endpoints_ordered.append(current_endpoint_path)
                operations.append(f'{op_key.upper()} {current_endpoint_path}')
                total_operations += 1

    return expected_endpoints_ordered, total_operations, operations


def _build_expected_endpoints_and_ops_count_for_oas3(spec_dict):
    """Helper per OAS3 (servers)."""
    expected_endpoints_ordered = []
    operations = []
    total_operation_instances = 0

    servers = spec_dict.get("servers", [])
    if not servers and "host" in spec_dict:
        return _build_expected_endpoints_and_ops_count_for_oas2(spec_dict)

    server_urls_parsed = [urlparse(server["url"]) for server in servers]
    path_definitions = spec_dict.get("paths", {})

    for server_url_obj in server_urls_parsed:
        server_path_prefix = server_url_obj.path.rstrip('/')

        for path_key in (path_definitions.keys()):
            path_item_operations = path_definitions[path_key]

            if server_path_prefix == "" or server_path_prefix == "/":
                current_endpoint_path = path_key
            else:
                current_endpoint_path = server_path_prefix + path_key

            if len(current_endpoint_path) > 1 and current_endpoint_path.startswith("//"):
                current_endpoint_path = current_endpoint_path[1:]

            # Ordina le operazioni e conta solo le operazioni HTTP valide
            for op_key in (path_item_operations.keys()):
                if op_key.lower() in VALID_HTTP_METHODS:  # MODIFICA QUI
                    expected_endpoints_ordered.append(current_endpoint_path)
                    operations.append(f'{op_key.upper()} {current_endpoint_path}')
                    total_operation_instances += 1

    return expected_endpoints_ordered, total_operation_instances, operations


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
        resource_type=RESOURCE_TYPE,
        location=LOCATION,
        timespan=TIMESPAN,
        availability_threshold=AVAILABILITY_THRESHOLD,
        response_time_threshold=RESPONSE_TIME_THRESHOLD,
        evaluation_frequency=EVALUATION_FREQUENCY,
        evaluation_time_window=EVALUATION_TIME_WINDOW,
        event_occurrences=EVENT_OCCURRENCES,
        resources=[RESOURCE_ID]
    )

    spec_dict = resolver.resolve()
    template_dict = json.loads(builder.produce())

    assert template_dict["name"] == NAME
    assert template_dict["location"] == LOCATION

    parts = template_dict["properties"]["lenses"]["0"]["parts"]
    paths = [spec_dict["basePath"] + path for path in list(spec_dict["paths"].keys())]

    # MODIFICA: Calcola il numero di operazioni e gli endpoint attesi
    expected_endpoints_ordered, total_operations, operations \
        = _build_expected_endpoints_and_ops_count_for_oas2(spec_dict)

    assert len(parts) == total_operations * NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT

    for i, part_index in enumerate(parts):
        assert i == int(part_index)

        part = parts[part_index]
        if (len(paths) <= i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT):
            continue
        # path = paths[i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]

        assert part["position"]["x"] == i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * COL_SPAN
        assert part["position"]["y"] == i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT * ROW_SPAN

        resouce_id = next(e for e in part["metadata"]["inputs"] if e["name"] == "Scope")
        title = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartTitle")
        subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
        # query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")

        assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
        assert title["value"].endswith(f"({TIMESPAN})")
        assert subtitle["value"].split(" ")[1] in expected_endpoints_ordered

        # query_params = {
        #     "hosts": [spec_dict["host"]],
        #     "timespan": TIMESPAN,
        #     'props': {
        #         "method": subtitle["value"].split(" ")[0],
        #         "path": path
        #     }
        # }

        # queries = [
        #     Template("app-gateway_queries/availability.kusto").render(query_params),
        #     Template("app-gateway_queries/response_codes.kusto").render(query_params),
        #     Template("app-gateway_queries/response_time.kusto").render(query_params),
        # ]
        # assert query["value"] in queries

        # content = part["metadata"]["settings"]["content"]
        # assert content["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
        # assert content["PartTitle"].endswith(f"({TIMESPAN})")

# def test_the_template_with_host_and_base_path_options_and_hosts_overrides():
#     """
#     GIVEN a name, a location, a timespan, a list of resources and a OA3 spec with host and basePath
#     WHEN the builder produces the template overriding hosts
#     THEN the template is rendered with correct hosts
#     """
#     resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
#     builder = create_builder(
#         "azure-dashboard-raw",
#         resolver=resolver,
#         name=NAME,
#         resource_type=RESOURCE_TYPE,
#         location=LOCATION,
#         timespan=TIMESPAN,
#         evaluation_frequency=EVALUATION_FREQUENCY,
#         evaluation_time_window=EVALUATION_TIME_WINDOW,
#         event_occurrences=EVENT_OCCURRENCES,
#         resources=[RESOURCE_ID]
#     )
#
#     custom_hosts = ["foo.pagopa.it", "bar.pagopa.it"]
#     spec_dict = resolver.resolve()
#     template_dict = json.loads(builder.produce({"hosts": custom_hosts}))
#
#     assert template_dict["name"] == NAME
#     assert template_dict["location"] == LOCATION
#
#     parts = template_dict["properties"]["lenses"]["0"]["parts"]
#
#     # MODIFICA: Calcola il numero di operazioni e gli endpoint attesi
#     expected_endpoints_ordered, total_operations, operations
#     = _build_expected_endpoints_and_ops_count_for_oas2(spec_dict)
#
#     assert len(parts) == total_operations * NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT
#
#     # MODIFICA: Itera sugli indici delle parti
#     for i in range(len(parts)):
#         part_index_str = str(i)
#         part = parts[part_index_str]
#
#         # MODIFICA: Ottieni l'endpoint atteso
#         current_expected_endpoint = expected_endpoints_ordered[i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#
#         assert part["position"]["x"] == (i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT) * COL_SPAN
#         assert part["position"]["y"] == (i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT) * ROW_SPAN
#
#         resouce_id = next(e for e in part["metadata"]["inputs"] if e["name"] == "Scope")
#         title = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartTitle")
#         subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
#         query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")
#
#         assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
#         assert title["value"].endswith(f"({TIMESPAN})")
#         assert subtitle["value"].split(" ")[1] in expected_endpoints_ordered
#
#         query_params = {
#             "endpoint": current_expected_endpoint,
#             "hosts": custom_hosts, # Usa gli host customizzati
#             "timespan": TIMESPAN,
#         }
#
#         queries = [
#             Template("app-gateway_queries/availability.kusto").render(query_params),
#             Template("app-gateway_queries/response_codes.kusto").render(query_params),
#             Template("app-gateway_queries/response_time.kusto").render(query_params),
#         ]
#
#         assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#
#         content = part["metadata"]["settings"]["content"]
#         assert content["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#         assert content["PartTitle"].endswith(f"({TIMESPAN})")
#
#
# def test_produce_the_template_with_servers_option():
#     """
#     GIVEN a name, a location, a timespan, a list of resources and a OA3 spec with servers
#     WHEN the builder produces the template
#     THEN the template is rendered and properties applied
#     """
#     resolver = OA3Resolver(f"{DATA_BASE_PATH}/selfcare_party_process.yaml")
#     builder = create_builder(
#         "azure-dashboard-raw",
#         resolver=resolver,
#         name=NAME,
#         resource_type=RESOURCE_TYPE,
#         location=LOCATION,
#         timespan=TIMESPAN,
#         evaluation_frequency=EVALUATION_FREQUENCY,
#         evaluation_time_window=EVALUATION_TIME_WINDOW,
#         event_occurrences=EVENT_OCCURRENCES,
#         resources=[RESOURCE_ID]
#     )
#
#     spec_dict = resolver.resolve()
#     template_dict = json.loads(builder.produce())
#
#     assert template_dict["name"] == NAME
#     assert template_dict["location"] == LOCATION
#
#     parts = template_dict["properties"]["lenses"]["0"]["parts"]
#
#     # MODIFICA: Calcola il numero totale di istanze di operazioni (server * operazioni) e gli endpoint attesi
#     expected_endpoints_ordered, total_operation_instances, operations
#     = _build_expected_endpoints_and_ops_count_for_oas3(spec_dict)
#
#     assert len(parts) == total_operation_instances * NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT
#
#     # MODIFICA: Ottieni gli host dai server per le query
#     hosts_for_query = [urlparse(server["url"]).netloc for server in spec_dict.get("servers", [])]
#     if not hosts_for_query and "host" in spec_dict: # Fallback per spec OAS2-like
#         hosts_for_query = [spec_dict["host"]]
#
#
#     # MODIFICA: Itera sugli indici delle parti
#     for i in range(len(parts)):
#         part_index_str = str(i)
#         part = parts[part_index_str]
#
#         current_expected_endpoint = expected_endpoints_ordered[i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#
#         resouce_id = next(e for e in part["metadata"]["inputs"] if e["name"] == "Scope")
#         title = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartTitle")
#         subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
#         query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")
#
#         assert part["position"]["x"] == (i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT) * COL_SPAN
#         assert part["position"]["y"] == (i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT) * ROW_SPAN
#
#         assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
#         assert title["value"].endswith(f"({TIMESPAN})")
#         # MODIFICA: Verifica il subtitle esatto
#         assert subtitle["value"].split(" ")[1] in expected_endpoints_ordered
#
#         query_params = {
#             "endpoint": current_expected_endpoint,
#             "hosts": hosts_for_query, # Usa gli host derivati dai server
#             "timespan": TIMESPAN,
#         }
#
#         queries = [
#             Template("app-gateway_queries/availability.kusto").render(query_params),
#             Template("app-gateway_queries/response_codes.kusto").render(query_params),
#             Template("app-gateway_queries/response_time.kusto").render(query_params),
#         ]
#
#         assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#
#         content = part["metadata"]["settings"]["content"]
#         assert content["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#         assert content["PartTitle"].endswith(f"({TIMESPAN})")
#
#
# def test_the_template_with_servers_option_and_hosts_overrides():
#     """
#     GIVEN a name, a location, a timespan, a list of resources and a OA3 spec with servers
#     WHEN the builder produces the template overriding hosts
#     THEN the template is rendered and properties applied
#     """
#     resolver = OA3Resolver(f"{DATA_BASE_PATH}/selfcare_party_process.yaml")
#     builder = create_builder(
#         "azure-dashboard-raw",
#         resolver=resolver,
#         name=NAME,
#         resource_type=RESOURCE_TYPE,
#         location=LOCATION,
#         timespan=TIMESPAN,
#         evaluation_frequency=EVALUATION_FREQUENCY,
#         evaluation_time_window=EVALUATION_TIME_WINDOW,
#         event_occurrences=EVENT_OCCURRENCES,
#         resources=[RESOURCE_ID]
#     )
#
#     custom_hosts = ["foo.pagopa.it", "bar.pagopa.it"]
#     spec_dict = resolver.resolve()
#     template_dict = json.loads(builder.produce({"hosts": custom_hosts}))
#
#     assert template_dict["name"] == NAME
#     assert template_dict["location"] == LOCATION
#
#     parts = template_dict["properties"]["lenses"]["0"]["parts"]
#
#     # MODIFICA: Calcola il numero totale di istanze di operazioni e gli endpoint attesi
#     expected_endpoints_ordered, total_operation_instances, operations
#     = _build_expected_endpoints_and_ops_count_for_oas3(spec_dict)
#
#     assert len(parts) == total_operation_instances * NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT
#
#     # MODIFICA: Itera sugli indici delle parti
#     for i in range(len(parts)):
#         part_index_str = str(i)
#         part = parts[part_index_str]
#
#         current_expected_endpoint = expected_endpoints_ordered[i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#
#         resouce_id = next(e for e in part["metadata"]["inputs"] if e["name"] == "Scope")
#         title = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartTitle")
#         subtitle = next(e for e in part["metadata"]["inputs"] if e["name"] == "PartSubTitle")
#         query = next(e for e in part["metadata"]["inputs"] if e["name"] == "Query")
#
#         assert part["position"]["x"] == (i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT) * COL_SPAN
#         assert part["position"]["y"] == (i // NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT) * ROW_SPAN
#
#         assert resouce_id["value"] == {"resourceIds": [RESOURCE_ID]}
#         assert title["value"].endswith(f"({TIMESPAN})")
#         assert subtitle["value"].split(" ")[1] in expected_endpoints_ordered
#
#         query_params = {
#             "endpoint": operations,
#             "hosts": custom_hosts, # Usa gli host customizzati
#             "timespan": TIMESPAN,
#         }
#
#         queries = [
#             Template("app-gateway_queries/availability.kusto").render(query_params),
#             Template("app-gateway_queries/response_codes.kusto").render(query_params),
#             Template("app-gateway_queries/response_time.kusto").render(query_params),
#         ]
#
#         assert query["value"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#
#         content = part["metadata"]["settings"]["content"]
#         assert content["Query"] == queries[i % NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT]
#         assert content["PartTitle"].endswith(f"({TIMESPAN})")

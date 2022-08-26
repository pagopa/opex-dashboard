import json

from src.opex_dashboard.azure_template import AZTemplate

AVAILABILITY_QUERY_PATH = "./test/data/availability-query.kusto"
RESPONSE_CODES_QUERY_PATH = "./test/data/response-codes-query.kusto"
RESPONSE_TIME_QUERY_PATH = "./test/data/response-time-query.kusto"

NAME = "DEV-IO/IO App Availability"
LOCATION = "West Europe"
HOSTS = ["app-backend.io.italia.it", "api-app.io.pagopa.it"]
ENDPOINTS = ["/api/v1/services/1", "/api/v1/profile"]

def test_render_availability():
    """
    GIVEN a list of hosts and an endpoint
    WHEN availability is rendered
    THEN the Kusto query is generated
    """
    template = AZTemplate(NAME, LOCATION)

    fin = open(AVAILABILITY_QUERY_PATH, "rt")
    kusto_query = fin.read()
    fin.close()

    assert template.availability(HOSTS, ENDPOINTS[0], False) == kusto_query

def test_render_response_codes():
    """
    GIVEN a list of hosts and an endpoint
    WHEN response codes is rendered
    THEN the Kusto query is generated
    """
    template = AZTemplate(NAME, LOCATION)

    fin = open(RESPONSE_CODES_QUERY_PATH, "rt")
    kusto_query = fin.read()
    fin.close()

    assert template.response_codes(HOSTS, ENDPOINTS[0], False) == kusto_query

def test_render_response_time():
    """
    GIVEN a list of hosts and an endpoint
    WHEN response time is rendered
    THEN the Kusto query is generated
    """
    template = AZTemplate(NAME, LOCATION)

    fin = open(RESPONSE_TIME_QUERY_PATH, "rt")
    kusto_query = fin.read()
    fin.close()

    assert template.response_time(HOSTS, ENDPOINTS[0], False) == kusto_query

def test_render_part():
    """
    GIVEN a name, a location, a list of hosts, and an endpoint
    WHEN a part is rendered
    THEN an Azure Dashboard json part property is generated
    """
    template = AZTemplate(NAME, LOCATION)

    properties = {
        "x": "0",
        "y": "0",
        "colspan": "6",
        "rowspan": "4",
        "query": template.availability(HOSTS, ENDPOINTS[0]),
        "scopes": [ "azure/resource/id" ],
        "title": "APIs Profile Availability (5min)",
        "subtitle": "io-d-appgateway",
        "range": "PT4H",
        "x_label": "TimeGenerated",
        "y_label": "Availability",
        "split_by": [ "something" ],
        "aggregation": "Sum",
    }

    part_dict = json.loads(template.render_part(properties))

    assert part_dict["position"]["x"] == int(properties["x"])
    assert part_dict["position"]["y"] == int(properties["y"])
    assert part_dict["position"]["colSpan"] == int(properties["colspan"])
    assert part_dict["position"]["rowSpan"] == int(properties["rowspan"])
    assert part_dict["metadata"]["settings"]["content"]["PartTitle"] == properties["title"]

    target = next((i for i in part_dict["metadata"]["inputs"] if i["name"] == "Query"), None)
    unraw_query = template.availability(HOSTS, ENDPOINTS[0], False)
    assert target["value"] == unraw_query
    assert part_dict["metadata"]["settings"]["content"]["Query"] == unraw_query

    target = next((i for i in part_dict["metadata"]["inputs"] if i["name"] == "Scope"), None)
    assert target["value"]["resourceIds"] == properties["scopes"]

    target = next((i for i in part_dict["metadata"]["inputs"] if i["name"] == "TimeRange"), None)
    assert target["value"] == properties["range"]

    target = next((i for i in part_dict["metadata"]["inputs"] if i["name"] == "PartSubTitle"), None)
    assert target["value"] == properties["subtitle"]

    target = next((i for i in part_dict["metadata"]["inputs"] if i["name"] == "Dimensions"), None)
    assert target["value"]["xAxis"]["name"] == properties["x_label"]
    assert target["value"]["yAxis"][0]["name"] == properties["y_label"]
    assert target["value"]["splitBy"] == properties["split_by"]
    assert target["value"]["aggregation"] == properties["aggregation"]

def test_render_template():
    """
    GIVEN a name, a location, a list of hosts, and a list of endpoints
    WHEN template is rendered
    THEN an Azure Dashboard json is generated
    """
    template = AZTemplate(NAME, LOCATION)

    template_dict = json.loads(template.render(HOSTS, ENDPOINTS))

    assert template_dict["name"] == NAME
    assert template_dict["tags"]["hidden-title"] == NAME
    assert template_dict["location"] == LOCATION
    assert isinstance(template_dict["properties"]["lenses"]["0"]["parts"], dict)
    assert len(template_dict["properties"]["lenses"]["0"]["parts"].keys()) == len(ENDPOINTS)

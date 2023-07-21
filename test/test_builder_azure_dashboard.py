from os.path import dirname, join

from opex_dashboard.builder_factory import create_builder
from opex_dashboard.resolver import OA3Resolver

DATA_BASE_PATH = join(dirname(__file__), "data")
NUMBER_OF_GRAPH_FOR_EACH_ENDPOINT = 3
NAME = "PROD-IO/IO App Availability"
RESOURCE_TYPE = "app-gateway"
RESOURCE_ID = ("/subscriptions/uuid/"
               "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
               "/applicationGateways/io-p-appgateway")
LOCATION = "West Europe"
TIMESPAN = "5m"
EVALUATION_FREQUENCY = 10
EVALUATION_TIME_WINDOW = 20
EVENT_OCCURRENCES = 2
DATA_SOURCE_ID = "data_source_id"
ACTION_GROUPS_IDS = ["/subscriptions/uuid/resourceGroups/my-rg/providers/"
                     "microsoft.insights/actionGroups/my-action-group-email",
                     "/subscriptions/uuid/resourceGroups/my-rg/providers/"
                     "microsoft.insights/actionGroups/my-action-group-slack"
                     ]
ROW_SPAN = 4
COL_SPAN = 6


def test_produce_the_template_with_no_overrides(snapshot):
    """
    GIVEN a valid list of parameter
    WHEN no overrides are defined
    THEN the template is rendered and properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend_light.yaml")
    builder = create_builder(
        "azure-dashboard",
        resolver=resolver,
        name=NAME,
        resource_type=RESOURCE_TYPE,
        location=LOCATION,
        timespan=TIMESPAN,
        evaluation_frequency=EVALUATION_FREQUENCY,
        evaluation_time_window=EVALUATION_TIME_WINDOW,
        event_occurrences=EVENT_OCCURRENCES,
        resources=[RESOURCE_ID],
        data_source_id=DATA_SOURCE_ID,
        action_groups_ids=ACTION_GROUPS_IDS
    )

    prova = builder.produce({})

    snapshot.snapshot_dir = 'test/snapshots'  # This line is optional.
    snapshot.assert_match(prova, 'iobackend_light_no_overrides.txt')


def test_produce_the_template_with_overrides(snapshot):
    """
    GIVEN a valid list of parameter
    WHEN overrides are defined for and endpoint
    THEN the template is rendered and override properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend_light.yaml")
    builder = create_builder(
        "azure-dashboard",
        resolver=resolver,
        name=NAME,
        resource_type=RESOURCE_TYPE,
        location=LOCATION,
        timespan=TIMESPAN,
        evaluation_frequency=EVALUATION_FREQUENCY,
        evaluation_time_window=EVALUATION_TIME_WINDOW,
        event_occurrences=EVENT_OCCURRENCES,
        resources=[RESOURCE_ID],
        data_source_id=DATA_SOURCE_ID,
        action_groups_ids=ACTION_GROUPS_IDS
    )

    overrides = {"endpoints": {"/api/v1/services/{service_id}": {"availability_threshold": 0.12,
                                                                 "availability_evaluation_frequency": 111,
                                                                 "availability_evaluation_time_window": 222,
                                                                 "availability_event_occurrences": 333,
                                                                 "response_time_threshold": 0.23,
                                                                 "response_time_evaluation_frequency": 444,
                                                                 "response_time_evaluation_time_window": 555,
                                                                 "response_time_event_occurrences": 666,
                                                                 }}}
    prova = builder.produce(overrides)

    snapshot.snapshot_dir = 'test/snapshots'  # This line is optional.
    snapshot.assert_match(prova, 'iobackend_light_overrides.txt')


def test_produce_the_template_with_overrided_base_path(snapshot):
    """
    GIVEN a valid list of parameter
    WHEN overrides are defined for and endpoint
    THEN the template is rendered and override properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend_light.yaml")
    builder = create_builder(
        "azure-dashboard",
        resolver=resolver,
        name=NAME,
        resource_type=RESOURCE_TYPE,
        location=LOCATION,
        timespan=TIMESPAN,
        evaluation_frequency=EVALUATION_FREQUENCY,
        evaluation_time_window=EVALUATION_TIME_WINDOW,
        event_occurrences=EVENT_OCCURRENCES,
        resources=[RESOURCE_ID],
        data_source_id=DATA_SOURCE_ID,
        action_groups_ids=ACTION_GROUPS_IDS
    )

    overrides = {"endpoints": {"/api/v1/services/{service_id}": {"availability_threshold": 0.12,
                                                                 "availability_evaluation_frequency": 111,
                                                                 "availability_evaluation_time_window": 222,
                                                                 "availability_event_occurrences": 333,
                                                                 "response_time_threshold": 0.23,
                                                                 "response_time_evaluation_frequency": 444,
                                                                 "response_time_evaluation_time_window": 555,
                                                                 "response_time_event_occurrences": 666,
                                                                 }},
                 "base_path": "basepath_override"
                                                                 }
    prova = builder.produce(overrides)

    snapshot.snapshot_dir = 'test/snapshots'  # This line is optional.
    snapshot.assert_match(prova, 'iobackend_light_overrides_base_path.txt')
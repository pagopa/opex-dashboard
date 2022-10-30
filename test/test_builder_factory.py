import pytest

from os.path import dirname, join

from opex_dashboard.builder_factory import create_builder
from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_dashboard_raw_builder import AzDashboardRawBuilder
from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.error import InvalidBuilderError

DATA_BASE_PATH = join(dirname(__file__), "data")


def test_create_a_basic_builder():
    """
    GIVEN a base builder type and a template
    WHEN the builder is created
    THEN it returns an instance of Builder
    """
    builder = create_builder("base", template="template.json")

    assert isinstance(builder, Builder)


def test_create_an_inexsiting_builder():
    """
    GIVEN an inexsiting builder type
    WHEN the builder is created
    THEN it returns None
    """
    builder = create_builder("unknow")

    assert not builder


def test_create_a_basic_builder_without_a_template():
    """
    GIVEN a base builder type
    WHEN the builder is created
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        create_builder("base")

    assert str(e.value).endswith("required positional argument: 'template'")


def test_create_a_basic_builder_with_an_invalid_template():
    """
    GIVEN a base builder type and a dict
    WHEN the builder is create with the dict as template name
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        create_builder("base", template={"foo": "bar"})

    assert str(e.value) == f"Invalid builder error: 'template' must be a {str}"


def test_create_a_basic_builder_with_invalid_base_properties():
    """
    GIVEN a base builder type and a str
    WHEN the builder is create with the str as base properites
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        create_builder("base", template_name="template.json", base_properties="foobar")

    assert str(e.value) == f"Invalid builder error: 'base_properties' must be a {dict}"


def test_create_an_azure_dashboard_raw_builder():
    """
    GIVEN an azure dashboard builder type, a resolver, a name, a location, a timespan, and a list of resources
    WHEN the builder is created
    THEN it returns an instance of AzDashboardRawBuilder
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
    builder = create_builder(
            "azure-dashboard",
            resolver=resolver,
            name="PROD-IO/IO App Availability",
            location="West Europe",
            timespan="5m",
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert isinstance(builder, AzDashboardRawBuilder)


def test_create_an_azure_dashboard_raw_builder_without_a_resolver():
    """
    GIVEN an azure dashboard builder type, a name, a location, a timespan, and a list of resources
    WHEN the builder is created
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        create_builder(
            "azure-dashboard",
            name="PROD-IO/IO App Availability",
            location="West Europe",
            timespan="5m",
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert str(e.value).endswith("required positional argument: 'resolver'")


def test_create_an_azure_dashboard_raw_builder_with_an_invalid_resolver():
    """
    GIVEN an azure dashboard builder type, a name, a location, a timespan, a list of resources, and a dict
    WHEN the builder is created with the dict as resolver
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        create_builder(
            "azure-dashboard",
            resolver={"foo": "bar"},
            name="PROD-IO/IO App Availability",
            location="West Europe",
            timespan="5m",
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert str(e.value) == f"Invalid builder error: 'resolver' must be a {OA3Resolver}"


def test_create_an_azure_dashboard_raw_builder_without_a_name():
    """
    GIVEN an azure dashboard builder type, a resolver, a location, a timespan, and a list of resources
    WHEN the builder is created
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
        create_builder(
            "azure-dashboard",
            resolver=resolver,
            location="West Europe",
            timespan="5m",
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert str(e.value).endswith("required positional argument: 'name'")


def test_create_an_azure_dashboard_raw_builder_with_an_invalid_name():
    """
    GIVEN an azure dashboard builder type, a resolver, a location, a timespan, a list of resources, and a dict
    WHEN the builder is created with the dict as resolver
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
        create_builder(
            "azure-dashboard",
            resolver=resolver,
            name={"foo": "bar"},
            location="West Europe",
            timespan="5m",
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert str(e.value) == f"Invalid builder error: 'name' must be a {str}"


def test_create_an_azure_dashboard_raw_builder_without_a_location():
    """
    GIVEN an azure dashboard builder type, a resolver, a name, a timespan, and a list of resources
    WHEN the builder is created
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
        create_builder(
            "azure-dashboard",
            resolver=resolver,
            name="PROD-IO/IO App Availability",
            timespan="5m",
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert str(e.value).endswith("required positional argument: 'location'")


def test_create_an_azure_dashboard_raw_builder_with_an_invalid_location():
    """
    GIVEN an azure dashboard builder type, a resolver, a name, a timespan, a list of resources, and a dict
    WHEN the builder is created with the dict as resolver
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
        create_builder(
            "azure-dashboard",
            resolver=resolver,
            name="PROD-IO/IO App Availability",
            location={"foo": "bar"},
            timespan="5m",
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert str(e.value) == f"Invalid builder error: 'location' must be a {str}"


def test_create_an_azure_dashboard_raw_builder_without_a_timespan():
    """
    GIVEN an azure dashboard builder type, a resolver, a name, a location, and a list of resources
    WHEN the builder is created
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
        create_builder(
            "azure-dashboard",
            resolver=resolver,
            name="PROD-IO/IO App Availability",
            location="West Europe",
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert str(e.value).endswith("required positional argument: 'timespan'")


def test_create_an_azure_dashboard_raw_builder_with_an_invalid_timespan():
    """
    GIVEN an azure dashboard builder type, a resolver, a name, a location, a list of resources, and a dict
    WHEN the builder is created with the dict as resolver
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
        create_builder(
            "azure-dashboard",
            resolver=resolver,
            name="PROD-IO/IO App Availability",
            location="West Europe",
            timespan={"foo": "bar"},
            resources=[("/subscriptions/uuid/"
                        "resourceGroups/io-p-rg-external/providers/Microsoft.Network"
                        "/applicationGateways/io-p-appgateway")])

    assert str(e.value) == f"Invalid builder error: 'timespan' must be a {str}"


def test_create_an_azure_dashboard_raw_builder_without_a_list_of_resources():
    """
    GIVEN an azure dashboard builder type, a resolver, a name, a timespan, and a location
    WHEN the builder is created
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
        create_builder(
            "azure-dashboard",
            resolver=resolver,
            name="PROD-IO/IO App Availability",
            location="West Europe",
            timespan="5m")

    assert str(e.value).endswith("required positional argument: 'resources'")


def test_create_an_azure_dashboard_raw_builder_with_an_invalid_list_of_resources():
    """
    GIVEN an azure dashboard builder type, a resolver, a name, a timespan, a list of resources, and a dict
    WHEN the builder is created with the dict as resolver
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
        create_builder(
            "azure-dashboard",
            resolver=resolver,
            name="PROD-IO/IO App Availability",
            location="West Europe",
            timespan="5m",
            resources={"foo": "bar"})

    assert str(e.value) == f"Invalid builder error: 'resources' must be a {list}"

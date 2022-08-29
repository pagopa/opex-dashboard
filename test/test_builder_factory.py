import pytest

from os.path import dirname, join

from opex_dashboard.builder_factory import BuilderFactory
from opex_dashboard.builders.base import Builder
from opex_dashboard.builders.azure_builder import AzDashboardBuilder
from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.error import InvalidBuilderError

DATA_BASE_PATH = join(dirname(__file__), "data")


def test_create_a_basic_builder():
    """
    GIVEN a base builder type and a template
    WHEN the builder is created
    THEN it retruns an instance of Builder
    """
    builder = BuilderFactory.create_builder("base", template_name="template.json")

    assert isinstance(builder, Builder)


def test_create_a_basic_builder_without_a_template():
    """
    GIVEN a base builder type
    WHEN the builder is created
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        BuilderFactory.create_builder("base")

    assert str(e.value) == "Invalid builder error: 'template_name' is mandatory with base"


def test_create_a_basic_builder_with_an_invalid_template_name():
    """
    GIVEN a base builder type and a dict
    WHEN the builder is create with the dict as template name
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        BuilderFactory.create_builder("base", template_name={"foo": "bar"})

    assert str(e.value) == "Invalid builder error: 'template_name' must be a string"


def test_create_a_basic_builder_with_invalid_base_properties():
    """
    GIVEN a base builder type and a str
    WHEN the builder is create with the str as base properites
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        BuilderFactory.create_builder("base", template_name="template.json", base_properties="foobar")

    assert str(e.value) == "Invalid builder error: 'base_properties' must be a dict"


def test_create_an_azure_dashboard_builder():
    """
    GIVEN an azure dashboard builder type and a resolver
    WHEN the builder is created
    THEN it retruns an instance of AzDashboardBuilder
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")
    builder = BuilderFactory.create_builder("azure-dashboard", resolver=resolver)

    assert isinstance(builder, AzDashboardBuilder)


def test_create_an_azure_dashboard_builder_without_a_resolver():
    """
    GIVEN an azure dashboard builder type
    WHEN the builder is created
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        BuilderFactory.create_builder("azure-dashboard")

    assert str(e.value) == "Invalid builder error: 'resolver' is mandatory with azure-dashboard"


def test_create_an_azure_dashboard_builder_with_an_invalid_resolver():
    """
    GIVEN an azure dashboard builder type and a dict
    WHEN the builder is created with the dict as resolver
    THEN it throws an exception
    """
    with pytest.raises(InvalidBuilderError) as e:
        BuilderFactory.create_builder("azure-dashboard", resolver={"foo": "bar"})

    assert str(e.value) == "Invalid builder error: 'resolver' must be an OA3Resolver"

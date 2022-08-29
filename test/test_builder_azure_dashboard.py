import json

from os.path import dirname, join

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.builder_factory import BuilderFactory
from opex_dashboard.builders.azure_builder import AzureBuilder

DATA_BASE_PATH = join(dirname(__file__), "data")


def test_produce_a_template():
    """
    GIVEN an Azure Dashboard builder
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io-backend.yaml")
    builder = BuilderFactory.create_builder("azure-dashboard", resolver=resolver)
    template_dict = json.loads(builder.produce())

    assert template_dict["name"] == "PROD-IO/IO App Availability"
    assert template_dict["location"] == "West Europe"
    # TODO add others

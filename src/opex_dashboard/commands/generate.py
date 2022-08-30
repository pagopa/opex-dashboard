import click

from typing import Tuple

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.builder_factory import create_builder
from opex_dashboard.error import InvalidBuilderError


def setup_required(ctx: click.Context, params: click.Option, value: str) -> str:
    if value == "azure-dashboard":
        for option in ctx.command.params:
            if option.name and option.name.startswith("az_"):
                option.required = True

    return value


@click.command()
@click.option("--template-name", "-t",
              required=True,
              type=click.Choice(["azure-dashboard"]),
              help="Name of the template.",
              callback=setup_required)
@click.option("--output-file", "-o",
              type=str,
              default=None,
              help="Save the output into a file.")
@click.option("--az-oa3-spec",
              type=str,
              required=False,
              default=None,
              help="OA3 spec file to generate the Azure Dashboard form.")
@click.option("--az-name",
              type=str,
              required=False,
              default=None,
              help="Name of the Azure Dashboard.")
@click.option("--az-location",
              type=str,
              required=False,
              default=None,
              help="Azure location.")
@click.option("--az-resource",
              type=str,
              required=False,
              default=None,
              multiple=True,
              help="Resource id of the gateway.")
def generate(
    template_name: str,
    az_oa3_spec: str,
    az_name: str,
    az_location: str,
    az_resource: Tuple[str],
    output_file: str) -> None:
    """Description
    """
    properties = {
        "resolver": OA3Resolver(az_oa3_spec),
        "name": az_name,
        "location": az_location,
        "resources": list(az_resource),
    }

    builder = create_builder(template=template_name, **properties)
    if not builder:
        raise InvalidBuilderError(f"Invalid builder error: unknown builder {template_name}")
    result = builder.produce()

    if output_file:
        file = open(output_file, "w")
        file.write(result)
        file.close()
    else:
        print(result)

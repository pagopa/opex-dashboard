import click
import yaml
import tempfile
import requests
import os

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.builder_factory import create_builder
from opex_dashboard.error import InvalidBuilderError


@click.command(short_help="Generate a dashboard definition.")
@click.option("--template-name", "-t",
              required=True,
              type=click.Choice(["azure-dashboard"]),
              help="Name of the template.")
@click.option("--config-file", "-c",
              type=click.File("r"),
              required=True,
              help="A yaml file with all params to create the template, use - value to get input from stdin.")
@click.option("--output-file", "-o",
              type=str,
              default=None,
              help="Save the output into a file.")
def generate(template_name: str,
             config_file: str,
             output_file: str) -> None:
    """Generate enables you to create a dashboard definition that could be
       imported in a compatible provider.
    """
    config = yaml.load(config_file, Loader=yaml.FullLoader)

    spec_path = config["oa3_spec"]
    if spec_path.startswith("http"):
        req = requests.get(spec_path)
        fd, spec_path = tempfile.mkstemp()
        os.write(fd, req.content)
        os.close(fd)

    properties = {
        "resolver": OA3Resolver(spec_path),
        "name": config["name"],
        "location": config["location"],
        "timespan": config["timespan"],
        "resources": config["resources"],
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

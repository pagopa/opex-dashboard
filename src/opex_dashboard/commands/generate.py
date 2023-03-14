import click
import yaml
import tempfile
import requests
import os

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.builder_factory import create_builder
from opex_dashboard.error import InvalidBuilderError
from opex_dashboard.error import ConfigError


@click.command(short_help="Generate a dashboard definition.")
@click.option("--template-name", "-t",
              required=True,
              type=click.Choice(["azure-dashboard", "azure-dashboard-raw"]),
              help="Name of the template.")
@click.option("--config-file", "-c",
              type=click.File("r"),
              required=True,
              help="A yaml file with all params to create the template, use - value to get input from stdin.")
@click.option("--package",
              type=click.Path(),
              is_flag=False,
              flag_value=os.getcwd(),
              default=None,
              help="Save the template as a package, by default it creates a folder in the current directory.")
def generate(template_name: str,
             config_file: str,
             package: str) -> None:
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

    allowed_resource_type = ["app-gateway", "api-management"]

    properties = {
        "resolver": OA3Resolver(spec_path),
        "name": config["name"],
        "resource_type": config.get("resource_type", "app-gateway"),
        "location": config["location"],
        "timespan": config.get("timespan", "5m"),
        "resources": [config["data_source"]],
        "data_source_id": config["data_source"],
        "action_groups_ids": config.get("action_groups", []),
    }

    if properties["resource_type"] not in allowed_resource_type:
        raise ConfigError(f"Invalid resource_type configuration: valid values are {allowed_resource_type}")

    builder = create_builder(template_type=template_name, **properties)
    if not builder:
        raise InvalidBuilderError(f"Invalid builder error: unknown builder {template_name}")

    overrides = config.get("overrides", {})
    if package:
        basepath = os.path.join(package, template_name)
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        builder.package(path=basepath, values=overrides)
    else:
        print(builder.produce(overrides))

import click

from typing import Dict, Any

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.builder import BuilderFactory
from opex_dashboard.error import InvalidBuilderError


def setup_required(ctx: click.Context, params: click.Option, value: str) -> str:
    if value == "azure-dashboard":
        option = next(o for o in ctx.command.params if o.name == 'oa3_spec')
        option.required = True
    return value


@click.command()
@click.option('--template-name', '-t',
              required=True,
              type=click.Choice(["azure-dashboard"]),
              help="Name of the template.",
              callback=setup_required)
@click.option('--output-file', '-o',
              type=str,
              default=None,
              help="Save the output into a file.")
@click.option('--oa3-spec',
              type=str,
              required=False,
              default=None,
              help="OA3 spec file")
def generate(template_name: str, oa3_spec: str, output_file: str) -> None:
    """Something
    """
    if oa3_spec.startswith("http"):
        print("download")  # TODO
    else:
        resolver = OA3Resolver(oa3_spec)
        builder = BuilderFactory.create_builder(template=template_name, resolver=resolver)
        if not builder:
            raise InvalidBuilderError(f"Invalid builder error: unknown builder {template_name}")
        result = builder.produce()
        if output_file:
            file = open(output_file, "w")
            file.write(result)
            file.close()
        else:
            print(result)

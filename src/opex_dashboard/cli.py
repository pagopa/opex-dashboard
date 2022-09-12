import click

from opex_dashboard.commands.generate import generate


@click.group()
def cli() -> None:
    """The OpEx Dashboard Command Line Interface is a tool to manage
       operational dashboards from an OA3 spec.
    """
    pass


cli.add_command(generate)

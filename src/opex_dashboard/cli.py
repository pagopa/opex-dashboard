import click

from opex_dashboard.commands.generate import generate


@click.group()
def cli() -> None:
    pass


cli.add_command(generate)

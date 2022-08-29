import click

from opex_dashboard.commands.generate import generate


@click.group()
def opex_dashboard() -> None:
    pass


opex_dashboard.add_command(generate)

if __name__ == "__main__":  # TODO substitute with setuptools
    opex_dashboard()

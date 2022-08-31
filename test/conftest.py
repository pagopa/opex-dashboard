import pytest

from os.path import dirname, join

from src.opex_dashboard.template import Template


@pytest.fixture(scope="session", autouse=True)
def add_templates_dir_to_django_engine() -> None:
    Template.engine.dirs.append(join(dirname(__file__), "data"))

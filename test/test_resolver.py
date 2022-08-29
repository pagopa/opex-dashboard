import pytest

from os.path import dirname, join

from opex_dashboard.resolver import OA3Resolver
from opex_dashboard.error import ParseError

DATA_BASE_PATH = join(dirname(__file__), "data")

def test_resolve_valid_spec():
    """
    GIVEN a valid OA3 spec
    WHEN a resolver is created
    THEN a dict representation of the spec is available
    """
    resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend.yaml")

    assert isinstance(resolver.resolve(), dict)

def test_resolve_malformed_spec():
    """
    GIVEN a malformed OA3 spec
    WHEN a resolver is created
    THEN an exception is throwed
    """
    with pytest.raises(ParseError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend_malformed.yaml")
        resolver.resolve()

    assert str(e.value).startswith("OA3 parsing error: ", 0)

def test_resolve_invalid_spec():
    """
    GIVEN an invalid OA3 spec
    WHEN a resolver is created
    THEN an exception is throwed
    """
    with pytest.raises(ParseError) as e:
        resolver = OA3Resolver(f"{DATA_BASE_PATH}/io_backend_invalid.yaml")
        resolver.resolve()

    assert str(e.value).startswith("OA3 validation error: ", 0)

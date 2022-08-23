import pytest

from src.opex_dashboard.resolver import OA3Resolver
from src.opex_dashboard.error import ParseError

OA3_FILEPATH = './test/data/io-backend.yaml'
MALFORMED_OA3_FILEPATH = './test/data/io-backend-malformed.yaml'
INVALID_OA3_FILEPATH = './test/data/io-backend-invalid.yaml'

MALFORMED_ERROR_MESSAGE = "OA3 parsing error"
INVALID_ERROR_MESSAGE = "OA3 validation error"

def test_resolve_valid_spec():
    """
    GIVEN a valid OA3 spec
    WHEN a resolver is created
    THEN a dict representation of the spec is available
    """
    resolver = OA3Resolver(OA3_FILEPATH)

    assert isinstance(resolver.resolve(), dict)

def test_resolve_malformed_spec():
    """
    GIVEN a malformed OA3 spec
    WHEN a resolver is created
    THEN an exception is throwed
    """
    with pytest.raises(ParseError) as e:
        resolver = OA3Resolver(MALFORMED_OA3_FILEPATH)
        resolver.resolve()

    assert str(e.value).startswith(MALFORMED_ERROR_MESSAGE, 0)

def test_resolve_invalid_spec():
    """
    GIVEN an invalid OA3 spec
    WHEN a resolver is created
    THEN an exception is throwed
    """
    with pytest.raises(ParseError) as e:
        resolver = OA3Resolver(INVALID_OA3_FILEPATH)
        resolver.resolve()

    assert str(e.value).startswith(INVALID_ERROR_MESSAGE, 0)

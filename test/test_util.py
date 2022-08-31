import pytest

from opex_dashboard.util import normalize_params


def test_normalize_params():
    """
    GIVEN some mapped values and their type
    WHEN all those values are normalized
    THEN it returns all the valid values
    """
    values = {
        "str_value": "this is a string",
        "int_value": 3,
        "list_value": [1, 2, 3],
        "dict_value": {"1": 1, "2": 2, "3": 3},
        "tuple_value": (1, 2, 3),
    }
    types = {
        "str_value": str,
        "int_value": int,
        "list_value": list,
        "dict_value": dict,
        "tuple_value": tuple,
    }
    inputs = normalize_params(values, types)

    assert "str_value" in inputs and inputs["str_value"] == values["str_value"]
    assert "int_value" in inputs and inputs["int_value"] == values["int_value"]
    assert "list_value" in inputs and inputs["list_value"] == values["list_value"]
    assert "dict_value" in inputs and inputs["dict_value"] == values["dict_value"]
    assert "tuple_value" in inputs and inputs["tuple_value"] == values["tuple_value"]


def test_normalize_params_with_selective_types():
    """
    GIVEN some mapped values and few of their type
    WHEN all those values are normalized
    THEN it returns only the valid values
    """
    values = {
        "str_value": "this is a string",
        "int_value": 3,
        "list_value": [1, 2, 3],
        "dict_value": {"1": 1, "2": 2, "3": 3},
        "tuple_value": (1, 2, 3),
    }
    types = {
        "str_value": str,
        "int_value": int,
    }
    inputs = normalize_params(values, types)

    assert "str_value" in inputs and inputs["str_value"] == values["str_value"]
    assert "int_value" in inputs and inputs["int_value"] == values["int_value"]
    assert "list_value" not in inputs
    assert "dict_value" not in inputs
    assert "tuple_value" not in inputs


def test_normalize_params_with_inexisting_type_definition():
    """
    GIVEN some mapped values, their type, and some additional type
    WHEN all those values are normalized
    THEN it returns all and only the valid values
    """
    values = {
        "str_value": "this is a string",
        "int_value": 3,
        "list_value": [1, 2, 3],
        "dict_value": {"1": 1, "2": 2, "3": 3},
        "tuple_value": (1, 2, 3),
    }
    types = {
        "str_value": str,
        "int_value": int,
        "list_value": list,
        "dict_value": dict,
        "tuple_value": tuple,
        "additional_value": int,
    }
    inputs = normalize_params(values, types)

    assert "str_value" in inputs and inputs["str_value"] == values["str_value"]
    assert "int_value" in inputs and inputs["int_value"] == values["int_value"]
    assert "list_value" in inputs and inputs["list_value"] == values["list_value"]
    assert "dict_value" in inputs and inputs["dict_value"] == values["dict_value"]
    assert "tuple_value" in inputs and inputs["tuple_value"] == values["tuple_value"]
    assert "additional_value" not in inputs


def test_normalize_params_with_invalid_type():
    """
    GIVEN some mapped values with an invalid one and their correct type
    WHEN all those values are normalized
    THEN it throws an exception
    """
    values = {
        "str_value": "this is a string",
        "int_value": 3,
        "list_value": (1, 2, 3),
        "dict_value": {"1": 1, "2": 2, "3": 3},
        "tuple_value": (1, 2, 3),
    }
    types = {
        "str_value": str,
        "int_value": int,
        "list_value": list,
        "dict_value": dict,
        "tuple_value": tuple,
    }

    with pytest.raises(TypeError) as e:
        normalize_params(values, types)

    assert str(e.value) == f"'list_value' must be a {list}"

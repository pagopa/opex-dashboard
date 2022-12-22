from typing import Dict, Any


def normalize_params(values: Dict[str, Any], types: Dict[str, Any]) -> Dict[str, Any]:
    """Check the type of one or more mapped values in a dict, it skips missing values declared in types

    Returns
        Dict[str, Any]: All the checked and valid values

    Raises:
        TypeError: If a value's type missmatch
    """
    inputs = {}
    for value in types:
        try:
            if not isinstance(values[value], types[value]):
                raise TypeError(f"'{value}' must be a {types[value]}")
            inputs[value] = values[value]
        except KeyError:
            continue  # ignore missing values

    return inputs


def override_with(source: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Deep override a dictionary with values in another one.

    Returns
        Dict[str, Any]: The resulting dictionary
    """
    result = source.copy()
    for key, value in overrides.items():
        if isinstance(value, dict):
            result[key] = override_with(source.get(key, {}), value)
        else:
            result[key] = value

    return result

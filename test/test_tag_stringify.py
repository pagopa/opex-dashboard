from opex_dashboard.tags.stringify import stringify


def test_stringify():
    """
    GIVEN an object
    WHEN it is given to stringify filter
    THEN the filter returns the repr of the object inside a double quotes
    """
    assert stringify("a string") == '"a string"'
    assert stringify("a string with\nnewline") == '"a string with\\nnewline"'
    assert stringify(["a", "list", "of", "string"]) == '["a", "list", "of", "string"]'
    assert stringify({"foo": "bar", "hello": "world"}) == '{"foo": "bar", "hello": "world"}'

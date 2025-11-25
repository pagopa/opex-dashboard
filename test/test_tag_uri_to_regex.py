from opex_dashboard.tags.uri_to_regex import uri_to_regex

PATH = "/api/v1/services"


def test_uri_to_regex():
    """
    GIVEN an object
    WHEN it is given to uri_to_regex filter
    THEN the filter replace all path parameters with regex [^/]+
    """
    assert uri_to_regex(f"{PATH}/{{serviceId}}") == f"{PATH}/[^/]+($|\\?)"
    assert uri_to_regex(f"{PATH}/{{serviceId}}/preferences") == f"{PATH}/[^/]+/preferences($|\\?)"
    assert uri_to_regex(f"{PATH}/{{serviceId}}/preferences/{{preferenceId}}") == f"{PATH}/[^/]+/preferences/[^/]+($|\\?)"

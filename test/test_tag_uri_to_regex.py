from opex_dashboard.tags.uri_to_regex import uri_to_regex


def test_uri_to_regex():
    """
    GIVEN an object
    WHEN it is given to uri_to_regex filter
    THEN the filter replace all path parameters with regex [^/]+
    """
    assert uri_to_regex("/api/v1/services/{serviceId}") == "/api/v1/services/[^/]+"
    assert uri_to_regex("/api/v1/services/{serviceId}/preferences") == "/api/v1/services/[^/]+/preferences"
    assert uri_to_regex("/api/v1/services/{serviceId}/preferences/{preferenceId}") == "/api/v1/services/[^/]+/preferences/[^/]+"

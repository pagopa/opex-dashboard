from opex_dashboard.tags.mul import mul

def test_multiplication():
    """
    GIVEN a value and a factor
    WHEN they are given to mul filter
    THEN the filter returns their product
    """
    assert mul(2, 3) == 6
    assert mul(0, 3) == 0
    assert mul(2, -3) == -6

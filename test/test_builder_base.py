import json

from opex_dashboard.builder_factory import create_builder


def test_produce_a_template_without_base_properties():
    """
    GIVEN a base builder
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    values = {
        "debug": "off",
        "window": {"title": "My Window"},
        "image": {"offset": 200}
    }

    builder = create_builder("base", template_name="template.json")
    template_dict = json.loads(builder.produce(values))

    assert template_dict["widget"]["debug"] == values["debug"]
    assert template_dict["widget"]["window"]["title"] == values["window"]["title"]
    assert template_dict["widget"]["image"]["hOffset"] == values["image"]["offset"]
    assert template_dict["widget"]["image"]["vOffset"] == values["image"]["offset"]


def test_produce_a_template_with_base_properties():
    """
    GIVEN a base builder
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    values = {
        "debug": "off",
        "window": {"title": "My Window"},
        "image": {"offset": 200}
    }

    builder = create_builder("base", template_name="template.json", base_properties=values)
    template_dict = json.loads(builder.produce())

    assert template_dict["widget"]["debug"] == values["debug"]
    assert template_dict["widget"]["window"]["title"] == values["window"]["title"]
    assert template_dict["widget"]["image"]["hOffset"] == values["image"]["offset"]
    assert template_dict["widget"]["image"]["vOffset"] == values["image"]["offset"]


def test_produce_a_template_overwriting_base_properties():
    """
    GIVEN a base builder
    WHEN the builder produces the template
    THEN the template is rendered and properties applied
    """
    values = {
        "debug": "off",
        "window": {"title": "My Window"},
        "image": {"offset": 200}
    }

    base_values = values | {"debug": "on"}

    builder = create_builder("base", template_name="template.json", base_properties=base_values)
    template_dict = json.loads(builder.produce(values))

    assert template_dict["widget"]["debug"] == values["debug"]
    assert template_dict["widget"]["window"]["title"] == values["window"]["title"]
    assert template_dict["widget"]["image"]["hOffset"] == values["image"]["offset"]
    assert template_dict["widget"]["image"]["vOffset"] == values["image"]["offset"]

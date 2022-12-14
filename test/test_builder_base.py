import os
import json
import tempfile

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

    builder = create_builder("base", template="template.json")
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

    builder = create_builder("base", template="template.json", base_properties=values)
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

    builder = create_builder("base", template="template.json", base_properties=base_values)
    template_dict = json.loads(builder.produce(values))

    assert template_dict["widget"]["debug"] == values["debug"]
    assert template_dict["widget"]["window"]["title"] == values["window"]["title"]
    assert template_dict["widget"]["image"]["hOffset"] == values["image"]["offset"]
    assert template_dict["widget"]["image"]["vOffset"] == values["image"]["offset"]


def test_package_a_template():
    """
    GIVEN a base builder
    WHEN the builder packages the template
    THEN the template is rendered and saved into a file
    """
    values = {
        "debug": "off",
        "window": {"title": "My Window"},
        "image": {"offset": 200}
    }

    builder = create_builder("base", template="template.json")
    basedir = tempfile.mkdtemp()
    builder.package(basedir, values)

    with open(os.path.join(basedir, "template.json")) as file:
        template_dict = json.loads(file.read())

        assert template_dict["widget"]["debug"] == values["debug"]
        assert template_dict["widget"]["window"]["title"] == values["window"]["title"]
        assert template_dict["widget"]["image"]["hOffset"] == values["image"]["offset"]
        assert template_dict["widget"]["image"]["vOffset"] == values["image"]["offset"]

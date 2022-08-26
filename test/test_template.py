import json
import pytest

from os.path import dirname, join

from opex_dashboard.template import Template
from opex_dashboard.error import FileError

Template.engine.dirs = [join(dirname(__file__), "data")]

def test_render_existing_template():
    """
    GIVEN a template with {{ debug }}, {{ window.title }}, and {{ image.offset }} tags
    WHEN all values are applied and the template is rendered
    THEN it returns the template with the substitutions
    """
    values = {
        "debug": "off",
        "window": { "title": "My Window" },
        "image": { "offset": 200 }
    }

    template = Template("template.json")
    template_dict = json.loads(template.render(values))

    assert template_dict["widget"]["debug"] == values["debug"]
    assert template_dict["widget"]["window"]["title"] == values["window"]["title"]
    assert template_dict["widget"]["image"]["hOffset"] == values["image"]["offset"]
    assert template_dict["widget"]["image"]["vOffset"] == values["image"]["offset"]

def test_render_inexisting_template():
    """
    GIVEN a missing file template
    WHEN the template is created
    THEN it throws an exception
    """
    values = {
        "debug": "off",
        "window": { "title": "My Window" },
        "image": { "offset": 200 }
    }

    with pytest.raises(FileError) as e:
        template = Template("missing_template.json")

    assert str(e.value) == "Template file missing error: missing_template.json"

def test_render_without_all_tags():
    """
    GIVEN a template with {{ debug }}, {{ window.title }}, and {{ image.offset }} tags
    WHEN only image.offset is applied and the template is rendered
    THEN it returns the template with empty value for missing tags
    """
    values = {
        "image": { "offset": 200 }
    }

    template = Template("template.json")
    template_dict = json.loads(template.render(values))

    assert not template_dict["widget"]["debug"]
    assert not template_dict["widget"]["window"]["title"]
    assert template_dict["widget"]["image"]["hOffset"] == values["image"]["offset"]
    assert template_dict["widget"]["image"]["vOffset"] == values["image"]["offset"]

def test_render_with_inexistent_tag():
    """
    GIVEN a template without {{ empty }}
    WHEN empty is applied and the template is rendered
    THEN it returns the template and ignore inexistent tag
    """
    values = {
        "empty": "undefined",
        "debug": "off",
        "window": { "title": "My Window" },
        "image": { "offset": 200 }
    }

    template = Template("template.json")
    template_dict = json.loads(template.render(values))

    assert template_dict["widget"]["debug"] == values["debug"]
    assert template_dict["widget"]["window"]["title"] == values["window"]["title"]
    assert template_dict["widget"]["image"]["hOffset"] == values["image"]["offset"]
    assert template_dict["widget"]["image"]["vOffset"] == values["image"]["offset"]

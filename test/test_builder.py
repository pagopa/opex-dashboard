import pytest
import json

from src.opex_dashboard.builder import Builder
from src.opex_dashboard.error import PlaceholderError, RenderError

TEMPLATE_FILEPATH = "./test/data/template.json"

DEBUG_VALUE = "off"
WINDOW_TITLE_VALUE = "My window"
IMAGE_OFFSET_VALUE = "250"

PLACEHOLDER_ERROR_MESSAGE = "Missing placeholder error"
RENDER_ERROR_MESSAGE = "Render error"

def test_render_complete_template():
    """
    GIVEN a template with ${debug}, ${window_title}, and ${image_offset} placeholders
    WHEN all values are applied and the template is rendered
    THEN it returns the template with the substitutions
    """
    builder = Builder(TEMPLATE_FILEPATH)
    builder.apply("debug", DEBUG_VALUE)
    builder.apply("window_title", WINDOW_TITLE_VALUE)
    builder.apply("image_offset", IMAGE_OFFSET_VALUE)

    template_dict = json.loads(builder.render())

    assert template_dict["widget"]["debug"] == DEBUG_VALUE
    assert template_dict["widget"]["window"]["title"] == WINDOW_TITLE_VALUE
    assert template_dict["widget"]["image"]["hOffset"] == int(IMAGE_OFFSET_VALUE)
    assert template_dict["widget"]["image"]["vOffset"] == int(IMAGE_OFFSET_VALUE)

def test_render_incomplete_template():
    """
    GIVEN a template with ${debug}, ${window_title}, and ${image_offset} placeholders
    WHEN only debuy value is applied and the template is rendered
    THEN an exception is throwed
    """
    with pytest.raises(RenderError) as e:
        builder = Builder(TEMPLATE_FILEPATH)
        builder.apply("debug", DEBUG_VALUE)

        template_dict = json.loads(builder.render())

    unsets = ['${window_title}', '${image_offset}', '${image_offset}']
    assert str(e.value).startswith(f"{RENDER_ERROR_MESSAGE}: unset {unsets}", 0)

def test_check_existing_placeholder():
    """
    GIVEN a template with ${debug} placeholder
    WHEN check the existence of debug placholder
    THEN it returns True
    """
    builder = Builder(TEMPLATE_FILEPATH)

    assert builder.hasplaceholder("debug")

def test_check_inexisting_placeholder():
    """
    GIVEN a template without ${empty} placeholder
    WHEN check the existence of debug placholder
    THEN it returns False
    """
    builder = Builder(TEMPLATE_FILEPATH)

    assert not builder.hasplaceholder("empty")

def test_apply_existing_placeholder():
    """
    GIVEN a template with ${debug}, ${window_title}, and ${image_offset} placeholders
    WHEN values are applied
    THEN a compiled template is available
    """
    builder = Builder(TEMPLATE_FILEPATH)
    builder.apply("debug", DEBUG_VALUE)
    builder.apply("window_title", WINDOW_TITLE_VALUE)
    builder.apply("image_offset", IMAGE_OFFSET_VALUE)

    template_dict = json.loads(builder._template)

    assert template_dict["widget"]["debug"] == DEBUG_VALUE
    assert template_dict["widget"]["window"]["title"] == WINDOW_TITLE_VALUE
    assert template_dict["widget"]["image"]["hOffset"] == int(IMAGE_OFFSET_VALUE)
    assert template_dict["widget"]["image"]["vOffset"] == int(IMAGE_OFFSET_VALUE)

def test_apply_inexisting_placeholder():
    """
    GIVEN a template without ${empty} placeholder
    WHEN the empty is applied
    THEN an exception is throwed
    """
    with pytest.raises(PlaceholderError) as e:
        builder = Builder(TEMPLATE_FILEPATH)
        builder.apply("empty", DEBUG_VALUE)

    assert str(e.value).startswith(f"{PLACEHOLDER_ERROR_MESSAGE}: empty", 0)

def test_case_sensitive_placeholder():
    """
    GIVEN a template with ${debug} placeholder and no ${DEBUG}
    WHEN the debug is applied
    THEN an exception is throwed
    """
    with pytest.raises(PlaceholderError) as e:
        builder = Builder(TEMPLATE_FILEPATH)
        builder.apply("DEBUG", DEBUG_VALUE)

    assert not builder.hasplaceholder("DEBUG")
    assert str(e.value).startswith(f"{PLACEHOLDER_ERROR_MESSAGE}: DEBUG", 0)

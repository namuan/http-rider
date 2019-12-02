from httprider.core import abbreviate, template_sub
from uuid import UUID


def test_abbreviate():
    assert abbreviate("Hello World", 5) == "Hello ..."


def test_template_sub_variable():
    templated_str = "Hello ${name}"
    tokens = dict(
        name='John Doe'
    )
    output = template_sub(templated_str, tokens)
    assert output == "Hello John Doe"


def test_template_sub_uuid_generator():
    templated_str = "${uuid()}"
    output = template_sub(templated_str, {})
    assert UUID(output, version=4)


def test_template_sub_random_string_generator():
    inp = "${random(10, True, True)}"
    output = template_sub(inp, {})
    assert len(output) == 10
    assert isinstance(output, str)

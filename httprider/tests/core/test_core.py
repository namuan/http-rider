from httprider.core import abbreviate, template_sub, evaluate_nested_functions
from uuid import UUID
from httprider.core.util_functions import str_to_base64e


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


def test_template_sub_base_64_encoder():
    inp_str = "Hello"
    inp = '${utils("base64Encode", "' + inp_str + '")}'
    output = template_sub(inp, {})
    assert output == str_to_base64e(inp_str)


def test_evaluate_nested_functions():
    inp = '${utils("base64Encode", "${custom("**#-#**", True)}")}'
    output = evaluate_nested_functions(inp)
    assert "base64Encode" not in output

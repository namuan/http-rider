from httprider.presenters import assertion_variable_name


def test_assertion_variable_name():
    # given
    api_call_title = "[A -> B] Get Something"
    assertion_source = "request_body"
    input_str = "$.name"
    # when
    var_name = assertion_variable_name(api_call_title, assertion_source, input_str)
    # then
    assert var_name == "var_a___b_get_something_request_body__name"

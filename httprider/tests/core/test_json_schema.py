import json

from httprider.core.json_schema import schema_from_json


def test_generate_schema_from_json():
    # given
    raw_json = json.dumps(
        dict(
            name="john doe",
            age=51,
            height=5.10,
            addresses=[],
            balance=dict(amount=1000, currency="GBP"),
        )
    )
    # when
    generated_schema = schema_from_json(raw_json).get("schema")
    # then
    assert generated_schema is not None
    assert generated_schema.get("type") == "object"

    object_properties = generated_schema.get("properties")
    assert object_properties.get("name").get("type") == "string"
    assert object_properties.get("age").get("type") == "integer"
    assert object_properties.get("height").get("type") == "number"
    assert object_properties.get("addresses").get("type") == "array"
    assert object_properties.get("balance").get("type") == "object"
    balance_properties = object_properties.get("balance").get("properties")
    assert balance_properties.get("amount").get("type") == "integer"
    assert balance_properties.get("currency").get("type") == "string"

    assert "name" in generated_schema.get("required")
    assert "age" in generated_schema.get("required")
    assert "height" in generated_schema.get("required")


def test_generate_schema_with_no_required_fields():
    # given
    raw_json = json.dumps(
        dict(
            name="john doe",
            age=51,
            height=5.10,
            addresses=[],
            balance=dict(amount=1000, currency="GBP"),
        )
    )
    # when
    generated_schema = schema_from_json(raw_json, remove_required=True).get("schema")
    # then
    assert generated_schema.get("required") is None
    assert generated_schema.get("properties").get("balance").get("required") is None

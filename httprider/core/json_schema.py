import json
from json import JSONDecodeError

from .json_generator import *
import genson


def json_from_schema(json_schema):
    schema_type = json_schema.get("type", "object")
    if schema_type == "array":
        return fuzz_array(json_schema)
    elif schema_type == "object" and json_schema.get("properties"):
        return fuzz_object(json_schema["properties"])


def schema_from_json(json_body):
    try:
        j = json.loads(json_body)
        s = genson.SchemaBuilder(schema_uri=None)
        s.add_object(j)
        return {"schema": s.to_schema()}
    except JSONDecodeError:
        return {}

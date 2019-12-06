import json
from json import JSONDecodeError

import genson
from contextlib import suppress


def __delete_nested_keys(nested_dict, keys):
    for k in keys:
        with suppress(KeyError):
            del nested_dict[k]
    for ke, v in nested_dict.items():
        if isinstance(v, dict):
            __delete_nested_keys(v, keys)


def schema_from_json(json_body, remove_required=False):
    try:
        j = json.loads(json_body)
        s = genson.SchemaBuilder(schema_uri=None)
        s.add_object(j)
        schema = s.to_schema()
        if remove_required:
            __delete_nested_keys(schema, ["required"])
        return {"schema": schema}
    except JSONDecodeError:
        return {}

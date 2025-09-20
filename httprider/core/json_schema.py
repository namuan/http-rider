import json
from contextlib import suppress
from json import JSONDecodeError

import genson


def __delete_nested_keys(nested_dict, keys):
    for k in keys:
        with suppress(KeyError):
            del nested_dict[k]
    for v in nested_dict.values():
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

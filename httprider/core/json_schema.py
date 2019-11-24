import json
from json import JSONDecodeError

import genson


def schema_from_json(json_body):
    try:
        j = json.loads(json_body)
        s = genson.SchemaBuilder(schema_uri=None)
        s.add_object(j)
        return {"schema": s.to_schema()}
    except JSONDecodeError:
        return {}

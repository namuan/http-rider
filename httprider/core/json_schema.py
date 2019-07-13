from .json_generator import *


def json_from_schema(json_schema):
    schema_type = json_schema.get('type', 'object')
    if schema_type == 'array':
        return fuzz_array(json_schema)
    elif schema_type == 'object' and json_schema.get('properties'):
        return fuzz_object(json_schema['properties'])

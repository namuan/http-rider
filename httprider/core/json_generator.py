import string
from random import randint, getrandbits, choices


def rand_int(upper_limit, lower_limit=0):
    return randint(lower_limit, upper_limit)


def fuzz_boolean(boolean_schema):
    return bool(getrandbits(1))


def fuzz_date_time():
    year = rand_int(2018, 1990)
    month = rand_int(12, 1)
    day = rand_int(30, 1)
    hour = rand_int(24, 1)
    minute = rand_int(60, 1)
    second = rand_int(60, 1)

    return "%s-%02d-%02dT%02d:%02d:%02d.000+00:00" % (
        year,
        month,
        day,
        hour,
        minute,
        second,
    )


def fuzz_string(string_schema):
    is_enum = string_schema.get("enum")
    string_format = string_schema.get("format")
    if is_enum:
        # get a random item from list
        return is_enum[rand_int(len(is_enum) - 1)]

    if string_format == "date-time":
        return fuzz_date_time()

    return "".join(choices(string.ascii_uppercase + string.digits, k=rand_int(100)))


def fuzz_int(int_schema):
    return rand_int(1000, 1)


def fuzz_file(file_schema):
    return ""


def fuzz_array_length(num_items=10):
    return rand_int(num_items)


def fuzz_array(arr_schema, arr_length=fuzz_array_length()):
    items = arr_schema.get("items")
    if not items:
        return []

    arr_items_type = items.get("type", "object")
    fuzz_func = type_mapping.get(arr_items_type)
    if arr_items_type == "object":
        return [
            fuzz_object(arr_schema["items"]["properties"]) for o in range(arr_length)
        ]
    else:
        return [fuzz_func(items) for _ in range(arr_length)]


def fuzz_object(root_properties):
    obj_root = {}
    for k, v in root_properties.items():
        prop_type = v.get("type", "object")
        if prop_type != "object":
            fuzz_func = type_mapping.get(prop_type)
            obj_root[k] = fuzz_func(v)
        else:
            obj_root[k] = fuzz_object(v.get("properties", {}))

    return obj_root


type_mapping = {
    "integer": fuzz_int,
    "number": fuzz_int,
    "boolean": fuzz_boolean,
    "string": fuzz_string,
    "array": fuzz_array,
    "file": fuzz_file,
}

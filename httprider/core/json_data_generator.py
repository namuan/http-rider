import string
import sys
from random import randint, getrandbits, choices

DEFAULT_INT_UPPER_LIMIT = sys.maxsize
DEFAULT_INT_LOWER_LIMIT = -1 * sys.maxsize
DEFAULT_STRING_MAX_LENGTH = 250
DEFAULT_ARRAY_MAX_LENGTH = 10


class JsonDataGenerator:
    def __init__(self):
        self.type_mapping = {
            "integer": self.fuzz_int,
            "number": self.fuzz_int,
            "boolean": self.fuzz_boolean,
            "string": self.fuzz_string,
            "array": self.fuzz_array,
            "file": self.fuzz_file,
        }
        self.int_upper_limit = DEFAULT_INT_UPPER_LIMIT
        self.int_lower_limit = DEFAULT_INT_LOWER_LIMIT
        self.string_max_length = DEFAULT_STRING_MAX_LENGTH
        self.array_max_length = DEFAULT_ARRAY_MAX_LENGTH

    def update_limits(self, string_ml, array_ml):
        self.string_max_length = string_ml
        self.array_max_length = array_ml

    def rand_int(self, upper_limit, lower_limit):
        return randint(lower_limit, upper_limit)

    def fuzz_boolean(self, boolean_schema):
        return bool(getrandbits(1))

    def fuzz_date_time(self):
        year = self.rand_int(2018, 1990)
        month = self.rand_int(12, 1)
        day = self.rand_int(30, 1)
        hour = self.rand_int(24, 1)
        minute = self.rand_int(60, 1)
        second = self.rand_int(60, 1)

        return "%s-%02d-%02dT%02d:%02d:%02d.000+00:00" % (
            year,
            month,
            day,
            hour,
            minute,
            second,
        )

    def fuzz_string(self, string_schema):
        is_enum = string_schema.get("enum")
        string_format = string_schema.get("format")
        if is_enum:
            return is_enum[self.rand_int(len(is_enum) - 1, 0)]

        if string_format == "date-time":
            return self.fuzz_date_time()

        string_length = self.rand_int(self.string_max_length, 0)
        return "".join(choices(string.ascii_uppercase + string.digits, k=string_length))

    def fuzz_int(self, int_schema):
        return self.rand_int(self.int_upper_limit, self.int_lower_limit)

    def fuzz_file(self, file_schema):
        return ""

    def fuzz_array(self, arr_schema):
        items = arr_schema.get("items")
        if not items:
            return []

        arr_items_type = items.get("type", "object")
        arr_length = self.rand_int(self.array_max_length, 0)
        if arr_items_type == "object":
            return [
                self.fuzz_object(arr_schema["items"]["properties"])
                for _ in range(arr_length)
            ]
        else:
            fuzz_func = self.type_mapping.get(arr_items_type)
            return [fuzz_func(items) for _ in range(arr_length)]

    def fuzz_object(self, root_properties):
        obj_root = {}
        for k, v in root_properties.items():
            prop_type = v.get("type", "object")
            if prop_type != "object":
                fuzz_func = self.type_mapping.get(prop_type)
                obj_root[k] = fuzz_func(v)
            else:
                obj_root[k] = self.fuzz_object(v.get("properties", {}))

        return obj_root

    def json_from_schema(self, json_schema):
        schema_type = json_schema.get("type", "object")
        if schema_type == "array":
            return self.fuzz_array(json_schema)
        elif schema_type == "object" and json_schema.get("properties"):
            return self.fuzz_object(json_schema["properties"])


jdg = JsonDataGenerator()

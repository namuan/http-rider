import re

import stringcase

__type_mapping = {
    "integer": "int",
    "number": "int",
    "boolean": "boolean",
    "string": "String",
}


def __norm(name):
    return re.sub(r"[^a-zA-Z]", "", name)


def to_java_function_name(name):
    return stringcase.camelcase(__norm(name))


def to_java_class_name(name):
    return __norm(name).capitalize()


def to_java_variable(var_name):
    return stringcase.camelcase(__norm(var_name))


def gen_class_variable(var_name, var_type, is_array=False):
    # print("--> Class Variable: {}".format(var_name))
    json_type = var_type.get("type")
    if json_type == "object":
        class_declaration = f"{var_name.capitalize()} {var_name};"
        return (
            class_declaration
            + "\n"
            + gen_class(var_name.capitalize(), var_type.get("properties"))
        )
    if json_type == "array":
        return gen_array(var_name, var_type)

    java_type = __type_mapping.get(json_type, f"Unhandled type {json_type}")
    if is_array:
        return "List<{}> {};".format(java_type, to_java_variable(var_name))
    else:
        return "{} {};".format(java_type, to_java_variable(var_name))


def gen_class(clazz_name, clazz_properties):
    # print("-> Class {}".format(clazz_name))
    properties = (
        [gen_class_variable(*j) for j in clazz_properties.items()]
        if clazz_properties
        else []
    )
    properties_str = "\n".join(properties)
    return f"""
public class {clazz_name} {{
    {properties_str}
}}    
    """


def gen_array(var_name, json_schema):
    # print("--> Array {}".format(var_name))
    array_items = json_schema.get("items")
    if array_items.get("type") == "object":
        clazz_name = var_name.capitalize()
        item_class = gen_class(clazz_name, array_items.get("properties"))
        return item_class + "\n" + "List<{}> {};".format(clazz_name, var_name)
    else:
        rv = gen_class_variable(var_name, array_items, is_array=True)
        return rv


def code_from_schema(root_clazz, json_schema):
    schema_type = json_schema.get("type", "object")
    if schema_type == "array":
        return gen_array("Root", json_schema)
    elif schema_type == "object" and json_schema.get("properties"):
        return gen_class(root_clazz, json_schema["properties"])


if __name__ == "__main__":
    # test_schema = {
    #     "schema": {
    #         "type": "object",
    #         "properties": {
    #             "name": {"type": "string"},
    #             "amount": {
    #                 "type": "object",
    #                 "properties": {
    #                     "value": {"type": "integer"},
    #                     "currency": {"type": "string"},
    #                 },
    #                 "required": ["currency", "value"],
    #             },
    #             "references": {"type": "array", "items": {"type": "string"}},
    #         },
    #         "required": ["amount", "name", "references"],
    #     }
    # }
    test_schema = {
        "schema": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "object",
                    "properties": {"username": {"type": "string"}},
                    "required": ["username"],
                },
                "data": {"type": "string"},
                "files": {"type": "object"},
                "form": {"type": "object"},
                "headers": {
                    "type": "object",
                    "properties": {
                        "Accept": {"type": "string"},
                        "Accept-Encoding": {"type": "string"},
                        "Connection": {"type": "string"},
                        "Content-Length": {"type": "string"},
                        "Content-Type": {"type": "string"},
                        "Host": {"type": "string"},
                        "User-Agent": {"type": "string"},
                        "X-Correlation-Id": {"type": "string"},
                        "X-Shared": {"type": "string"},
                    },
                    "required": [
                        "Accept",
                        "Accept-Encoding",
                        "Connection",
                        "Content-Length",
                        "Content-Type",
                        "Host",
                        "User-Agent",
                        "X-Correlation-Id",
                        "X-Shared",
                    ],
                },
                "json": {
                    "type": "object",
                    "properties": {
                        "amount": {
                            "type": "object",
                            "properties": {
                                "currency": {"type": "string"},
                                "value": {"type": "integer"},
                            },
                            "required": ["currency", "value"],
                        },
                        "name": {"type": "string"},
                        "references": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["amount", "name", "references"],
                },
                "origin": {"type": "string"},
                "url": {"type": "string"},
            },
            "required": [
                "args",
                "data",
                "files",
                "form",
                "headers",
                "json",
                "origin",
                "url",
            ],
        }
    }
    code = code_from_schema("ApiRequest", test_schema.get("schema"))
    print("--- " * 50)
    print(code)

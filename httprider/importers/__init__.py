import cattr


def structure_attrs_from_dict(obj, cl):
    # type: (Mapping, Type) -> Any
    """Instantiate an attrs class from a mapping (dict)."""
    # For public use.

    # conv_obj = obj.copy()  # Dict of converted parameters.
    conv_obj = {}  # Start fresh

    # dispatch = self._structure_func.dispatch
    dispatch = cattr.global_converter._structure_func.dispatch  # Ugly I know
    for a in cl.__attrs_attrs__:
        # We detect the type by metadata.
        type_ = a.type
        if type_ is None:
            # No type.
            continue
        name = a.name
        try:
            val = obj[name]
        except KeyError:
            continue
        conv_obj[name] = dispatch(type_)(val, type_)

    return cl(**conv_obj)


# Import statements after any function definitions as they are using
# from the importers
# ruff: noqa: E402
from . import importer_curl, importer_openapi_v3, importer_postman_collections

importer_plugins = [importer_curl, importer_openapi_v3, importer_postman_collections]

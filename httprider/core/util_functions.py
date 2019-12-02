import base64

from httprider.core.constants import UTF_8_ENCODING


def str_to_base64e(arg, url_safe=False):
    if not arg:
        return ""

    if url_safe:
        return base64.urlsafe_b64encode(bytes(arg, UTF_8_ENCODING)).decode(
            UTF_8_ENCODING
        )
    else:
        return base64.b64encode(bytes(arg, UTF_8_ENCODING)).decode(UTF_8_ENCODING)


def str_to_base64d(arg, url_safe=False):
    if not arg:
        return ""

    if url_safe:
        return base64.urlsafe_b64decode(arg).decode(UTF_8_ENCODING)
    else:
        return base64.b64decode(arg).decode(UTF_8_ENCODING)


utility_func_map = {"base64Encode": str_to_base64e, "base64Decode": str_to_base64d}

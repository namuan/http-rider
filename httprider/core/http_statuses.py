def is_2xx(response_code):
    return 200 <= response_code < 300


def is_3xx(response_code):
    return 300 <= response_code < 400


def is_4xx(response_code):
    return 400 <= response_code < 500


def is_5xx(response_code):
    return response_code >= 500

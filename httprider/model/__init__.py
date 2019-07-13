from .app_data import ApiCall, HttpExchange


def to_curl(api_call: ApiCall, exchange: HttpExchange, compressed=False, verify=True):
    http_method = api_call.http_method
    http_url = api_call.http_url
    req_headers = {k: v.display_text for k, v in api_call.http_headers.items()}
    req_qp = {k: v.display_text for k, v in api_call.http_params.items()}
    req_body = api_call.http_request_body

    if exchange.response.http_status_code != 0:
        http_method = exchange.request.http_method
        http_url = exchange.request.http_url
        req_qp = exchange.request.query_params
        req_headers = exchange.request.headers
        req_body = exchange.request.request_body

    if req_qp:
        http_url = http_url + "?" + "&".join([f"{k}={v}" for k, v in req_qp.items()])

    parts = [
        ('curl', None),
        ('-X', http_method),
    ]

    for k, v in sorted(req_headers.items()):
        parts += [('-H', '{0}: {1}'.format(k, v))]

    if req_body:
        body = req_body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        parts += [('-d', body)]

    if compressed:
        parts += [('--compressed', None)]

    if not verify:
        parts += [('--insecure', None)]

    parts += [(None, http_url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(k)
        if v:
            flat_parts.append("'{0}'".format(v))

    return ' '.join(flat_parts)

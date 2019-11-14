# Status code to Enum + message mapping
from enum import Enum, auto


class Languages(Enum):
    JAVA = auto()


_mappings = {
    Languages.JAVA: {
        100: ("HttpStatus.CONTINUE", "Continue"),
        101: ("HttpStatus.SWITCHING_PROTOCOLS", "Switching Protocols"),
        102: ("HttpStatus.PROCESSING", "Processing"),
        103: ("HttpStatus.CHECKPOINT", "Checkpoint"),
        200: ("HttpStatus.OK", "OK"),
        201: ("HttpStatus.CREATED", "Created"),
        202: ("HttpStatus.ACCEPTED", "Accepted"),
        203: ("HttpStatus.NON_AUTHORITATIVE_INFORMATION", "Non"),
        204: ("HttpStatus.NO_CONTENT", "No Content"),
        205: ("HttpStatus.RESET_CONTENT", "Reset Content"),
        206: ("HttpStatus.PARTIAL_CONTENT", "Partial Content"),
        207: ("HttpStatus.MULTI_STATUS", "Multi"),
        208: ("HttpStatus.ALREADY_REPORTED", "Already Reported"),
        226: ("HttpStatus.IM_USED", "IM Used"),
        300: ("HttpStatus.MULTIPLE_CHOICES", "Multiple Choices"),
        301: ("HttpStatus.MOVED_PERMANENTLY", "Moved Permanently"),
        302: ("HttpStatus.MOVED_TEMPORARILY", "Moved Temporarily"),
        303: ("HttpStatus.SEE_OTHER", "See Other"),
        304: ("HttpStatus.NOT_MODIFIED", "Not Modified"),
        305: ("HttpStatus.USE_PROXY", "Use Proxy"),
        307: ("HttpStatus.TEMPORARY_REDIRECT", "Temporary Redirect"),
        308: ("HttpStatus.PERMANENT_REDIRECT", "Permanent Redirect"),
        400: ("HttpStatus.BAD_REQUEST", "Bad Request"),
        401: ("HttpStatus.UNAUTHORIZED", "Unauthorized"),
        402: ("HttpStatus.PAYMENT_REQUIRED", "Payment Required"),
        403: ("HttpStatus.FORBIDDEN", "Forbidden"),
        404: ("HttpStatus.NOT_FOUND", "Not Found"),
        405: ("HttpStatus.METHOD_NOT_ALLOWED", "Method Not Allowed"),
        406: ("HttpStatus.NOT_ACCEPTABLE", "Not Acceptable"),
        407: (
            "HttpStatus.PROXY_AUTHENTICATION_REQUIRED",
            "Proxy Authentication Required",
        ),
        408: ("HttpStatus.REQUEST_TIMEOUT", "Request Timeout"),
        409: ("HttpStatus.CONFLICT", "Conflict"),
        410: ("HttpStatus.GONE", "Gone"),
        411: ("HttpStatus.LENGTH_REQUIRED", "Length Required"),
        412: ("HttpStatus.PRECONDITION_FAILED", "Precondition Failed"),
        413: ("HttpStatus.PAYLOAD_TOO_LARGE", "Payload Too Large"),
        414: ("HttpStatus.URI_TOO_LONG", "URI Too Long"),
        415: ("HttpStatus.UNSUPPORTED_MEDIA_TYPE", "Unsupported Media Type"),
        416: (
            "HttpStatus.REQUESTED_RANGE_NOT_SATISFIABLE",
            "Requested range not satisfiable",
        ),
        417: ("HttpStatus.EXPECTATION_FAILED", "Expectation Failed"),
        418: ("HttpStatus.I_AM_A_TEAPOT", "I"),
        419: (
            "HttpStatus.INSUFFICIENT_SPACE_ON_RESOURCE",
            "Insufficient Space On Resource",
        ),
        420: ("HttpStatus.METHOD_FAILURE", "Method Failure"),
        421: ("HttpStatus.DESTINATION_LOCKED", "Destination Locked"),
        422: ("HttpStatus.UNPROCESSABLE_ENTITY", "Unprocessable Entity"),
        423: ("HttpStatus.LOCKED", "Locked"),
        424: ("HttpStatus.FAILED_DEPENDENCY", "Failed Dependency"),
        425: ("HttpStatus.TOO_EARLY", "Too Early"),
        426: ("HttpStatus.UPGRADE_REQUIRED", "Upgrade Required"),
        428: ("HttpStatus.PRECONDITION_REQUIRED", "Precondition Required"),
        429: ("HttpStatus.TOO_MANY_REQUESTS", "Too Many Requests"),
        431: (
            "HttpStatus.REQUEST_HEADER_FIELDS_TOO_LARGE",
            "Request Header Fields Too Large",
        ),
        451: (
            "HttpStatus.UNAVAILABLE_FOR_LEGAL_REASONS",
            "Unavailable For Legal Reasons",
        ),
        500: ("HttpStatus.INTERNAL_SERVER_ERROR", "Internal Server Error"),
        501: ("HttpStatus.NOT_IMPLEMENTED", "Not Implemented"),
        502: ("HttpStatus.BAD_GATEWAY", "Bad Gateway"),
        503: ("HttpStatus.SERVICE_UNAVAILABLE", "Service Unavailable"),
        504: ("HttpStatus.GATEWAY_TIMEOUT", "Gateway Timeout"),
        505: ("HttpStatus.HTTP_VERSION_NOT_SUPPORTED", "HTTP Version not supported"),
        506: ("HttpStatus.VARIANT_ALSO_NEGOTIATES", "Variant Also Negotiates"),
        507: ("HttpStatus.INSUFFICIENT_STORAGE", "Insufficient Storage"),
        508: ("HttpStatus.LOOP_DETECTED", "Loop Detected"),
        509: ("HttpStatus.BANDWIDTH_LIMIT_EXCEEDED", "Bandwidth Limit Exceeded"),
        510: ("HttpStatus.NOT_EXTENDED", "Not Extended"),
    }
}


def to_http_status(http_status_code, lang):
    return _mappings.get(lang).get(http_status_code)


if __name__ == "__main__":
    print(to_http_status(409, Languages.JAVA))
    print(to_http_status(400, Languages.JAVA))

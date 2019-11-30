import json
from unittest.mock import Mock

from httprider.core import DynamicStringData
from httprider.core.constants import PROJECT_INFO_RECORD_TYPE, ContentType
from httprider.core.core_settings import CoreSettings
from httprider.core.faker_config import g
from httprider.model.app_data import (
    ApiCall,
    HttpExchange,
    ExchangeRequest,
    ExchangeResponse,
    ProjectInfo,
)


def mock_dynamic_string_dict():
    return {
        "a": DynamicStringData(display_text="${custom()}", value="${custom()}"),
        "b": DynamicStringData(display_text="555", value="555"),
    }


def mock_flat_dict():
    return {"a": "some-value-a", "b": "some-value-b"}


def mock_raw_json():
    j = {
        "a": "value_a",
        "b_int": 30,
        "c": "value_c",
        "d_float": 5.4,
        "e_bool": False,
        "f_nested": {"aa_str": "aa_value_str"},
    }
    return json.dumps(j)


def mock_api_call():
    return ApiCall(
        id=g.pystr(),
        description="Httpbin call to get request data - df92df60-c1b1-46fe-b83d-220e22ba152a",
        title="Get httpbin",
        http_url="${API_URL}/get",
        http_method="GET",
        http_headers=mock_dynamic_string_dict(),
        http_params=mock_dynamic_string_dict(),
        form_params=mock_dynamic_string_dict(),
        http_request_body=mock_raw_json(),
        sequence_number=1000,
        type="api",
        tags=["Registration"],
        last_response_code=200,
        enabled=True,
    )


def mock_db_table():
    return {PROJECT_INFO_RECORD_TYPE: {}}


def mock_app_data_writer():
    app_data_writer = Mock()
    return app_data_writer


def mock_app_data_cache():
    app_data_cache = Mock()
    app_data_cache.get_last_exchange.return_value = mock_exchange()
    return app_data_cache


def mock_project_info():
    return ProjectInfo(
        record_type=PROJECT_INFO_RECORD_TYPE,
        info=g.pystr(),
        title=g.pystr(),
        version="1.0.0",
    )


def mock_app_data_reader():
    app_data_reader = Mock()
    app_data_reader.get_or_create_project_info.return_value = mock_project_info()
    return app_data_reader


def mock_core_settings():
    cs = CoreSettings()
    cs.app_data_reader = mock_app_data_reader()
    cs.app_data_writer = mock_app_data_writer()
    cs.app_data_cache = mock_app_data_cache()
    return cs


def mock_exchange():
    return HttpExchange(
        api_call_id="2",
        id="5",
        request=ExchangeRequest(
            request_time="Thu Jun 20 09:04:55 2019",
            http_method="GET",
            http_url="http://127.0.0.1:8000/get",
            headers={"Content-Type": ContentType.JSON.value},
            query_params=mock_flat_dict(),
            form_params=mock_flat_dict(),
            request_body=mock_raw_json(),
        ),
        type="http_exchange",
        response=ExchangeResponse(
            http_status_code=200,
            response_headers={
                "server": "gunicorn/19.9.0",
                "date": "Thu, 20 Jun 2019 08:04:55 GMT",
                "connection": "close",
                "content-type": "application/json",
                "content-length": "273",
                "access-control-allow-origin": "*",
                "access-control-allow-credentials": "true",
            },
            response_body='{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate", \n    "Connection": "keep-alive", \n    "Host": "127.0.0.1:8000", \n    "User-Agent": "python-requests/2.21.0"\n  }, \n  "origin": "127.0.0.1", \n  "url": "http://127.0.0.1:8000/get"\n}\n',
            response_time=236.530_999_999_999_98,
        ),
        assertions=[],
    )

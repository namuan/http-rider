import yaml

from httprider.exporters.exporter_openapi_v3 import OpenApiv3Exporter
from httprider.tests.presenters.object_builder import *


def test_export_single_open_api_v3_document():
    # given
    api_call = mock_api_call()
    api_calls = [api_call]
    mock_app_settings = mock_core_settings()

    # when
    exporter = OpenApiv3Exporter(mock_app_settings)
    exported_yaml = exporter.export_data(api_calls, return_raw=True)

    # then
    openapi = yaml.safe_load(exported_yaml)
    assert openapi.get("openapi") == "3.0.2"
    assert openapi.get("info").get("description") is not ""
    assert openapi.get("info").get("title") is not ""
    assert openapi.get("info").get("version") == "1.0.0"

    openapi_path = openapi.get("paths").get("${API_URL}/get", None)
    assert openapi_path is not None
    assert openapi_path.get("get").get("summary") == "Get httpbin"
    assert "Registration" in openapi_path.get("get").get("tags")

    # including header and query parameters in exchange
    assert len(openapi_path.get("get").get("parameters")) == 3

    # assert query param example from exchange
    qp_a = next(
        (
            p
            for p in openapi_path.get("get").get("parameters")
            if p.get("in") == "query" and p.get("name") == "a"
        ),
        None,
    )
    assert qp_a is not None
    assert qp_a.get("schema").get("example") == "some-value-a"

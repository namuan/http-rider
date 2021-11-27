from . import exporter_apickli
from . import exporter_curl
from . import exporter_markdown
from . import exporter_mermaid
from . import exporter_openapi_v3
from . import exporter_runscope
from . import exporter_restassured
from . import exporter_python_requests
from . import exporter_plantuml
from . import exporter_slow_cooker
from . import exporter_confluence
from . import exporter_locust_tests
from . import exporter_spring_contract_tests

exporter_plugins = {
    "locust": exporter_locust_tests,
    "confluence": exporter_confluence,
    "runscope": exporter_runscope,
    "apickli": exporter_apickli,
    "slow_cooker": exporter_slow_cooker,
    "plant_uml": exporter_plantuml,
    "python_requests": exporter_python_requests,
    "curl": exporter_curl,
    "markdown": exporter_markdown,
    "mermaid": exporter_mermaid,
    "openapi_v3": exporter_openapi_v3,
    "restassured": exporter_restassured,
    "spring_contract_tests": exporter_spring_contract_tests,
}

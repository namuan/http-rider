from . import importer_curl
from . import importer_openapi_v3
from . import importer_postman_collections

importer_plugins = [
    importer_curl,
    importer_openapi_v3,
    importer_postman_collections
]

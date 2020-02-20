import shutil
import tempfile

import requests


def getlink():
    try:
        response = requests.post(
            url="http://api.openapi-generator.tech/api/gen/clients/java",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "openAPIUrl":
                    "https://raw.githubusercontent.com/OpenAPITools/openapi-generator/master/modules/openapi-generator/src/test/resources/2_0/petstore.yaml"
            })
        print(f'Response HTTP Status Code: {response.status_code}')
        return response.json().get("link")
    except requests.exceptions.RequestException as e:
        print(f'HTTP Request failed {e}')


def openapi_sdk_downloads(download_url):
    _, fn = tempfile.mkstemp(suffix=".zip")
    with requests.get(download_url, stream=True) as r:
        with open(fn, 'wb+') as f:
            shutil.copyfileobj(r.raw, f)

    return fn


if __name__ == '__main__':
    download_link = getlink()
    temp_file = openapi_sdk_downloads(download_link)

    print("File saved in {}".format(temp_file))

from urllib import parse

import attr
import uncurl
from uncurl.api import ParsedContext

from ..core import DynamicStringData, split_url_qs
from ..core.core_settings import app_settings
from ..model.app_data import ApiCall


@attr.s
class CurlImporter:
    name: str = "Curl"
    input_type: str = "text"

    def import_data(self, curl_command):
        try:
            ctx: ParsedContext = uncurl.parse_context(curl_command)
            api_call = self.__extract_api_call(ctx)
            return None, [
                api_call
            ]
        except BaseException:
            raise SyntaxError("Unable to parse curl command")

    def __extract_api_call(self, ctx):
        url, qs = split_url_qs(ctx.url.strip())
        return ApiCall(
            title="Curl command",
            description=f"Imported from {url}",
            http_url=url,
            http_method=ctx.method,
            http_request_body=self.__extract_request_body(ctx),
            form_params=self.__extract_form_data(ctx),
            http_params=qs,
            http_headers=self.__extract_header_data(ctx.headers),
            sequence_number=app_settings.app_data_writer.generate_sequence_number()
        )

    def __extract_header_data(self, headers):
        return {hk: DynamicStringData(display_text=hv) for hk, hv in headers.items()}

    def __extract_form_data(self, ctx: ParsedContext):
        form_content_type = ctx.headers.get('Content-Type', None) == 'application/x-www-form-urlencoded'
        if form_content_type:
            return {fk: DynamicStringData(display_text=",".join(fv)) for fk, fv in parse.parse_qs(ctx.data).items()}
        else:
            return {}

    def __extract_request_body(self, ctx: ParsedContext):
        form_content_type = ctx.headers.get('Content-Type', None) == 'application/x-www-form-urlencoded'
        if not form_content_type:
            return ctx.data or ""
        else:
            return ""


importer = CurlImporter()

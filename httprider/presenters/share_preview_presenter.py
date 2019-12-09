from httprider.model.app_data import HttpExchange, ApiCall
from httprider.presenters.common import md_request_response_generator
from httprider.core.core_settings import app_settings
from mistune import markdown


class SharePreviewPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent

        # ui events
        self.view.btn_show_preview.clicked.connect(self.render_preview)

    def render_preview(self):
        raw_md = self.view.txt_preview_share.toPlainText()
        html_md = markdown(raw_md)
        self.view.txt_preview_share.setHtml(html_md)

    def prepend_api_call(self, api_call: ApiCall, raw_md):
        return f"""## {api_call.title}
{api_call.description}
        
{raw_md}
        """

    def show_dialog(self, selected_exchange: HttpExchange):
        api_call = app_settings.app_data_cache.get_api_call(
            selected_exchange.api_call_id
        )
        raw_md = md_request_response_generator(selected_exchange)
        combined_md = self.prepend_api_call(api_call, raw_md)
        self.view.txt_preview_share.setPlainText(combined_md)
        self.view.show()

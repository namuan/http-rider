import mistune

from httprider.core.core_settings import app_settings
from httprider.core.markdown_renderer import HighlightRenderer
from httprider.core.pygment_styles import pyg_styles
from httprider.model.app_data import HttpExchange, ApiCall
from httprider.presenters.common import md_request_response_generator

renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)


class SharePreviewPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent
        self.selected_exchange = None
        self.edit_view = True
        self.md_content = ""

        self.view.txt_preview_share.document().setDefaultStyleSheet(pyg_styles())

        # ui events
        self.view.btn_show_preview.clicked.connect(self.render_preview)

    def render_preview(self):
        if self.edit_view:
            raw_md = self.view.txt_preview_share.toPlainText()
            self.md_content = raw_md
            self.render_html_markdown()
        else:
            self.render_raw_markdown()

        self.edit_view = not self.edit_view

    def prepend_api_call(self, api_call: ApiCall, raw_md):
        return f"""## {api_call.title}
{api_call.description}
        
{raw_md}
        """

    def refresh(self):
        api_call = app_settings.app_data_cache.get_api_call(
            self.selected_exchange.api_call_id
        )
        raw_md = md_request_response_generator(
            self.selected_exchange, include_sep=False
        )
        combined_md = self.prepend_api_call(api_call, raw_md)
        self.md_content = combined_md
        self.render_raw_markdown()

    def show_dialog(self, selected_exchange: HttpExchange):
        self.selected_exchange = selected_exchange
        self.refresh()
        self.view.show()

    def render_html_markdown(self):
        html_md = markdown(self.md_content)
        self.view.txt_preview_share.setHtml(html_md)
        self.view.btn_show_preview.setText("Edit")
        self.view.txt_preview_share.setReadOnly(True)

    def render_raw_markdown(self):
        self.view.txt_preview_share.setPlainText(self.md_content)
        self.view.btn_show_preview.setText("Preview")
        self.view.txt_preview_share.setReadOnly(False)

import mistune

from httprider.core.core_settings import app_settings
from httprider.core.markdown_renderer import HighlightRenderer
from httprider.core.pygment_styles import pyg_styles
from httprider.interactors.share_service_interactor import ShareServiceInteractor
from httprider.model.app_data import HttpExchange, ApiCall, ProjectInfo
from httprider.presenters.common import md_request_response_generator

renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)


class SharePreviewPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent
        self.selected_exchanges = None
        self.edit_view = True
        self.md_content = ""
        self.share_service_interactor = ShareServiceInteractor(self.view)

        self.view.txt_preview_share.document().setDefaultStyleSheet(pyg_styles())

        # ui events
        self.view.btn_show_preview.clicked.connect(self.render_preview)
        self.view.btn_share_exchange.clicked.connect(self.share_exchange)

        # domain events
        app_settings.app_data_writer.signals.exchange_share_created.connect(
            self.on_share_created
        )
        app_settings.app_data_writer.signals.exchange_share_failed.connect(
            self.on_share_failed
        )

    def on_share_failed(self, error_message):
        self.view.lbl_share_location.setText(error_message)
        self.on_share_exchange_saved()

    def on_share_created(self, share_location_url):
        share_location_href = 'Shared document: <a href="{0}">{0}</a>'.format(
            share_location_url
        )
        self.view.lbl_share_location.setText(share_location_href)
        self.on_share_exchange_saved()

    def share_exchange(self):
        self.view.btn_share_exchange.setEnabled(False)
        self.view.lbl_share_location.setText("Creating document ...")
        if self.edit_view:
            self.update_cached_markdown()

        markdown_html = markdown(self.md_content)
        self.share_service_interactor.create_document(markdown_html)

    def on_share_exchange_saved(self):
        self.view.btn_share_exchange.setEnabled(True)

    def update_cached_markdown(self):
        self.md_content = self.view.txt_preview_share.toPlainText()

    def render_preview(self):
        self.edit_view = not self.edit_view

        if not self.edit_view:
            self.update_cached_markdown()
            self.render_html_markdown()
        else:
            self.render_raw_markdown()

    def prepend_api_call(self, api_call: ApiCall, raw_md):
        return f"""### {api_call.title}
{api_call.description}
        
{raw_md}"""

    def refresh(self):
        self.view.lbl_share_location.setText("")
        project: ProjectInfo = app_settings.app_data_reader.get_or_create_project_info()
        md_project_info = self.md_for_project_info(project)

        md_content_for_exchanges = [
            self.md_for_exchange(exchange) for exchange in self.selected_exchanges
        ]

        self.md_content = (
            md_project_info + "\r\n" + "\r\n".join(md_content_for_exchanges)
        )

        self.render_raw_markdown()

    def md_for_project_info(self, project: ProjectInfo):
        return f"""
## {project.title}

{project.info}
        """

    def md_for_exchange(self, http_exchange: HttpExchange):
        api_call = app_settings.app_data_cache.get_api_call(http_exchange.api_call_id)
        raw_md = md_request_response_generator(http_exchange, include_sep=False)
        return self.prepend_api_call(api_call, raw_md)

    def show_dialog(self, selected_exchange: HttpExchange):
        self.selected_exchanges = [selected_exchange]
        self.refresh()
        self.view.show()

    def show_dialog_multiple_apis(self):
        api_calls = app_settings.app_data_cache.get_all_active_api_calls()
        self.selected_exchanges = app_settings.app_data_cache.get_multiple_api_latest_exchanges(
            api_calls
        )
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

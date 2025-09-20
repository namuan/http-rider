from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu


def menu_items(self):
    # File Menu
    new_action = QAction("&New", self)
    new_action.setShortcut("Ctrl+N")
    new_action.triggered.connect(self.file_menu_presenter.on_file_new)

    open_action = QAction("&Open ...", self)
    open_action.setShortcut("Ctrl+O")
    open_action.triggered.connect(self.file_menu_presenter.on_file_open)

    save_action = QAction("&Save", self)
    save_action.setShortcut("Ctrl+S")
    save_action.triggered.connect(self.file_menu_presenter.on_file_save)

    save_as_action = QAction("Save &As...", self)
    save_as_action.triggered.connect(self.file_menu_presenter.on_file_save_as)

    # save_env_and_apis_action = QAction("Save &Environments And APIs...", self)
    # save_env_and_apis_action.triggered.connect(
    #     self.file_menu_presenter.on_file_save_env_and_apis
    # )

    f: QMenu = self.menu_bar.addMenu("&File")
    f.addAction(new_action)
    f.addAction(open_action)
    f.addSeparator()
    f.addAction(save_action)
    f.addAction(save_as_action)
    # f.addAction(save_env_and_apis_action)

    single_request = QAction("&Send", self)
    single_request.setShortcut("Ctrl+Return")
    single_request.triggered.connect(self.request_presenter.on_btn_send_request)

    multiple_request = QAction("&Send All", self)
    multiple_request.setShortcut("Ctrl+Shift+Return")
    multiple_request.triggered.connect(self.api_list_presenter.run_all_api_calls)

    single_export = QAction("&Export", self)
    single_export.setShortcut("Ctrl+E")
    single_export.triggered.connect(self.code_generator_dialog.export_single_dialog)

    multiple_export = QAction("&Export All", self)
    multiple_export.setShortcut("Ctrl+Shift+E")
    multiple_export.triggered.connect(self.code_generator_dialog.export_all_dialog)

    generate_data = QAction("&Insert Variables", self)
    generate_data.setShortcut("Ctrl+I")
    generate_data.triggered.connect(self.request_presenter.on_show_data_generator_dialog)

    r: QMenu = self.menu_bar.addMenu("&Requests")
    r.addAction(single_request)
    r.addAction(multiple_request)
    r.addSeparator()
    r.addAction(single_export)
    r.addAction(multiple_export)
    r.addSeparator()
    r.addAction(generate_data)

    # Environments Menu
    export_env_action = QAction("&Export", self)
    export_env_action.triggered.connect(self.env_menu_presenter.on_export)

    import_env_action = QAction("&Import", self)
    import_env_action.triggered.connect(self.env_menu_presenter.on_import)

    r: QMenu = self.menu_bar.addMenu("&Environments")
    r.addAction(export_env_action)
    r.addAction(import_env_action)

    # Generators Menu
    # openapi_sdk_gen_action = QAction("&OpenAPI SDK", self)
    # openapi_sdk_gen_action.triggered.connect(self.generator_menu_presenter.on_openapi_sdk_generator)
    #
    # r: QMenu = self.menu_bar.addMenu("&Generators")
    # r.addAction(openapi_sdk_gen_action)

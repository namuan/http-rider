# HTTP-Rider Feature → Code Quick Reference

Complete 1:1 mapping of every feature to implementation files.

---

## 1. REQUEST MANAGEMENT

| Feature                    | Presenter             | Interactor             | Model                     | Dialog         | View                     |
| -------------------------- | --------------------- | ---------------------- | ------------------------- | -------------- | ------------------------ |
| **Create Request**         | request_presenter.py  | api_call_interactor.py | ApiCall                   | base_window.py | main_window.py           |
| **Edit Request**           | request_presenter.py  | api_call_interactor.py | ApiCall                   | base_window.py | main_window.py           |
| **Delete Request**         | api_list_presenter.py | api_call_interactor.py | ApiCall                   | -              | api_calls_list_view.py   |
| **Set HTTP Method**        | request_presenter.py  | -                      | ApiCall.http_method       | base_window.py | main_window.py           |
| **Set URL**                | request_presenter.py  | -                      | ApiCall.http_url          | base_window.py | main_window.py           |
| **Manage Headers**         | request_presenter.py  | -                      | ApiCall.http_headers      | base_window.py | key_value_widget.py      |
| **Manage Query Params**    | request_presenter.py  | -                      | ApiCall.http_params       | base_window.py | key_value_widget.py      |
| **Manage Form Data**       | request_presenter.py  | -                      | ApiCall.form_params       | base_window.py | key_value_widget.py      |
| **Request Body**           | request_presenter.py  | -                      | ApiCall.http_request_body | base_window.py | completion_plain_text.py |
| **Request Title**          | request_presenter.py  | -                      | ApiCall.title             | base_window.py | main_window.py           |
| **Request Description**    | request_presenter.py  | -                      | ApiCall.description       | base_window.py | main_window.py           |
| **Add Tag**                | request_presenter.py  | api_call_interactor.py | ApiCall.tags              | base_window.py | new_tag_entry_input.py   |
| **Remove Tag**             | request_presenter.py  | api_call_interactor.py | ApiCall.tags              | base_window.py | tag_label_widget.py      |
| **Enable/Disable Request** | api_list_presenter.py | api_call_interactor.py | ApiCall.enabled           | -              | api_calls_list_view.py   |
| **Duplicate Request**      | api_list_presenter.py | api_call_interactor.py | ApiCall                   | -              | api_calls_list_view.py   |
| **Drag-Drop Reorder**      | api_list_presenter.py | api_call_interactor.py | ApiCall.sequence_number   | -              | api_calls_list_view.py   |

---

## 2. REQUEST EXECUTION / SENDING

| Feature                   | Presenter             | Core                        | External              | Model                             |
| ------------------------- | --------------------- | --------------------------- | --------------------- | --------------------------------- |
| **Send Single Request**   | request_presenter.py  | safe_rest_api_interactor.py | rest_api_connector.py | HttpExchange                      |
| **Send All Requests**     | api_list_presenter.py | safe_rest_api_interactor.py | rest_api_connector.py | HttpExchange                      |
| **Variable Substitution** | request_presenter.py  | **init**.py (core)          | -                     | DynamicStringData                 |
| **Dynamic Variables**     | request_presenter.py  | -                           | -                     | DynamicStringData                 |
| **Serialize Request**     | request_presenter.py  | -                           | requester.py          | ExchangeRequest                   |
| **URL Parsing**           | request_presenter.py  | -                           | -                     | ExchangeRequest                   |
| **Headers Combination**   | request_presenter.py  | -                           | -                     | ExchangeRequest                   |
| **Async Execution**       | api_list_presenter.py | safe_rest_api_interactor.py | rest_api_connector.py | HttpExchange                      |
| **Request Timing**        | exchange_presenter.py | -                           | rest_api_connector.py | ExchangeRequest.request_time      |
| **Timeout Config**        | config_presenter.py   | -                           | requester.py          | AppConfiguration.timeout_in_secs  |
| **TLS Verification**      | config_presenter.py   | -                           | requester.py          | AppConfiguration.tls_verification |
| **Redirect Following**    | config_presenter.py   | -                           | requester.py          | AppConfiguration.allow_redirects  |
| **Proxy Support**         | config_presenter.py   | -                           | requester.py          | AppConfiguration.http_proxy       |

---

## 3. RESPONSE VIEWING

| Feature                    | Presenter             | Core                 | Model                               | View                     |
| -------------------------- | --------------------- | -------------------- | ----------------------------------- | ------------------------ |
| **Display Status Code**    | exchange_presenter.py | pygment_styles.py    | ExchangeResponse.http_status_code   | base_window.py           |
| **Display Headers Table**  | exchange_presenter.py | -                    | ExchangeResponse.response_headers   | base_window.py           |
| **Display Body**           | exchange_presenter.py | pygment_styles.py    | ExchangeResponse.response_body      | base_window.py           |
| **Syntax Highlighting**    | exchange_presenter.py | pygment_styles.py    | -                                   | completion_plain_text.py |
| **Pretty-Print JSON**      | exchange_presenter.py | pygments (external)  | -                                   | completion_plain_text.py |
| **Format XML**             | exchange_presenter.py | pygments (external)  | -                                   | completion_plain_text.py |
| **Display Response Time**  | exchange_presenter.py | -                    | ExchangeResponse.response_time      | base_window.py           |
| **Content-Type Detection** | exchange_presenter.py | -                    | ExchangeResponse.response_body_type | -                        |
| **Raw Response Display**   | exchange_presenter.py | markdown_renderer.py | ExchangeResponse                    | base_window.py           |
| **Raw Request Display**    | exchange_presenter.py | markdown_renderer.py | ExchangeRequest                     | base_window.py           |

---

## 4. REQUEST HISTORY / EXCHANGES

| Feature                 | Presenter                      | Model                             | View                   |
| ----------------------- | ------------------------------ | --------------------------------- | ---------------------- |
| **Last 10 Exchanges**   | api_calls_history_presenter.py | app_data_cache.py                 | base_window.py         |
| **Exchange Buttons**    | api_calls_history_presenter.py | HttpExchange                      | base_window.py         |
| **Status Color Coding** | api_calls_history_presenter.py | ExchangeResponse.http_status_code | api_calls_list_view.py |
| **Exchange Switching**  | api_calls_history_presenter.py | app_data_cache.py                 | base_window.py         |
| **Exchange Selection**  | api_calls_history_presenter.py | app_state_interactor.py           | base_window.py         |
| **Select Exchange**     | exchange_presenter.py          | app_data_cache.py                 | -                      |

---

## 5. ASSERTIONS / VALIDATIONS

| Feature                  | Presenter                       | Logic                          | Model                         | Dialog                      |
| ------------------------ | ------------------------------- | ------------------------------ | ----------------------------- | --------------------------- |
| **Build Assertions**     | assertion_builder_presenter.py  | assertion_list_presenter.py    | Assertion                     | assertion_builder_dialog.py |
| **Response Code Assert** | assertion_list_presenter.py     | -                              | Assertion                     | assertion_builder_dialog.py |
| **Response Time Assert** | assertion_list_presenter.py     | -                              | Assertion                     | assertion_builder_dialog.py |
| **Header Assertions**    | headers_assertions_presenter.py | assertion_builder_presenter.py | Assertion                     | assertion_builder_dialog.py |
| **Body Assertions**      | body_assertion_presenter.py     | assertion_builder_presenter.py | Assertion                     | assertion_builder_dialog.py |
| **Value Extraction**     | assertion_list_presenter.py     | -                              | Assertion (matcher='extract') | assertion_builder_dialog.py |
| **Assertion Matchers**   | assertion_list_presenter.py     | assertion_result_presenter.py  | AssertionMatchers (const)     | assertion_builder_dialog.py |
| **Evaluate Assertions**  | assertion_result_presenter.py   | assertion_result_presenter.py  | ApiTestCase                   | -                           |
| **Show Pass/Fail**       | api_list_presenter.py           | assertion_result_presenter.py  | ApiCall.last_assertion_result | api_calls_list_view.py      |
| **Assertion Results**    | assertion_result_presenter.py   | assertion_result_presenter.py  | HttpExchange.assertions       | base_window.py              |

---

## 6. ENVIRONMENTS & VARIABLES

| Feature                      | Presenter                              | Interactor                | Model                             | Dialog                              |
| ---------------------------- | -------------------------------------- | ------------------------- | --------------------------------- | ----------------------------------- |
| **Create Environment**       | environment_configuration_presenter.py | environment_interactor.py | Environment                       | environment_configuration_dialog.py |
| **Select Environment**       | envs_list_presenter.py                 | app_state_interactor.py   | Environment.name                  | main_window.py (toolbar)            |
| **Add Variables**            | environment_configuration_presenter.py | -                         | DynamicStringData                 | environment_configuration_dialog.py |
| **Edit Variables**           | environment_configuration_presenter.py | -                         | DynamicStringData                 | environment_configuration_dialog.py |
| **Enable/Disable Variables** | environment_configuration_presenter.py | -                         | DynamicStringData.is_enabled      | environment_configuration_dialog.py |
| **Secret Values**            | environment_configuration_presenter.py | -                         | DynamicStringData.display_value() | environment_configuration_dialog.py |
| **Variable Substitution**    | request_presenter.py                   | core/**init**.py          | DynamicStringData                 | -                                   |
| **Variable Completion**      | completer.py                           | -                         | get_completer_model()             | completion_line_edit.py             |
| **Duplicate Environment**    | environment_configuration_presenter.py | environment_interactor.py | Environment                       | environment_configuration_dialog.py |
| **Delete Environment**       | environment_configuration_presenter.py | environment_interactor.py | Environment                       | environment_configuration_dialog.py |
| **Import Environments**      | environment_configuration_presenter.py | -                         | Environment                       | -                                   |
| **Export Environments**      | environment_configuration_presenter.py | -                         | Environment                       | -                                   |

---

## 7. DATA GENERATION / FAKER

| Feature              | Presenter                   | Logic           | Model             |
| -------------------- | --------------------------- | --------------- | ----------------- |
| **Random String**    | data_generator_presenter.py | generators.py   | -                 |
| **UUID Generation**  | data_generator_presenter.py | generators.py   | -                 |
| **Custom Templates** | data_generator_presenter.py | generators.py   | -                 |
| **Person Data**      | data_generator_presenter.py | faker_config.py | CustomFaker       |
| **Address Data**     | data_generator_presenter.py | faker_config.py | CustomFaker       |
| **Live Preview**     | data_generator_presenter.py | generators.py   | -                 |
| **Insert Variables** | request_presenter.py        | generators.py   | DynamicStringData |

---

## 8. FUZZING / CHAOS TESTING

| Feature                 | Presenter              | Logic                       | Model            | Dialog              |
| ----------------------- | ---------------------- | --------------------------- | ---------------- | ------------------- |
| **Fuzz Test**           | fuzz_test_presenter.py | json_data_generator.py      | HttpExchange     | fuzz_test_dialog.py |
| **Random Payload**      | fuzz_test_presenter.py | json_data_generator.py      | -                | fuzz_test_dialog.py |
| **Schema Generation**   | fuzz_test_presenter.py | json_schema.py              | -                | -                   |
| **Batch Fuzzing**       | fuzz_test_presenter.py | safe_rest_api_interactor.py | HttpExchange     | fuzz_test_dialog.py |
| **Configurable Limits** | fuzz_test_presenter.py | json_data_generator.py      | -                | fuzz_test_dialog.py |
| **Status Aggregation**  | fuzz_test_presenter.py | http_statuses.py            | ExchangeResponse | fuzz_test_dialog.py |
| **Fuzz Results**        | fuzz_test_presenter.py | markdown_renderer.py        | HttpExchange     | fuzz_test_dialog.py |

---

## 9. CODE GENERATION / EXPORT (16+ Formats)

| Feature               | Presenter                   | Exporter Module                   | Format Name     |
| --------------------- | --------------------------- | --------------------------------- | --------------- |
| **cURL Export**       | code_generator_presenter.py | exporter_curl.py                  | curl            |
| **Python Requests**   | code_generator_presenter.py | exporter_python_requests.py       | python_requests |
| **Java Feign**        | code_generator_presenter.py | exporter_java_feign_client.py     | java_feign      |
| **Spring Boot**       | code_generator_presenter.py | exporter_spring_boot_api_java.py  | spring_boot     |
| **Spring Contract**   | code_generator_presenter.py | exporter_spring_contract_tests.py | spring_contract |
| **RestAssured**       | code_generator_presenter.py | exporter_restassured.py           | restassured     |
| **Locust**            | code_generator_presenter.py | exporter_locust_tests.py          | locust          |
| **ApickLi**           | code_generator_presenter.py | exporter_apickli.py               | apickli         |
| **Runscope**          | code_generator_presenter.py | exporter_runscope.py              | runscope        |
| **Slow Cooker**       | code_generator_presenter.py | exporter_slow_cooker.py           | slow_cooker     |
| **Markdown**          | code_generator_presenter.py | exporter_markdown.py              | markdown        |
| **Mermaid**           | code_generator_presenter.py | exporter_mermaid.py               | mermaid         |
| **PlantUML**          | code_generator_presenter.py | exporter_plantuml.py              | plantuml        |
| **Confluence**        | code_generator_presenter.py | exporter_confluence.py            | confluence      |
| **OpenAPI 3.0**       | code_generator_presenter.py | exporter_openapi_v3.py            | openapi_v3      |
| **Postman**           | code_generator_presenter.py | exporter_postman_collections.py   | postman         |
| **Copy to Clipboard** | code_generator_presenter.py | -                                 | -               |
| **Export to File**    | code_generator_presenter.py | -                                 | -               |

---

## 10. IMPORT

| Feature            | Presenter             | Importer Module                 | Input Type |
| ------------------ | --------------------- | ------------------------------- | ---------- |
| **Import cURL**    | importer_presenter.py | importer_curl.py                | text       |
| **Import OpenAPI** | importer_presenter.py | importer_openapi_v3.py          | file       |
| **Import Postman** | importer_presenter.py | importer_postman_collections.py | file       |

---

## 11. PROJECTS

| Feature              | Presenter                 | Logic | Model                      | Dialog                 |
| -------------------- | ------------------------- | ----- | -------------------------- | ---------------------- |
| **New Project**      | file_menu_presenter.py    | -     | -                          | -                      |
| **Open Project**     | file_menu_presenter.py    | -     | -                          | -                      |
| **Save Project**     | file_menu_presenter.py    | -     | -                          | -                      |
| **Project Title**    | project_info_presenter.py | -     | ProjectInfo.title          | project_info_dialog.py |
| **Project Version**  | project_info_presenter.py | -     | ProjectInfo.version        | project_info_dialog.py |
| **Project Info**     | project_info_presenter.py | -     | ProjectInfo.info           | project_info_dialog.py |
| **Contact Info**     | project_info_presenter.py | -     | ProjectInfo (contact\_\*)  | project_info_dialog.py |
| **License**          | project_info_presenter.py | -     | ProjectInfo (license\_\*)  | project_info_dialog.py |
| **Terms of Service** | project_info_presenter.py | -     | ProjectInfo.tos_url        | project_info_dialog.py |
| **Server URLs**      | project_info_presenter.py | -     | ProjectInfo.servers        | project_info_dialog.py |
| **Common Headers**   | project_info_presenter.py | -     | ProjectInfo.common_headers | project_info_dialog.py |
| **Tags**             | project_info_presenter.py | -     | ProjectInfo.tags           | project_info_dialog.py |

---

## 12. ORGANIZATION - TAGS & FILTERING

| Feature            | Presenter                 | Logic                   | Model                 | View                     |
| ------------------ | ------------------------- | ----------------------- | --------------------- | ------------------------ |
| **Tag Selection**  | tags_list_presenter.py    | app_state_interactor.py | ApiCall.tags          | main_window.py (toolbar) |
| **Tag Filtering**  | api_list_presenter.py     | app_data_cache.py       | AppState.selected_tag | api_calls_list_view.py   |
| **Show All**       | tags_list_presenter.py    | app_data_cache.py       | DEFAULT_TAG           | main_window.py           |
| **Tag Display**    | request_presenter.py      | -                       | ApiCall.tags          | tag_label_widget.py      |
| **Auto-Discovery** | project_info_presenter.py | -                       | ProjectInfo.tags      | -                        |
| **Tag Rename**     | api_list_presenter.py     | api_call_interactor.py  | ApiCall.tags          | -                        |

---

## 13. SEARCH & FILTERING

| Feature                 | Component               | Logic                             | Storage               |
| ----------------------- | ----------------------- | --------------------------------- | --------------------- |
| **Filter by Tag**       | tags_list_presenter.py  | app_data_cache.filter_api_calls() | AppState.selected_tag |
| **Selected Tag State**  | app_state_interactor.py | -                                 | AppState record in DB |
| **Request List Filter** | api_list_presenter.py   | app_data_cache.filter_api_calls() | -                     |

---

## 14. CONFIGURATION & SETTINGS

| Feature              | Presenter           | Config Class     | Storage      |
| -------------------- | ------------------- | ---------------- | ------------ |
| **Update Check**     | config_presenter.py | AppConfiguration | app_settings |
| **TLS Verification** | config_presenter.py | AppConfiguration | app_settings |
| **Allow Redirects**  | config_presenter.py | AppConfiguration | app_settings |
| **Timeout**          | config_presenter.py | AppConfiguration | app_settings |
| **HTTP Proxy**       | config_presenter.py | AppConfiguration | app_settings |
| **HTTPS Proxy**      | config_presenter.py | AppConfiguration | app_settings |
| **No Proxy List**    | config_presenter.py | AppConfiguration | app_settings |

---

## 15. THEMES & APPEARANCE

| Feature                 | Module            | Logic                                   |
| ----------------------- | ----------------- | --------------------------------------- |
| **Dark Mode**           | theme_provider.py | is_dark()                               |
| **Light Mode**          | theme_provider.py | is_dark()                               |
| **Syntax Highlighting** | pygment_styles.py | pyg_styles()                            |
| **Status Code Colors**  | theme_provider.py | http_ex_success/client_err/server_err() |
| **List Item Colors**    | theme_provider.py | api_call_list_rect/pen/selected_rect()  |
| **Apply Theme**         | theme_provider.py | configure_theme()                       |

---

## 16. MOCKING

| Feature                   | Presenter                    | Model                      | Dialog         |
| ------------------------- | ---------------------------- | -------------------------- | -------------- |
| **Enable Mock**           | mocked_response_presenter.py | MockedResponse.is_enabled  | base_window.py |
| **Mock Status Code**      | mocked_response_presenter.py | MockedResponse.status_code | base_window.py |
| **Mock Headers**          | mocked_response_presenter.py | MockedResponse.headers     | base_window.py |
| **Mock Body**             | mocked_response_presenter.py | MockedResponse.body        | base_window.py |
| **Variable Support**      | mocked_response_presenter.py | DynamicStringData          | -              |
| **Mocked Response Check** | rest_api_connector.py        | ApiCall.mocked_response    | -              |

---

## 17. SHARING / COLLABORATION

| Feature             | Presenter                  | Service                     | Model          |
| ------------------- | -------------------------- | --------------------------- | -------------- |
| **Share Dialog**    | share_preview_presenter.py | -                           | HttpExchange   |
| **Markdown Export** | share_preview_presenter.py | markdown_renderer.py        | HttpExchange   |
| **HTML Preview**    | share_preview_presenter.py | markdown_renderer.py        | -              |
| **Upload Document** | share_preview_presenter.py | share_service_interactor.py | -              |
| **Share URL**       | share_preview_presenter.py | share_service_interactor.py | -              |
| **Edit & Preview**  | share_preview_presenter.py | -                           | -              |
| **Multiple APIs**   | share_preview_presenter.py | -                           | HttpExchange[] |

---

## PRESENTER INSTANTIATION HIERARCHY

All presenters initialized in **main_window.py** in `__init__()`:

```python
main_presenter = MainPresenter(self)
empty_frame_presenter = EmptyFramePresenter(self)
api_list_presenter = ApiListPresenter(self)
request_presenter = RequestPresenter(self)
exchange_presenter = ExchangePresenter(self)
importer_presenter = ImporterPresenter(self)
tags_list_presenter = TagsListPresenter(self)
envs_list_presenter = EnvironmentsListPresenter(self)
api_calls_history_presenter = ApiCallsHistoryPresenter(self)
file_menu_presenter = FileMenuPresenter(self)
env_menu_presenter = EnvironmentMenuPresenter(self)
generator_menu_presenter = GeneratorsMenuPresenter(self)
```

---

## SIGNAL EMISSION FLOW

All signals in `httprider/model/app_data_writer.py` → `AppDataSignals` class:

| Signal                      | Emitted When             | Triggering Code                                      |
| --------------------------- | ------------------------ | ---------------------------------------------------- |
| `api_call_added`            | Request created          | api_call_interactor.add_api_call()                   |
| `api_call_updated`          | Request edited           | api_call_interactor.update_api_call()                |
| `api_call_removed`          | Request deleted          | api_call_interactor.remove_api_call()                |
| `api_call_tag_added`        | Tag added to request     | api_call_interactor.add_tag_to_api_call()            |
| `api_call_tag_removed`      | Tag removed              | api_call_interactor.remove_tag_from_api_call()       |
| `multiple_api_calls_added`  | Batch import             | api_call_interactor.add_multiple_api_calls()         |
| `exchange_added`            | Response received        | rest_api_connector.py                                |
| `environment_added`         | Env created              | environment_interactor.py                            |
| `environment_removed`       | Env deleted              | environment_interactor.py                            |
| `environment_renamed`       | Env renamed              | environment_interactor.py                            |
| `environment_data_changed`  | Env variables updated    | app_data_writer.update_environment()                 |
| `project_info_updated`      | Project metadata changed | app_data_writer.update_project_info()                |
| `selected_tag_changed`      | Tag filter selected      | app_state_interactor.update_selected_tag()           |
| `selected_exchange_changed` | Exchange switched        | api_calls_history_presenter.handle_exchange_switch() |
| `api_test_case_changed`     | Assertions updated       | app_data_writer.upsert_assertions()                  |
| `exchange_share_created`    | Document shared          | share_service_interactor.py                          |
| `exchange_share_failed`     | Share error              | share_service_interactor.py                          |

---

## HOW TO ADD A NEW FEATURE

1. **Define Data Model** → `app_data.py`

   - Create `@attr.s` dataclass or extend existing

2. **Create Interactor** → `core/*_interactor.py`

   - Implement CRUD methods
   - Emit signals via `app_settings.app_data_writer.signals.*`

3. **Create Presenter** → `presenters/*_presenter.py`

   - Connect UI signals to methods
   - Subscribe to cache signals for reactive updates
   - Implement `form_to_object()` and `object_to_form()`

4. **Create UI** → `generated/*.py` or `ui/dialogs`

   - Use Qt Designer or PyQt code
   - Link to presenter in **init**

5. **Wire in Main Window** → `main_window.py`

   - Instantiate presenter in **init**
   - Connect menu items/toolbar buttons

6. **Persist to DB** → `model/app_data_writer.py`
   - Add read/write methods
   - Emit appropriate signal after write

---

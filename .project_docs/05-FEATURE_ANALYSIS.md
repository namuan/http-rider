# HTTP-Rider Feature Analysis

Complete documentation of all user-facing features with code mapping and architectural details.

---

## 1. CORE API TESTING FEATURES

### 1.1 Request Creation & Management

**Feature:** Create, edit, and organize HTTP requests with full protocol support

#### Sub-Features:

- **HTTP Method Selection** (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, etc.)
- **URL/Endpoint Configuration** with dynamic variables support
- **Headers Management** (request headers with key-value pairs)
- **Query Parameters** (URL query string parameters)
- **Form Parameters** (form-encoded body parameters)
- **Request Body** (raw text, JSON, XML, etc.)
- **Request Description & Titles** (metadata for documentation)
- **Request Tagging** (categorization with tags)
- **Enable/Disable Requests** (toggle requests on/off without deletion)
- **Comment Support in Request Bodies** (strip comments on execution)
- **Mocked Responses** (configure what API returns for testing)

#### Entry Points:

- `httprider/ui/main_window.py` :: `RequestPresenter` class
- `httprider/presenters/request_presenter.py` :: Full request form handling

#### Core Logic:

- `httprider/model/app_data.py` :: `ApiCall` dataclass
  - Fields: `http_url`, `http_method`, `http_headers`, `http_params`, `form_params`, `http_request_body`, `title`, `description`, `tags`, `enabled`, `mocked_response`
- `httprider/core/api_call_interactor.py` :: `ApiCallInteractor`
  - `add_api_call()` - Create new request
  - `update_api_call()` - Update existing request
  - `remove_api_call()` - Delete request

#### UI Components:

- `httprider/generated/base_window.py` :: Main UI form inputs
- `httprider/widgets/` :: Custom text editors, key-value lists
- `httprider/ui/main_window.py` :: `RequestPresenter.__init__()` initializes UI fields

#### Data Persistence:

- `httprider/model/app_data_writer.py` :: `update_api_call_in_db()`
- SQLite storage via dataset ORM

#### Signal Emissions:

- `api_call_added` when new request created
- `api_call_updated` when request edited
- `api_call_removed` when request deleted

---

### 1.2 Request Execution / Sending

**Feature:** Execute HTTP requests and capture real-time responses

#### Sub-Features:

- **Single Request Execution** (Ctrl+Return, "Send" button)
- **Batch Request Execution** ("Send All" button, Ctrl+Shift+Return)
- **Request Serialization** (URL encoding, form encoding, JSON body)
- **Dynamic Variable Substitution** (replace `${variable_name}` with environment values)
- **Header Combination** (merge request + project common headers)
- **Query String Parsing** (extract QS from URL)
- **Async Execution** (QThread-based non-blocking execution)
- **Request Timing** (capture request/response time)
- **Timeout Configuration** (configurable via settings)
- **TLS Verification Control** (skip/enable certificate verification)
- **Redirect Following** (allow/disallow HTTP redirects)
- **Proxy Support** (HTTP/HTTPS proxy configuration)

#### Entry Points:

- `httprider/presenters/request_presenter.py` :: `on_btn_send_request()`
- `httprider/ui/main_window.py` :: Menu items + shortcuts
- `httprider/presenters/api_list_presenter.py` :: `run_all_api_calls()`

#### Core Logic:

- `httprider/external/rest_api_connector.py` :: `RestApiConnector`
  - Executes HTTP requests via `requests` library
  - Runs in QThread for non-blocking UI
  - Captures full request/response including headers, body, timing
- `httprider/core/safe_rest_api_interactor.py` :: `RestApiInteractor`
  - Wrapper with error handling
  - Manages worker pool and queue
- `httprider/external/requester.py` :: `Requester` interface

#### Variable Replacement:

- `httprider/core::get_variable_tokens()` - Extract variable references
- `httprider/core::replace_variables()` - Substitute values
- `httprider/model/completer.py` :: `get_completer_model()` - Variable completion

#### Response Capture:

- `httprider/model/app_data.py` :: `HttpExchange` dataclass
  - Stores request + response + metadata
  - Fields: `api_call_id`, `request`, `response`, `response_status`, `assertions`

#### Signal Emissions:

- `exchange_added` when response received
- `request_started` when request begins
- `request_completed` when done

---

### 1.3 Response Viewing & Analysis

**Feature:** Display and analyze HTTP responses with formatted output

#### Sub-Features:

- **Status Code Display** (HTTP code with color coding: green 2xx, amber 4xx, red 5xx)
- **Response Headers Table** (display all response headers)
- **Response Body Rendering** (raw, JSON-formatted, XML-formatted)
- **Raw Request/Response Display** (markdown-formatted with syntax highlighting)
- **Response Body Syntax Highlighting** (JSON, XML, plain text)
- **Response Time Display** (elapsed time in milliseconds)
- **Content-Type Detection** (auto-detect and format based on content-type)
- **Pretty-Print JSON/XML** (formatted output with indentation)
- **Query Parameters Display** (echo back query params from request)
- **Form Parameters Display** (echo back form params from request)

#### Entry Points:

- `httprider/presenters/exchange_presenter.py` :: Main response presenter
- `httprider/ui/main_window.py` :: Exchange display frame

#### Core Logic:

- `httprider/model/app_data.py`
  - `ExchangeRequest` - captures sent request details
  - `ExchangeResponse` - captures response + metadata
  - `HttpExchange` - complete request-response pair
- `httprider/presenters/exchange_presenter.py` :: `ExchangePresenter`
  - `refresh()` - populate UI with exchange data
  - `display_last_exchange()` - show previous execution
  - `render_raw_exchange()` - markdown rendering

#### Rendering:

- `httprider/exporters/common.py` :: `request_body_highlighted()`, `response_body_highlighted()`
- `httprider/presenters/common.py` :: `markdown_request()`, `markdown_response()`
- `httprider/core/pygment_styles.py` :: Syntax highlighting with Pygments

#### Data Population:

- Trees/tables populated via `populate_tree_with_kv_dict()` helper

#### Signal Subscriptions:

- `exchange_added` triggers refresh
- `api_call_change_selection` triggers last exchange display
- `selected_exchange_changed` updates view

---

### 1.4 Request History

**Feature:** Track and browse previous request executions

#### Sub-Features:

- **Last 10 Exchanges Display** (button bar showing recent executions)
- **Exchange Status Color Coding** (green pass, amber 4xx, red 5xx)
- **Exchange Switching** (click button to view historical response)
- **Exchange Selection Persistence** (remember selected exchange)
- **Per-Request History** (separate history for each API call)

#### Entry Points:

- `httprider/presenters/api_calls_history_presenter.py` :: `ApiCallsHistoryPresenter`
- `httprider/generated/base_window.py` :: `horizontalLayout_6` (exchange button bar)

#### Core Logic:

- `httprider/presenters/api_calls_history_presenter.py`
  - `refresh()` - populate history buttons
  - `on_exchange_added()` - add new history button
  - `handle_exchange_switch()` - switch to different execution
  - `color_from_response()` - determine button color from status code
- `httprider/core/app_data_cache.py`
  - `get_api_call_exchanges()` - retrieve all exchanges for API call
  - `get_last_exchange()` - get most recent
  - `get_http_exchange(exchange_id)` - get specific exchange

#### Data Model:

- Max last 10 exchanges shown (hardcoded in presenter)
- Each exchange is `HttpExchange` object with response metadata

#### Signal Emissions:

- `exchange_added` when new response received
- `selected_exchange_changed` when user switches between exchanges

---

### 1.5 Favorites / Bookmarks / Separators

**Feature:** Organize requests with separators and visual grouping

#### Sub-Features:

- **Request Separators** (visual dividers in request list)
- **Drag-and-Drop Reordering** (rearrange request order)
- **Sequence Numbering** (maintain request order via `sequence_number`)

#### Entry Points:

- `httprider/presenters/api_list_presenter.py` :: Request list management
- `httprider/widgets/api_calls_list_view.py` :: Custom list view with drag-drop

#### Core Logic:

- `httprider/model/app_data.py` :: `ApiCall`
  - Field: `is_separator` - boolean flag
  - Field: `sequence_number` - ordering
- `httprider/presenters/api_list_presenter.py`
  - `on_drop_event()` - handle drag-drop
  - `show_context_menu()` - separator-specific menu options

#### Signal Subscriptions:

- `api_call_added` - refresh list
- `api_call_removed` - update after delete

---

## 2. ADVANCED TESTING FEATURES

### 2.1 Assertions / Validations / Test Cases

**Feature:** Define and validate response expectations automatically

#### Sub-Features:

- **Response Code Assertion** (assert HTTP status code)
- **Response Time Assertion** (assert response time < milliseconds)
- **Response Header Assertions** (assert header value exists/equals/matches)
- **Response Body Assertions** (JSON path assertion on response body)
- **Request Header Capture** (extract values from request headers)
- **Request Body Capture** (extract JSON path values from request)
- **Response Body Capture** (extract JSON path from response for reuse)
- **Assertion Matchers**:
  - `equalTo` - exact match
  - `notEqualTo` - not equal
  - `notNull` - value exists
  - `isEmpty` - empty string/value
  - `isNotEmpty` - non-empty
  - `containsString` - substring contains
  - `notContainsString` - substring not contains
  - `lessThan` - numeric less than
  - `greaterThan` - numeric greater than
  - `matches` - regex match
  - `extract` - extract value (variable capture)
- **Visual Pass/Fail Indicators** (✅ pass, ⛔ fail in list)
- **Assertion Result Display** (show which assertions passed/failed)
- **Multiple Assertions Per Request** (build complex test cases)

#### Entry Points:

- `httprider/generated/assertion_builder_dialog.py` :: UI dialog
- `httprider/presenters/assertion_builder_presenter.py` :: Main presenter
- Request presenter "Assertions" button

#### Core Logic:

- `httprider/model/app_data.py`
  - `Assertion` - individual assertion definition
  - `ApiTestCase` - collection of assertions per API call
  - Fields: `data_from`, `selector`, `matcher`, `expected_value`, `var_name`
- `httprider/presenters/assertion_builder_presenter.py` :: `AssertionBuilderPresenter`
  - Load from request/response preview
  - Click request/response values to build assertions
  - JSONPath builder for response body
- `httprider/presenters/assertion_list_presenter.py` :: `AssertionListPresenter`
  - `add_response_code_assertion()` - HTTP status assertion
  - `add_response_time_assertion()` - timing assertion
  - `get_all_assertions()` - collect defined assertions
- `httprider/presenters/assertion_result_presenter.py` :: `AssertionResultPresenter`
  - `evaluate()` - run all assertions against exchange
  - `__evaluate_assertion()` - check individual assertion
  - `__get_result_for_matcher()` - matcher logic
- `httprider/presenters/headers_assertions_presenter.py` :: Build header assertions
- `httprider/presenters/body_assertion_presenter.py` :: Build body assertions

#### Matchers Implementation:

- `httprider/core/constants.py` :: `AssertionMatchers` enum
- Logic in `assertion_result_presenter.py`:
  - `_handle_basic_matchers()` - equals, not equals, null
  - `_handle_string_matchers()` - contains, regex
  - `_handle_numeric_matchers()` - less than, greater than

#### Data Sources:

- `httprider/core/constants.py` :: `AssertionDataSource` enum
  - REQUEST_HEADER, RESPONSE_HEADER, REQUEST_BODY, RESPONSE_BODY, RESPONSE_CODE, RESPONSE_TIME

#### Persistence:

- Stored via `app_data_writer.upsert_assertions(api_test_case)`
- SQLite storage

#### Signal Subscriptions:

- `exchange_added` triggers auto-evaluation
- `api_call_change_selection` updates assertion builder preview

#### Result Display:

- API list shows green ✅ / red ⛔ indicator next to request
- Assertion results window shows detailed pass/fail

---

### 2.2 Environments & Variables

**Feature:** Manage environment-specific variables and values

#### Sub-Features:

- **Multiple Environments** (dev, staging, production, custom)
- **Environment Variables** (key-value pairs per environment)
- **Variable Substitution** (use `${variable_name}` in requests)
- **Variable Completion** (autocomplete variable references)
- **Environment Selection** (dropdown to select active environment)
- **Enable/Disable Variables** (toggle variables on/off)
- **Secret/Sensitive Values** (hide values in UI but use in requests)
- **Common Headers** (project-wide headers across environments)
- **Variable Extraction** (extract response values into variables)
- **Duplicate Environment** (clone environment configuration)
- **Environment Import/Export** (JSON-based import/export)

#### Entry Points:

- `httprider/ui/environment_configuration_dialog.py` :: Configuration UI
- `httprider/presenters/environment_configuration_presenter.py` :: Main presenter
- Toolbar environment dropdown

#### Core Logic:

- `httprider/model/app_data.py`
  - `Environment` - environment definition with variables
  - `DynamicStringData` - individual variable value
- `httprider/presenters/environment_configuration_presenter.py` :: `EnvironmentConfigurationPresenter`
  - `on_add_new_environment()` - create new env
  - `on_remove_selected_environment()` - delete env
  - `on_duplicate_environment()` - clone
  - `on_current_item_changed()` - switch environments
- `httprider/presenters/envs_list_presenter.py` :: `EnvironmentsListPresenter`
  - Toolbar dropdown for environment selection
- `httprider/core/environment_interactor.py` :: `EnvironmentInteractor`
  - Database CRUD operations
  - `add_environment()`, `remove_environment()`, `update_environment()`
- `httprider/core/app_state_interactor.py` :: `AppStateInteractor`
  - Track currently selected environment

#### Variable Resolution:

- `httprider/core::get_variable_tokens()` - find `${...}` patterns
- `httprider/core::replace_variables()` - substitute values
- `httprider/model/completer.py` :: Build autocomplete model

#### Persistence:

- `app_data_writer.update_environment()` - save to SQLite
- `app_data_reader.get_environments()` - load all environments

#### Signal Subscriptions:

- `environment_added`, `environment_removed`, `environment_renamed` signals
- `environment_data_changed` triggers variable completer refresh

---

### 2.3 Data Generation / Faker / Random Values

**Feature:** Generate realistic test data using Faker and dynamic functions

#### Sub-Features:

- **Random String Generation** (custom length, letters, digits)
- **UUID Generation** (`${uuid()}` function)
- **Custom String Templates** (template-based generation)
- **Person Data**:
  - First name, last name, full name, prefix, suffix
  - Gender-specific variants (male/female)
- **Address Data**:
  - Country, city, street, address, secondary address, zipcode, state
- **Preview Generation** (live preview of generated values)
- **Variable Insertion** (insert generated values into request)
- **Dynamic Function Syntax** (e.g., `${random(10, true, true)}`)

#### Entry Points:

- `httprider/ui/data_generator_dialog.py` :: UI dialog
- `httprider/presenters/data_generator_presenter.py` :: Main presenter
- Menu: Requests → Insert Variables (Ctrl+I)

#### Core Logic:

- `httprider/core/generators.py` :: Generator functions
  - `random_string_generator()` - custom random strings
  - `random_uuid()` - UUID v4
  - `custom_string_generator()` - template-based
  - `random_person()` - person data (first_name, last_name, full_name, prefix, suffix by gender)
  - `random_address()` - address data
- `httprider/core/faker_config.py` :: `CustomFaker`
  - Faker library configuration with providers
  - English (US) locale
  - Providers: Address, Company, DateTime, Internet, Lorem, Misc, Person, Python
- `httprider/presenters/data_generator_presenter.py`
  - Live preview on tab changes
  - `_get_misc_function()` - random/UUID/custom string
  - `_get_person_function()` - person data with gender
  - `_get_address_function()` - address selection
  - `get_function()` - final function string for insertion

#### Dynamic Function Format:

```
${random(10, true, true)}      # Random 10 chars, letters+digits
${uuid()}                       # UUID v4
${custom("HN##", true)}        # Custom template H=letter, #=digit, uppercase
${person("first_name", "Male")} # Person data
${address("country")}           # Address data
```

#### Implementation Integration:

- Functions are inserted as `${...}` syntax in request fields
- `httprider/core::replace_variables()` processes at execution time

---

### 2.4 Fuzzing / Chaos Testing

**Feature:** Automatically fuzz requests with random data to test robustness

#### Sub-Features:

- **Batch Fuzzing** (generate N random payloads)
- **JSON Schema-Based Fuzzing** (infer schema from request body)
- **Random Payload Generation** (fill fields with random values)
- **Configurable Limits**:
  - Max array items (for list fields)
  - Max string length (for string fields)
  - Number of requests to generate
- **Response Aggregation** (count 2xx, 3xx, 4xx, 5xx responses)
- **Fuzz Results Display** (markdown-formatted output)
- **Status Distribution** (show response code distribution)
- **Full Request/Response Logging** (see each fuzzy request attempt)

#### Entry Points:

- `httprider/ui/fuzz_test_dialog.py` :: UI dialog
- `httprider/presenters/fuzz_test_presenter.py` :: Main presenter
- Context menu on request: "Fuzz Test"

#### Core Logic:

- `httprider/presenters/fuzz_test_presenter.py` :: `FuzzTestPresenter`
  - `on_fuzz_test()` - execute fuzzing
  - `__prepare_fuzzed_exchange_from_api_call()` - generate fuzzed request
  - `__generate_fuzzed_payload()` - random JSON from schema
  - `__update_results()` - aggregate response codes
  - `__on_result()` - process each fuzzy response
- `httprider/core/json_data_generator.py` :: `JsonDataGenerator`
  - `json_from_schema()` - generate JSON from JSON schema
  - `update_limits()` - set max values
- `httprider/core/json_schema.py` :: `schema_from_json()`
  - Infer JSON schema from request body JSON
- `httprider/external/rest_api_connector.py` :: Async execution
  - Queue worker tasks for each fuzz request
  - Non-blocking async execution

#### Data Model:

- `ExchangeRequest.request_type = ExchangeRequestType.FUZZED` - mark fuzzy requests
- Each fuzzy iteration creates HttpExchange for tracking

#### Results Display:

- Count 2xx, 3xx, 4xx, 5xx status codes
- Full markdown-formatted request/response for each attempt
- Aggregated summary display

---

## 3. CODE GENERATION & EXPORT (16+ Formats)

**Feature:** Generate code snippets and export requests in multiple languages/frameworks

#### Supported Export Formats:

1. **cURL** - Shell commands
2. **Python Requests** - Python code using requests library
3. **Java Feign** - Spring Feign client code
4. **Java Spring Boot** - MockMvc test code
5. **Java RestAssured** - RestAssured test code
6. **Spring Cloud Contract Tests** - Contract testing code
7. **Locust** - Python load testing code
8. **ApickLi** - Gherkin BDD syntax
9. **Runscope** - Runscope API testing format
10. **Slow Cooker** - Load testing tool format
11. **Markdown** - Documentation format
12. **Mermaid** - Mermaid diagram syntax
13. **PlantUML** - PlantUML sequence diagrams
14. **Confluence** - Confluence wiki markup
15. **OpenAPI 3.0** - OpenAPI specification
16. **Postman Collections** - Postman collection format

#### Entry Points:

- `httprider/ui/code_generator_dialog.py` :: UI dialog
- `httprider/presenters/code_generator_presenter.py` :: Main presenter
- Menu: Requests → Export (Ctrl+E) / Export All (Ctrl+Shift+E)

#### Core Logic:

- `httprider/presenters/code_generator_presenter.py` :: `CodeGeneratorPresenter`
  - `show_dialog()` - load exporter list
  - `on_exporter_change()` - change selection
  - `generate_code()` - generate for single or all APIs
  - `on_copy_clipboard()` - copy to clipboard
  - `on_export_file()` - save to file
- `httprider/exporters/` :: Individual exporter modules
  - `exporter_curl.py`, `exporter_python_requests.py`, etc.
  - Each implements export logic for specific format
  - `export_data(api_calls)` - main method
- `httprider/exporters/common.py` :: Shared utilities
  - `api_request_body_highlighted()` - formatted body
  - `highlight_format_json()` - JSON syntax highlight
  - `request_body_highlighted()`, `response_body_highlighted()`

#### Plugin System:

- `httprider/exporters/__init__.py` :: `exporter_plugins` registry
  - Dynamic plugin loading
  - Each exporter registered with name + class

#### Code Generation Details:

Each exporter includes:

- **Request Gen** - transform ApiCall to code
- **Assertion Gen** - convert test assertions to framework-specific assertions
- **Variable Gen** - handle variable references
- **Header Gen** - include headers in code
- **Body Gen** - serialize request body

Examples:

- **Java Spring**: MockMvc test with `.andExpect()` assertions
- **Python Requests**: requests.post() with assertions
- **Markdown**: Formatted request/response documentation
- **OpenAPI**: Paths + Schemas from all requests

#### Output Options:

- Copy to clipboard
- Save to file
- Display in UI

#### Signal Subscriptions:

- `api_call_change_selection` - update selected API for generation

---

## 4. IMPORT FEATURES

**Feature:** Import requests from external formats

#### Supported Import Formats:

1. **cURL Commands** - Parse and convert cURL to ApiCall
2. **OpenAPI 3.0** - Import from OpenAPI specification
3. **Postman Collections** - Import from Postman collection.json

#### Entry Points:

- `httprider/ui/import_text_dialog.py` :: Text input dialog
- `httprider/presenters/importer_presenter.py` :: Main presenter
- Menu: Import → [format name]

#### Core Logic:

- `httprider/presenters/importer_presenter.py` :: `ImporterPresenter`
  - `import_collection()` - detect file vs. text input
  - `on_selected_text_to_import()` - process imported text
- `httprider/importers/` :: Individual importer modules
  - `importer_curl.py` - cURL parser
    - Parse cURL syntax: `-X`, `-H`, `-d`, `--form`, etc.
    - Output: list of ApiCall objects
  - `importer_openapi_v3.py` - OpenAPI parser
    - Parse OpenAPI schema document
    - Generate ApiCall from path definitions
    - Handle parameters, request bodies, etc.
  - `importer_postman_collections.py` - Postman parser
    - Parse Postman collection.json
    - Extract requests + folder structure
    - Preserve tags/descriptions
- `httprider/importers/__init__.py` :: `importer_plugins` registry

#### Processing:

- File input: Read file, parse, return list of ApiCall
- Text input: Show dialog, paste text, parse on submission
- ProjectInfo extraction: Get title, version, tags from import source

#### Storage:

- `api_call_interactor.add_multiple_api_calls(api_calls)` - batch insert
- Emits `multiple_api_calls_added` signal
- Updates `project_info` if available

#### Plugin System:

- Dynamic importer registration
- `input_type` property: "file" or "text"
- `import_data()` method - main parser

---

## 5. ORGANIZATION & MANAGEMENT

### 5.1 Projects

**Feature:** Manage multiple projects with separate request collections

#### Sub-Features:

- **Project File Storage** (SQLite per project)
- **Project Information**:
  - Title, version, description
  - API terms of service URL
  - License URL and name
  - Contact name and email
  - Tags (categorization)
  - Servers (base URLs)
  - Common headers across all requests
  - Setup/teardown code
- **Open Recent Projects** (quickly switch between projects)
- **New/Open/Save Project** (file operations)
- **Project Info Dialog** (edit metadata)
- **Common Headers** (shared headers for all requests)
- **Server Configuration** (base URLs for API)

#### Entry Points:

- `httprider/ui/project_info_dialog.py` :: UI dialog
- `httprider/presenters/project_info_presenter.py` :: Main presenter
- Menu: File → New/Open/Save
- Application startup loads last project

#### Core Logic:

- `httprider/model/app_data.py`
  - `ProjectInfo` - metadata
    - Fields: `title`, `version`, `tos_url`, `contact_name`, `contact_email`, `info`, `license_url`, `license_name`, `tags`, `servers`, `common_headers`, `setup_code`, `teardown_code`
  - `TagInfo` - tag with name + description
- `httprider/presenters/project_info_presenter.py` :: `ProjectInfoPresenter`
  - `show_dialog()` - load project info
  - `on_add_new_server()` - add server URL
  - `on_remove_selected_server()` - delete server
  - `on_close()` - save changes
  - `reload_tags()` - update tags from API calls
- `httprider/core/core_settings.py` :: `CoreSettings`
  - `load_current_project()` - get active project
  - `save_current_project()` - persist project selection
- `httprider/model/app_data_reader.py`
  - `get_or_create_project_info()` - load or initialize

#### Persistence:

- Project data stored in SQLite
- Each project has separate database file
- `app_data_writer.update_project_info()` - save metadata

#### Signal Subscriptions:

- `api_call_tag_added`, `api_call_tag_removed` - auto-update tags
- `project_info_updated` - refresh display

---

### 5.2 API Collections / Folders / Tree Structure

**Feature:** Organize requests hierarchically with tags

#### Sub-Features:

- **Tag-based Organization** (assign multiple tags per request)
- **Tag Filtering** (show only requests with selected tag)
- **Show All View** (DEFAULT_TAG shows all requests)
- **Tag Auto-Discovery** (tags auto-created when added to request)
- **Visual Tag Labels** (colored tag chips on request)
- **Tag Management** (rename, delete tags)

#### Entry Points:

- `httprider/presenters/tags_list_presenter.py` :: Toolbar tag dropdown
- `httprider/presenters/request_presenter.py` :: Tag input UI
- Request context menu

#### Core Logic:

- `httprider/model/app_data.py`
  - `ApiCall.tags` - list of tag names
- `httprider/presenters/tags_list_presenter.py` :: `TagsListPresenter`
  - `on_tag_changed(tag_name)` - filter by tag
  - `refresh()` - populate dropdown with tags
- `httprider/presenters/api_list_presenter.py`
  - Tag filtering applied via `app_data_cache.filter_api_calls()`
- `httprider/core/app_state_interactor.py`
  - `update_selected_tag()` - persist tag selection
- `httprider/presenters/request_presenter.py`
  - `add_new_tag_label()` - create tag
  - `get_all_tags()` - collect tags from form

#### Index:

- `httprider/core/constants.py` :: `DEFAULT_TAG = "Show All"`
- Represents unfiltered view

#### Signal Subscriptions:

- `selected_tag_changed` - refresh API list
- `api_call_tag_added`, `api_call_tag_removed` - update tag dropdown

---

### 5.3 Search & Filtering

**Feature:** Find requests by various criteria

#### Sub-Features:

- **Tag Selection** (filter by single tag)
- **Search by Title** (text search in request titles)
- **Search by URL** (find by endpoint)
- **Enabled/Disabled Filtering** (show/hide disabled requests)
- **Assertion Status Filtering** (show passing/failing)
- **Live Filtering** (real-time as you type)

#### Entry Points:

- `httprider/presenters/tags_list_presenter.py` :: Tag dropdown
- Request list auto-filters on tag change
- `httprider/ui/main_window.py` :: Title/description fields searchable

#### Core Logic:

- `httprider/core/app_data_cache.py`
  - `filter_api_calls()` - apply current filters
  - `get_appstate_tag()` - get selected tag filter
  - Applies tag filter to return matching requests
- `httprider/core/app_state_interactor.py` :: Track filter state
  - `update_selected_tag()` - save filter choice
  - `update_selected_search()` - save search text
  - `update_selected_environment()` - save env filter

#### Persistence:

- Filter choices saved to `AppState` record in SQLite
- Restored on app startup

---

## 6. CONFIGURATION & SETTINGS

### 6.1 Application Settings

**Feature:** Configure application behavior and network parameters

#### Sub-Features:

- **Update Check** (enable/disable auto-update checking)
- **Update Check on Startup** (check for updates when app launches)
- **TLS/SSL Verification** (enable/disable certificate validation)
- **Allow Redirects** (follow HTTP redirects)
- **HTTP Timeout** (seconds to wait for response)
- **Proxy Configuration**:
  - HTTP proxy URL
  - HTTPS proxy URL
  - No-proxy list (domains to skip proxy)
- **Printer Server** (print server configuration)

#### Entry Points:

- `httprider/ui/configuration_dialog.py` :: Settings dialog
- `httprider/presenters/config_presenter.py` :: Main presenter
- Menu: File → Settings (or preferences)

#### Core Logic:

- `httprider/presenters/config_presenter.py` :: `ConfigPresenter`
  - `load_configuration_dialog()` - load current settings
  - `form_to_object()` - collect form values
  - `object_to_form()` - populate form from config
  - `on_success()` - save settings
- `httprider/model/app_configuration.py` :: `AppConfiguration`
  - Dataclass for all settings
  - Fields: `update_check_on_startup`, `tls_verification`, `allow_redirects`, `http_proxy`, `https_proxy`, `no_proxy`, `timeout_in_secs`, `print_server`
- `httprider/core/core_settings.py` :: `CoreSettings`
  - `load_configuration()` - read from persistent storage
  - `save_configuration()` - write to persistent storage

#### Persistence:

- Stored in application config file (likely JSON/YAML)
- `app_settings.save_configuration(config)` persists

#### Signal Subscriptions:

- Settings loaded on app initialization
- Changes applied immediately

---

### 6.2 Themes & Appearance

**Feature:** Visual theme and display preferences

#### Sub-Features:

- **Dark Mode / Light Mode** (automatic or manual selection)
- **Syntax Highlighting** (code coloring for JSON, XML)
- **Status Code Coloring** (green/amber/red for 2xx/4xx/5xx)
- **Assertion Result Coloring** (pass/fail visual indicators)

#### Entry Points:

- Application-wide theme applied on startup
- `httprider/themes/` module

#### Core Logic:

- `httprider/themes/theme_provider.py` :: Theme configuration
  - `configure_theme()` - apply theme stylesheet
  - `is_dark()` - detect dark mode preference
  - Color functions for various UI elements:
    - `api_call_list_rect()` - request list background
    - `http_ex_success()` - green for 2xx
    - `http_ex_client_err()` - amber for 4xx
    - `http_ex_server_err()` - red for 5xx/no response
- `httprider/core/pygment_styles.py` :: Code syntax highlighting
  - `pyg_styles()` - Pygments CSS for code display
- `httprider/themes/theme.py` :: Theme class
  - `load_stylesheet(theme_mode)` - apply stylesheet

#### Response Code Color Coding:

- `httprider/presenters/api_calls_history_presenter.py`
  - `color_from_response()` method maps codes to colors
  - 100-399: green (success)
  - 400-499: amber (client error)
  - 500-599: red (server error)
  - ≤0: red (no response)

#### Assertion Color Coding:

- `httprider/widgets/api_calls_list_view.py`
  - `color_from_assertions()` - ✅ green / ⛔ red
  - Shows assertion result next to response code

---

## 7. UI/UX FEATURES

### 7.1 Syntax Highlighting & Formatting

**Feature:** Code and data formatting with visual syntax highlighting

#### Sub-Features:

- **Request Body Highlighting** (JSON, XML, plain text)
- **Response Body Highlighting** (same as request)
- **Code Export Highlighting** (syntax highlight in code generator)
- **Markdown Rendering** (markdown content in display)
- **Language Detection** (auto-detect JSON vs XML vs plain text)
- **JSON Pretty-Print** (formatted with indentation)
- **Custom Styles** (PyQt-integrated highlighting)

#### Core Logic:

- `httprider/core/pygment_styles.py`
  - `pyg_styles()` - CSS stylesheet for Pygments
  - Returns HTML/CSS for syntax highlighting
- `httprider/exporters/common.py`
  - `highlight_format_json()` - JSON formatting + highlighting
  - `api_request_body_highlighted()` - request body formatted
  - `request_body_highlighted()`, `response_body_highlighted()` - response bodies
- `httprider/core/markdown_renderer.py`
  - `HighlightRenderer` - Markdown to HTML with code highlighting
- Rendering via Pygments library (Python syntax highlighting)

#### Implementation:

```python
# Applied to QPlainTextEdit widgets:
self.view.txt_request_body.document().setDefaultStyleSheet(pyg_styles())
```

---

### 7.2 Request/Response Comparison

**Feature:** View and compare requests and responses side-by-side or sequentially

#### Sub-Features:

- **Raw Request Display** (full HTTP formatted request)
- **Raw Response Display** (full HTTP response)
- **Request Details** (headers, params, body in tables)
- **Response Details** (headers, body in tables/text)
- **Side-by-Side View** (request on left, response on right)
- **Tabbed View** (switch between request detail tabs)

#### Entry Points:

- `httprider/presenters/exchange_presenter.py` :: Main display
- `httprider/ui/main_window.py` :: Exchange frame

#### Core Logic:

- `httprider/presenters/exchange_presenter.py` :: `ExchangePresenter`
  - `refresh()` - populate all display fields
  - `display_last_exchange()` - show most recent
  - `render_raw_exchange()` - format raw request/response
- `httprider/presenters/common.py`
  - `markdown_request()` - format request as markdown
  - `markdown_response()` - format response as markdown
  - `md_request_response_generator()` - combined markdown
- `httprider/model/completer.py` - request preview data

#### Display Structure:

```
Request:
  - Raw (markdown + code syntax)
  - Headers (table)
  - Query Params (table)
  - Form Params (table)
  - Body (formatted text)

Response:
  - Raw (markdown + code syntax)
  - Headers (table)
  - Body (formatted text)

Metadata:
  - Request time
  - Response time
  - Status code
```

---

### 7.3 Drag-and-Drop Support

**Feature:** Reorder requests via drag-and-drop

#### Sub-Features:

- **Request Reordering** (drag request in list to new position)
- **Drop Position Tracking** (track where item was dropped)
- **Sequence Update** (update `sequence_number` on drop)

#### Entry Points:

- `httprider/widgets/api_calls_list_view.py` :: Custom list view
- `httprider/presenters/api_list_presenter.py` :: Drop handler

#### Core Logic:

- `httprider/widgets/api_calls_list_view.py` :: `ApiCallsListView (QListView)`
  - Inherits from QListView with custom drag-drop
  - `drop_event_signal` - emits on drop
  - Default drop action enabled
- `httprider/presenters/api_list_presenter.py` :: `ApiListPresenter`
  - `on_drop_event()` - handle drop event
  - `dropped_row` - track drop position
  - Update sequence numbers after drop

#### Model Update:

- Model: `QStandardItemModel` (standard Qt model)
- Supports default move item behavior
- Sequence numbers updated via `api_call_interactor.update_api_call()`

---

## 8. SHARING & COLLABORATION

### 8.1 Share Preview / Document Generation

**Feature:** Create shareable documents of request/response pairs

#### Sub-Features:

- **Markdown Export** (generate markdown from request)
- **HTML Preview** (render markdown to HTML)
- **Share Document** (upload to sharing service)
- **Shared Document Link** (get URL to shared doc)
- **Print-friendly** (optimized for printing)
- **Edit & Preview Toggle** (switch between edit/preview modes)
- **Project Metadata Inclusion** (include title, version, description)
- **Multiple Exchanges** (combine multiple request/response pairs)

#### Entry Points:

- `httprider/ui/share_preview_dialog.py` :: UI dialog
- `httprider/presenters/share_preview_presenter.py` :: Main presenter
- Exchange frame "Share Preview" button

#### Core Logic:

- `httprider/presenters/share_preview_presenter.py` :: `SharePreviewPresenter`
  - `show_dialog()` - display single exchange
  - `show_dialog_multiple_apis()` - multiple APIs
  - `render_preview()` - toggle edit/preview
  - `share_exchange()` - upload to service
  - `update_cached_markdown()` - sync edited markdown
  - `md_for_exchange()` - convert exchange to markdown
  - `md_for_project_info()` - include project metadata
- `httprider/interactors/share_service_interactor.py` :: `ShareServiceInteractor`
  - `create_document()` - upload markdown to sharing service
  - Handles remote service integration
- `httprider/core/markdown_renderer.py`
  - `HighlightRenderer` - render to syntax-highlighted HTML

#### Markdown Format:

```markdown
## Project Title

Project description

### Request Title

Request description

#### Request

GET /endpoint
Headers: ...
Params: ...

#### Response

HTTP 200
Headers: ...
Body: ...
```

#### Sharing Service:

- Signal emitted: `exchange_share_created` with sharing URL
- Signal emitted: `exchange_share_failed` with error message

---

## 9. MOCKING

### 9.1 Mocked Responses

**Feature:** Define mocked HTTP responses for testing without calling actual API

#### Sub-Features:

- **Mock Enable/Disable** (toggle mock on/off per request)
- **Mock Status Code** (set HTTP response code)
- **Mock Headers** (set response headers)
- **Mock Body** (set response body)
- **Variable Support** (use environment variables in mock body)
- **Formatted Body Support** (JSON, XML, plain text)
- **Mock Indicator** (show when response is mocked)

#### Entry Points:

- `httprider/presenters/request_presenter.py` :: Mocked Response section
- `httprider/presenters/mocked_response_presenter.py` :: Main presenter

#### Core Logic:

- `httprider/model/app_data.py`
  - `MockedResponse` - mock definition
  - Fields: `is_enabled`, `status_code`, `headers`, `body`
- `httprider/presenters/mocked_response_presenter.py` :: `MockedResponsePresenter`
  - `form_to_object()` - collect mock definition from UI
  - `object_to_form()` - populate form from mock config
  - `refresh_completer()` - variable completion in mock body
- `httprider/presenters/request_presenter.py`
  - `get_mocked_response()` - retrieve mock config from form
- `httprider/external/rest_api_connector.py`
  - Check `api_call.mocked_response.is_enabled` before executing
  - Return mock response instead of executing HTTP

#### Execution Flow:

1. Check if mock is enabled
2. If yes, create `ExchangeResponse` from `MockedResponse` config
3. If no, execute real HTTP request
4. Return either mocked or real response

---

## 10. UTILITIES & HELPERS

### 10.1 Utility Functions

**Feature:** Helper tools and utilities

#### Sub-Features:

- **Project Info Editing** (dialog for metadata)
- **Assertion Builder** (visual assertion builder)
- **Code Generator** (export in multiple formats)
- **Data Generator** (generate test data)
- **Utility Functions Dialog** (helper functions reference)

#### Entry Points:

- Various menu items and toolbar buttons
- Dialog shortcuts with keyboard combinations

#### Common Presenter Pattern:

```
Main Presenter → Initializes Dialogs
Dialog Presenter → Handles dialog logic
Dialog View (Qt Designer generated) → UI definition
```

---

## 11. DATA MODEL & STORAGE

### Core Data Structures:

```python
# ApiCall - HTTP request definition
ApiCall:
  - id: unique identifier
  - title: request name
  - description: documentation
  - http_method: HTTP verb
  - http_url: endpoint URL
  - http_headers: request headers (dict)
  - http_params: query parameters (dict)
  - form_params: form body parameters (dict)
  - http_request_body: raw request body
  - tags: list of categorization tags
  - enabled: is request active
  - last_response_code: HTTP code from last execution
  - last_assertion_result: pass/fail from last test
  - mocked_response: MockedResponse config
  - is_separator: visual divider in list
  - sequence_number: ordering

# HttpExchange - request-response pair
HttpExchange:
  - api_call_id: reference to ApiCall
  - id: unique identifier
  - request: ExchangeRequest (what was sent)
  - response: ExchangeResponse (what was received)
  - response_status: NONE | PASSED | FAILED
  - assertions: list of Assertion results

# Environment - variables collection
Environment:
  - id: unique identifier
  - name: environment name
  - data: dict of variable names → DynamicStringData

# ApiTestCase - assertions for one request
ApiTestCase:
  - api_call_id: reference to ApiCall
  - id: unique identifier
  - assertions: list of Assertion definitions

# ProjectInfo - project metadata
ProjectInfo:
  - title, version, description
  - contact info, license, terms
  - servers (base URLs)
  - common_headers
  - tags
```

### Persistence:

- SQLite database (one per project)
- Uses dataset ORM for table access
- `app_data_writer.py` - write operations + signal emission
- `app_data_reader.py` - read operations
- `app_data_cache.py` - in-memory cache of all data

### Signal-Driven Architecture:

```
User Action → Interactor → DB Write → Signal Emit → Cache Update → Presenter Refresh
```

All UI refreshes driven by signals, never direct updates.

---

## 12. MVP ARCHITECTURE

### Presenter Hierarchy:

```
MainPresenter (lifecycle)
├── ApiListPresenter (request list)
├── RequestPresenter (request form)
├── ExchangePresenter (response display)
├── EnvironmentConfigurationPresenter (env management)
├── TagsListPresenter (filter dropdown)
├── AssertionBuilderPresenter (assertion UI)
├── CodeGeneratorPresenter (export)
├── ImporterPresenter (import)
├── SharePreviewPresenter (document sharing)
├── ConfigPresenter (settings)
├── ProjectInfoPresenter (project metadata)
└── [20+ more specialized presenters]
```

### Data Flow:

```
UI Input → Presenter.form_to_object() →
Interactor.update_*() →
AppDataWriter.update_*_in_db() →
Signals.emit() →
AppDataCache.update() →
Presenter.refresh() /
AppDataReader.signals trigger Presenter.refresh()
```

### No Direct UI Updates:

- Presenters never modify UI directly
- Always go through signals
- Cache maintains single source of truth
- Multiple windows stay in sync via signals

---

## SUMMARY TABLE

| Feature Category  | Sub-Feature         | Module                         | Entry Point                             |
| ----------------- | ------------------- | ------------------------------ | --------------------------------------- |
| **Core Testing**  | Request CRUD        | api_call_interactor.py         | request_presenter.py                    |
|                   | Request Execution   | rest_api_connector.py          | request_presenter.on_btn_send_request() |
|                   | Response Viewing    | exchange_presenter.py          | main_window.frame_exchange              |
|                   | Request History     | api_calls_history_presenter.py | main_window.horizontalLayout_6          |
| **Advanced**      | Assertions          | assertion_builder_presenter.py | assertion_builder_dialog.py             |
|                   | Environments        | environment_interactor.py      | environment_configuration_dialog.py     |
|                   | Data Generation     | data_generator_presenter.py    | data_generator_dialog.py                |
|                   | Fuzzing             | fuzz_test_presenter.py         | fuzz_test_dialog.py                     |
| **Export/Import** | Code Generation     | code_generator_presenter.py    | code_generator_dialog.py                |
|                   | Export (16 formats) | exporters/\*.py                | menu: Requests → Export                 |
|                   | Import (3 formats)  | importers/\*.py                | menu: Import → [format]                 |
| **Organization**  | Projects            | project_info_presenter.py      | project_info_dialog.py                  |
|                   | Tags/Filtering      | tags_list_presenter.py         | main_window.tool_bar                    |
|                   | Environments        | envs_list_presenter.py         | main_window.tool_bar                    |
| **Config**        | Settings            | config_presenter.py            | configuration_dialog.py                 |
|                   | Themes              | theme_provider.py              | application.py                          |
| **UX**            | Syntax Highlighting | pygment_styles.py              | All text widgets                        |
|                   | Mocking             | mocked_response_presenter.py   | request_presenter.py                    |
|                   | Sharing             | share_preview_presenter.py     | share_preview_dialog.py                 |

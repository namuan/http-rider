# HTTP-Rider Feature Architecture Diagram

## User-Facing Feature Map (Product Engineer View)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        HTTP-RIDER REST API CLIENT                           │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ CORE TESTING FEATURES                                                  │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                        │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────────┐   │ │
│  │  │  Request Form   │  │ Response Viewer  │  │ Request History    │   │ │
│  │  ├─────────────────┤  ├──────────────────┤  ├────────────────────┤   │ │
│  │  │• HTTP Method    │  │• Status Code     │  │• Last 10 Exchanges │   │ │
│  │  │• URL/Endpoint   │  │• Headers Table   │  │• Color-coded       │   │ │
│  │  │• Headers        │  │• Body (formatted)│  │• Exchange Switch   │   │ │
│  │  │• Query Params   │  │• Raw Request     │  │• Response Codes    │   │ │
│  │  │• Form Data      │  │• Raw Response    │  │                    │   │ │
│  │  │• Body (JSON)    │  │• Time Display    │  │                    │   │ │
│  │  │• Title/Desc     │  │• Syntax Highlight│  │                    │   │ │
│  │  │• Tags           │  │                  │  │                    │   │ │
│  │  │• Send Button    │  │                  │  │                    │   │ │
│  │  └─────────────────┘  └──────────────────┘  └────────────────────┘   │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ ADVANCED TESTING                                                       │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                        │ │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────┐ │ │
│  │  │  Assertions      │  │  Environments    │  │  Data Generation    │ │ │
│  │  ├──────────────────┤  ├──────────────────┤  ├─────────────────────┤ │ │
│  │  │• Response Code   │  │• Env Variables   │  │• Random Strings     │ │ │
│  │  │• Response Time   │  │• Env Selection   │  │• UUID Generation    │ │ │
│  │  │• Header Asserts  │  │• Var Substitution│  │• Custom Templates   │ │ │
│  │  │• Body Path Assert│  │• Env Import/Exp  │  │• Person Data        │ │ │
│  │  │• Value Extraction│  │• Common Headers  │  │• Address Data       │ │ │
│  │  │• Matchers:       │  │• Secret Values   │  │• Live Preview       │ │ │
│  │  │  - equals        │  │• Duplication     │  │• Variable Insert    │ │ │
│  │  │  - contains      │  │• Multipl Envs    │  │                     │ │ │
│  │  │  - null/empty    │  │                  │  │                     │ │ │
│  │  │  - regex match   │  │                  │  │                     │ │ │
│  │  │  - < / >         │  │                  │  │                     │ │ │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────────┘ │ │
│  │                                                                        │ │
│  │  ┌──────────────────┐                                                 │ │
│  │  │  Fuzzing / Chaos │                                                 │ │
│  │  ├──────────────────┤                                                 │ │
│  │  │• Random Payload  │                                                 │ │
│  │  │• JSON Schema Gen │                                                 │ │
│  │  │• Batch Mode      │                                                 │ │
│  │  │• Status Aggr.    │                                                 │ │
│  │  │• Configurable    │                                                 │ │
│  │  │  Limits          │                                                 │ │
│  │  │• Results Output  │                                                 │ │
│  │  └──────────────────┘                                                 │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ EXPORT / IMPORT / CODE GENERATION (16+ Formats)                       │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                        │ │
│  │  Export To:                                                           │ │
│  │  • cURL                    • Java Spring Boot                         │ │
│  │  • Python Requests         • Spring Contract Tests                    │ │
│  │  • Java Feign              • Locust (Python)                          │ │
│  │  • Java RestAssured        • Runscope, Slow Cooker                    │ │
│  │  • Markdown (Docs)         • Mermaid Diagrams                         │ │
│  │  • PlantUML (Diagrams)     • Confluence                               │ │
│  │  • OpenAPI 3.0 Spec        • Postman Collections                      │ │
│  │                                                                        │ │
│  │  Import From:                                                         │ │
│  │  • cURL Commands           • OpenAPI 3.0 Specs                        │ │
│  │  • Postman Collections                                                │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ ORGANIZATION & MANAGEMENT                                             │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                        │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────┐ │ │
│  │  │  Projects       │  │  Tags/Filtering  │  │  Search             │ │ │
│  │  ├─────────────────┤  ├──────────────────┤  ├─────────────────────┤ │ │
│  │  │• Project File   │  │• Tag Selection   │  │• Filter by Tag      │ │ │
│  │  │• New/Open/Save  │  │• Auto-Discovery  │  │• Live Filtering     │ │ │
│  │  │• Title/Version  │  │• Tagged Requests │  │• By Title/URL       │ │ │
│  │  │• Metadata       │  │• Tag Labels      │  │                     │ │ │
│  │  │• Contact Info   │  │• Multiple Tags   │  │                     │ │ │
│  │  │• License        │  │• Tag Rename      │  │                     │ │ │
│  │  │• Common Headers │  │                  │  │                     │ │ │
│  │  │• Server URLs    │  │                  │  │                     │ │ │
│  │  └─────────────────┘  └──────────────────┘  └─────────────────────┘ │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ CONFIGURATION & FEATURES                                              │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                        │ │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────┐ │ │
│  │  │  Settings        │  │  Themes          │  │  Mocking/Sharing    │ │ │
│  │  ├──────────────────┤  ├──────────────────┤  ├─────────────────────┤ │ │
│  │  │• Update Check    │  │• Dark/Light      │  │• Mock Response      │ │ │
│  │  │• TLS Verify      │  │• Syntax Highlight│  │• Mock Body          │ │ │
│  │  │• Redirects       │  │• Code Coloring   │  │• Share Preview      │ │ │
│  │  │• Timeout         │  │• Status Coloring │  │• Document Link      │ │ │
│  │  │• Proxy Config    │  │• Assertion Colors│  │• Markdown Export    │ │ │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────────┘ │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Code Module → Feature Mapping

```
PRESENTERS (MVP Controllers)
├── main_presenter.py ..................... App lifecycle + state restoration
├── request_presenter.py .................. Request form +SEND button
├── exchange_presenter.py ................. Response display/formatting
├── api_list_presenter.py ................. Request list + drag-drop
├── api_calls_history_presenter.py ........ Last 10 exchanges
├── assertion_builder_presenter.py ........ Visual assertion builder
├── assertion_list_presenter.py ........... Assertion definition
├── assertion_result_presenter.py ......... Assertion execution + evaluation
├── environment_configuration_presenter.py Environment variable mgmt
├── envs_list_presenter.py ............... Environment dropdown
├── tags_list_presenter.py ............... Tag filter dropdown
├── data_generator_presenter.py .......... Faker/random value generation
├── fuzz_test_presenter.py ............... Fuzzing execution
├── code_generator_presenter.py .......... Code export dialog
├── importer_presenter.py ................ Import dialog
├── config_presenter.py .................. Settings dialog
├── project_info_presenter.py ............ Project metadata dialog
├── share_preview_presenter.py ........... Document sharing
├── mocked_response_presenter.py ......... Mock response config
└── [+15 more specialized presenters]

CORE LOGIC (Business Rules)
├── api_call_interactor.py .............. Request CRUD
├── environment_interactor.py ........... Environment CRUD
├── app_state_interactor.py ............. State persistence (selected filters)
├── safe_rest_api_interactor.py ......... HTTP execution wrapper
├── generators.py ....................... Faker + random value generators
├── json_data_generator.py .............. Fuzz payload generation
└── faker_config.py ..................... Faker library configuration

EXTERNAL (HTTP + Async)
├── rest_api_connector.py ............... QThread-based HTTP executor
└── requester.py ........................ requests library wrapper

MODELS (Data + SQL)
├── app_data.py ....................... Core dataclasses (ApiCall, HttpExchange, etc.)
├── app_data_cache.py ................. In-memory cache + filtering
├── app_data_writer.py ................ SQL writes + signal emission
├── app_data_reader.py ................ SQL reads
├── app_configuration.py .............. Settings storage
├── completer.py ...................... Variable completion
└── storage.py ........................ SQLite connection

EXPORTERS (16+ Formats)
├── exporter_curl.py .................. cURL export
├── exporter_python_requests.py ....... Python Requests export
├── exporter_java_feign_client.py ..... Java Feign export
├── exporter_java_spring_boot_api.py . Spring Boot test export
├── exporter_spring_contract_tests.py  Contract testing export
├── exporter_restassured.py ........... RestAssured export
├── exporter_locust_tests.py .......... Locust load test export
├── exporter_apickli.py ............... ApickLi BDD export
├── exporter_runscope.py .............. Runscope export
├── exporter_slow_cooker.py ........... Slow Cooker export
├── exporter_markdown.py .............. Markdown documentation
├── exporter_mermaid.py ............... Mermaid diagrams
├── exporter_plantuml.py .............. PlantUML diagrams
├── exporter_confluence.py ............ Confluence wiki format
├── exporter_openapi_v3.py ............ OpenAPI 3.0 spec
├── exporter_postman_collections.py ... Postman collection export
└── common.py ......................... Shared export utilities

IMPORTERS (3 Formats)
├── importer_curl.py .................. cURL command parser
├── importer_openapi_v3.py ............ OpenAPI spec parser
└── importer_postman_collections.py ... Postman collection parser

UI DIALOGS
├── assertion_builder_dialog.py ........ Assertion visual builder
├── configuration_dialog.py ............ Settings UI
├── data_generator_dialog.py .......... Faker/random value UI
├── environment_configuration_dialog.py Environment config UI
├── fuzz_test_dialog.py ............... Fuzzing configuration
├── code_generator_dialog.py .......... Export code dialog
├── import_text_dialog.py ............. Import text input
├── progress_dialog.py ................ Progress display
├── project_info_dialog.py ............ Project metadata UI
└── share_preview_dialog.py ........... Share/export dialog

UI UTILITIES
├── main_window.py .................... Main window container
├── menus.py .......................... Menu bar items
├── toolbar.py ........................ Toolbar buttons
├── shortcuts.py ...................... Keyboard shortcuts
├── themes/ ........................... Theme management
│   ├── theme.py ...................... Theme stylesheet
│   └── theme_provider.py ............. Dark/light mode colors
├── widgets/ .......................... Custom UI components
│   ├── api_calls_list_view.py ........ Custom list with drag-drop
│   ├── completion_line_edit.py ....... Autocomplete text input
│   ├── tag_label_widget.py ........... Tag display widget
│   └── [+3 more custom widgets]
└── util/pygment_styles.py ............ Syntax highlighting

CODEGEN
├── schema_to_java_generator.py ....... Java class generation from schema
└── http_status_code_mapping.py ....... HTTP status code utilities
```

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERACTIONS                         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  PRESENTERS (MVP)  │
        │  ├─ form_to_object │ (Collect UI → Data)
        │  └─ refresh()      │ (Update UI from Data)
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  INTERACTORS       │
        │  ├─ add_*()        │ (Business logic)
        │  ├─ update_*()     │
        │  └─ remove_*()     │
        └────────┬───────────┘
                 │
                 ▼
   ┌─────────────────────────────┐
   │   AppData{Writer|Reader}    │
   │  ├─ update_*_in_db()        │ (SQL WRITE)
   │  ├─ Signals.emit() ◄────────┼─── Signal Emitted
   │  └─ get_*()                 │ (SQL READ)
   └─────────┬───────────────────┘
             │
             ▼
   ┌─────────────────────────────┐
   │        SQ LITE DATABASE     │
   └─────────┬───────────────────┘
             │
             ├──────────────────────┐
             │                      │
    ┌────────▼─────────┐  ┌────────▼──────┐
    │  AppDataCache    │  │ AppState      │
    │  (In-Memory)     │  │ (Selected Tag)│
    │  ├─ filter_apis()│  │               │
    │  └─ update()◄────┼──┤ Signals.emit()│
    └────────┬─────────┘  └────────┬──────┘
             │                     │
             │     ┌───────────────┘
             │     │
             ▼     ▼
    ┌─────────────────────────────┐
    │   Presenter.refresh() ◄──────┼── Subscribe to Signals
    │   Update UI (reactive)       │
    └─────────────────────────────┘
```

**Key Principle:** NEVER modify UI directly. Always:

1. Modify data via Interactor
2. Data goes to DB
3. Signal emitted
4. Cache updated
5. Presenter refreshes UI reactively

---

## Feature Entry Points (How to Invoke Each Feature)

```
EXECUTION                              MENU/UI                      SHORTCUT
─────────────────────────────────────────────────────────────────────────────
Send Single Request                    Requests > Send              Ctrl+Return
Send All Requests                      Requests > Send All          Ctrl+Shift+Return
Export Single Request                  Requests > Export            Ctrl+E
Export All Requests                    Requests > Export All        Ctrl+Shift+E
Insert Variables                       Requests > Insert Variables  Ctrl+I
New Project                            File > New                   Ctrl+N
Open Project                           File > Open                  Ctrl+O
Save Project                           File > Save                  Ctrl+S
Save as Project                        File > Save As
Configure Settings                     File > Settings
Show Assertion Builder                 Button on Request Form
Show Environment Config                Dialog from toolbar
Show Data Generator                    Menu or Ctrl+I
Show Fuzz Test                         Context menu on request
Show Code Generator                    Requests > Export
Show Import Dialog                     Import > [Format]
Show Project Info                      Project > Info
Show Share Preview                     Button on Response
```

---

## Feature Dependency Matrix

```
                          depends on →
                   ┌──────────┬──────────┬──────────┐
                   │Database  │Signals   │Cache     │
  ┌─────────────┐  │          │          │          │
  │Request CRUD │  │    ✓     │    ✓     │    ✓     │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Assertions   │  │    ✓     │    ✓     │    ✓     │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Environments │  │    ✓     │    ✓     │    ✓     │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Data Gen     │  │          │          │          │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Fuzzing      │  │    ✓     │    ✓     │    ✓     │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Code Gen     │  │          │          │    ✓     │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Import       │  │    ✓     │    ✓     │          │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Sharing      │  │          │          │    ✓     │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Themes       │  │          │          │          │
  ├─────────────┤  ├──────────┼──────────┼──────────┤
  │Mocking      │  │    ✓     │          │    ✓     │
  └─────────────┘  └──────────┴──────────┴──────────┘
```

---

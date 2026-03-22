# HTTP-Rider Architecture Module Map

## 📊 High-Level Subsystems

```
┌─────────────────────────────────────────────────────────────────────┐
│                          UI Layer (PyQt6)                           │
│  MainWindow → Dialogs → Widgets → custom editors/inputs            │
└──────────────────────────────┬──────────────────────────────────────┘
                                │
┌──────────────────────────────▼──────────────────────────────────────┐
│                     Presenters (MVP Pattern)                        │
│  MainPresenter → {RequestPresenter, ExchangePresenter, etc.}       │
└──────────────────────────────┬──────────────────────────────────────┘
                                │
┌──────────────────────────────▼──────────────────────────────────────┐
│              Business Logic & Data Management                       │
│  Interactors → Core (API execution, data generation, state mgmt)   │
│  Exporters → Importers → Codegen                                    │
└──────────────────────────────┬──────────────────────────────────────┘
                                │
┌──────────────────────────────▼──────────────────────────────────────┐
│                    Model & Persistence Layer                        │
│  AppData (data structures) → Storage (SQLite) → External (HTTP)     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔌 Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  EXTERNAL LAYER                                                      │
│  ├── rest_api_connector.py ──► requests.PreparedRequest            │
│  └── requester.py ─────────► HTTP execution                        │
│                                                                       │
│         ▲                                                             │
│         │ (uses)                                                      │
│         │                                                             │
│  CORE LAYER (Business Logic)                                         │
│  ├── api_call_interactor.py ──► ApiCall CRUD                       │
│  ├── app_state_interactor.py ──► AppState management               │
│  ├── safe_rest_api_interactor.py ──► REST execution (wrapper)       │
│  ├── environment_interactor.py ──► Environment variable mgmt        │
│  ├── generators.py ────────────► Faker + Dynamic string generation  │
│  ├── json_data_generator.py ──► JSON schema generation              │
│  └── constants.py ────────────► Enums & constants                   │
│                                                                       │
│         ▲                                                             │
│         │ (uses)                                                      │
│         │                                                             │
│  PRESENTERS (MVP layer - handles UI logic)                          │
│  ├── main_presenter.py ───────► App initialization & lifecycle      │
│  ├── request_presenter.py ────► Request creation/editing UI          │
│  ├── exchange_presenter.py ───► Response rendering                  │
│  ├── api_list_presenter.py ───► List of API calls                   │
│  ├── api_calls_history_presenter.py ──► Execution history           │
│  ├── assertion_builder_presenter.py ──► Test assertion builder      │
│  ├── config_presenter.py ─────► Configuration dialog                │
│  └── [20+ more presenters...] ─► Various UI components              │
│                                                                       │
│         ▲                                                             │
│         │ (uses)                                                      │
│         │                                                             │
│  MODEL LAYER (Data structures & persistence)                        │
│  ├── app_data.py ──────────────► Core data classes (ApiCall, etc.)  │
│  ├── app_data_cache.py ───────► In-memory cache of all data         │
│  ├── app_data_reader.py ───────► SQLite read operations             │
│  ├── app_data_writer.py ───────► SQLite write operations + signals  │
│  ├── storage.py ───────────────► SQLite connection (dataset ORM)    │
│  ├── app_configuration.py ────► AppConfiguration dataclass          │
│  ├── user_data.py ─────────────► UserProject, SavedState            │
│  └── completer.py ────────────► Variable completion model           │
│                                                                       │
│         ▲                                                             │
│         │ (uses)                                                      │
│         │                                                             │
│  UI LAYER (PyQt6 Views)                                              │
│  ├── main_window.py ───────────► MainWindow container               │
│  ├── dialogs/ ──────────────────► Multiple modal dialogs             │
│  ├── widgets/ ──────────────────► Custom UI components              │
│  ├── menus.py ──────────────────► Menu bar configuration            │
│  ├── toolbar.py ─────────────────► Toolbar buttons                  │
│  └── shortcuts.py ────────────────► Keyboard shortcuts              │
│                                                                       │
│         ▲                                                             │
│         │ (uses)                                                      │
│         │                                                             │
│  APPLICATION ENTRY                                                   │
│  └── application.py ───────────► QApplication bootstrap             │
│                                                                       │
│  UTILITY MODULES                                                     │
│  ├── codegen/ ──────────────────► Code generation (Java, Python)    │
│  ├── exporters/ ────────────────► Export to various formats         │
│  ├── importers/ ────────────────► Import from cURL, OpenAPI, etc.   │
│  ├── themes/ ──────────────────► Application themes                 │
│  ├── interactors/ ─────────────► Service interactors (sharing)      │
│  └── core/util_functions.py ──► Utility functions                   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Pathways

### **Path 1: Create & Send API Request**

```
User Creates Request (UI)
         │
         ▼
RequestPresenter.form_to_object()
         │
         ▼
ApiCall object constructed in memory
         │
         ▼
ApiCallInteractor.add_api_call()
         │
         ├──► AppDataWriter.update_api_call_in_db()
         │           │
         │           ▼
         │        Storage (SQLite) ✓
         │
         └──► Emit Signal: signals.api_call_added
                    │
                    ▼
              AppDataCache.on_api_call_added()
                    │
                    ▼
              UI updates (lists, views)
```

### **Path 2: Execute API Call & Display Response**

```
User clicks "Send Request" (UI)
         │
         ▼
RequestPresenter.on_btn_send_request()
         │
         ├──► form_to_object() [update in-memory ApiCall]
         │
         ├──► RestApiConnector.run()
         │           │
         │           ├──► resolve variables (Environment, Faker)
         │           ├──► build PreparedRequest
         │           ├──► execute HTTP request
         │           └──► HttpExchange created
         │
         └──► AppDataWriter.add_http_exchange()
                    │
                    ├──► Storage (SQLite) ✓
                    │
                    ├──► Emit Signal: signals.exchange_added
                    │           │
         ┌──────────┘           ▼
         │               AppDataCache.on_api_http_exchange_added()
         │                       │
         │                       ▼
         │               Cache updated
         │
         └──► ExchangePresenter.refresh()
                    │
                    ▼
              Render HTTP exchange (request + response)
                    │
                    ├──► Display headers, body, status
                    ├──► Run assertions (if any)
                    └──► Update history
```

### **Path 3: Load Project & Cache Data**

```
Application Startup
         │
         ▼
CoreSettings.init()
         │
         ├──► Load user preferences from QSettings
         ├──► Initialize logging
         └──► Load project location
                    │
                    ▼
         AppDataCache.load_cache()
                    │
         ┌──────────┴──────────┬──────────┬──────────┐
         ▼                      ▼          ▼          ▼
    load_api_calls   load_test_cases  load_exchanges load_environments
         │                      │          │          │
         ▼                      ▼          ▼          ▼
    AppDataReader.get_*_from_db()
         │
         ▼
    Storage (SQLite query)
         │
         ▼
    Cache populated in AppDataCache
         │
         ▼
    Emit: initial_cache_loading_completed
         │
         ▼
    UI updates with data
```

### **Path 4: Filter & Search API Calls**

```
User searches/filters (UI)
         │
         ▼
ApListPresenter.filter()
         │
         ├──► AppDataCache.filter_api_calls(query, tag)
         │           │
         │           ▼
         │    Apply filter lambda:
         │    - Match tag (if selected)
         │    - Match search query (in title)
         │
         └──► Return filtered list
                    │
                    ▼
              Update API list view
```

### **Path 5: Save Project & Persist Data**

```
User action (add/update/delete)
         │
         ▼
CoreInteractor updates AppData object
         │
         ▼
AppDataWriter.update_*_in_db()
         │
         ├──► JSONify object
         ├──► Execute SQL upsert to Storage
         └──► Emit signal
                    │
                    ▼
         AppDataCache updates
                    │
                    ▼
         UI auto-refreshes (signal-driven)
```

---

## 📦 Module Interfaces & Key Classes

### **Core Module** (`httprider/core/`)

| Class                        | Responsibility                                          |
| ---------------------------- | ------------------------------------------------------- |
| `ApiCallInteractor`          | CRUD operations for API calls; emits signals            |
| `RestApiConnector` (QThread) | Executes HTTP requests asynchronously; handles fuzzing  |
| `SafeRestApiInteractor`      | Wrapper around RestApiConnector with error handling     |
| `AppStateInteractor`         | Manages selected tag, environment, search state         |
| `EnvironmentInteractor`      | Variable resolution from environments; data replacement |
| `Generators`                 | Dynamic string generation (Faker, regex, functions)     |
| `JsonDataGenerator`          | JSON schema-based fake data generation                  |

### **Model Module** (`httprider/model/`)

| Class                      | Responsibility                                       |
| -------------------------- | ---------------------------------------------------- |
| `ApiCall` (attrs)          | API request definition (URL, headers, body, params)  |
| `ApiTestCase` (attrs)      | Assertions for API response validation               |
| `HttpExchange` (attrs)     | Recorded request ↔ response pair                    |
| `ExchangeRequest` (attrs)  | Actual HTTP request sent to server                   |
| `ExchangeResponse` (attrs) | Actual HTTP response received                        |
| `Environment` (attrs)      | Set of variables (key=value pairs)                   |
| `AppData`                  | Base class for data structures; JSON serialization   |
| `AppDataCache`             | In-memory cache of all entities; filter/search logic |
| `AppDataReader`            | Load from SQLite; signals for async operations       |
| `AppDataWriter`            | Save to SQLite; emits signals for cache updates      |
| `Storage`                  | Raw SQLite connection via dataset ORM                |
| `AppConfiguration`         | App settings (proxy, timeout, TLS, updater)          |
| `CoreSettings`             | Singleton: settings, logging, paths, data layer init |

### **Presenters Module** (`httprider/presenters/`)

| Class                               | Responsibility                                |
| ----------------------------------- | --------------------------------------------- |
| `MainPresenter`                     | App lifecycle, settings, initial load         |
| `RequestPresenter`                  | Request editing form → ApiCall object         |
| `ExchangePresenter`                 | Response rendering (request/response display) |
| `ApiListPresenter`                  | List of API calls; filtering; run all         |
| `AssertionBuilderPresenter`         | Test assertion builder dialog                 |
| `ApiCallsHistoryPresenter`          | Recorded exchange history                     |
| `EnvironmentConfigurationPresenter` | Environment variable editor                   |
| `CodeGeneratorPresenter`            | Code export to Java, Python, etc.             |
| `ImporterPresenter`                 | Import from cURL, OpenAPI, Postman            |

### **UI Module** (`httprider/ui/`)

| Class          | Responsibility                                       |
| -------------- | ---------------------------------------------------- |
| `MainWindow`   | Main QMainWindow container; splitter layout          |
| Dialog classes | Modal windows (configuration, environment, code gen) |
| Widget classes | Custom UI components (auto-complete, tag editor)     |
| `menus.py`     | MenuBar items (File, Edit, Tools)                    |
| `toolbar.py`   | ToolBar buttons and actions                          |
| `shortcuts.py` | Keyboard shortcut bindings                           |

### **External Module** (`httprider/external/`)

| Class              | Responsibility                      |
| ------------------ | ----------------------------------- |
| `RestApiConnector` | HTTP execution; QThread-based async |
| `Requester`        | Prepare & execute HTTP requests     |

### **Utility Modules**

| Module         | Responsibility                                   |
| -------------- | ------------------------------------------------ |
| `codegen/`     | Code generation (Java Feign, Spring Boot, etc.)  |
| `exporters/`   | Export to cURL, Postman, Markdown, OpenAPI, etc. |
| `importers/`   | Import from cURL, OpenAPI, Postman Collections   |
| `themes/`      | Light/dark theme providers                       |
| `interactors/` | Service layer (exchange sharing)                 |

---

## 🎯 Top 10 Most Important Classes

1. **`CoreSettings`** - Singleton managing app configuration, logging, persistence initialization
2. **`AppDataCache`** - In-memory cache providing fast filtering & search
3. **`ApiCallInteractor`** - Core CRUD operations; signal dispatcher
4. **`RestApiConnector`** - HTTP execution engine (QThread-based)
5. **`AppDataWriter`** - Persistence layer; signal emitter for cache updates
6. **`AppDataReader`** - Data loading from SQLite
7. **`MainPresenter`** - Application lifecycle & state restoration
8. **`RequestPresenter`** - Request form handling & validation
9. **`ExchangePresenter`** - Response rendering & assertion evaluation
10. **`ApiCall`** (data class) - Core domain model representing HTTP request

---

## ⚙️ Configuration & Constants

### **Configuration Sources**

| File                         | Purpose                                                                                  |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| `core/constants.py`          | Enums & constants (AssertionDataSource, ContentType, ExchangeRequestType, HTTP statuses) |
| `model/app_configuration.py` | AppConfiguration dataclass (proxy, timeout, TLS, update check)                           |
| `model/user_data.py`         | UserProject, SavedState enum                                                             |
| `core/core_settings.py`      | CoreSettings singleton                                                                   |

### **Key Constants**

```python
# Record types for SQLite
ENVIRONMENT_RECORD_TYPE = "environment"
PROJECT_INFO_RECORD_TYPE = "project_info"
APP_STATE_RECORD_TYPE = "app_state"
HTTP_EXCHANGE_RECORD_TYPE = "http_exchange"
API_TEST_CASE_RECORD_TYPE = "api_test"
API_CALL_RECORD_TYPE = "api"

# Assertion matchers
class AssertionMatchers(Enum):
    EQ, NOT_EQ, CONTAINS, MATCHES, EMPTY, etc.

# Content types & request methods
class ContentType(Enum):
    JSON, XML, FORM, RAW

# Common HTTP headers
COMMON_HEADERS = ["Content-Type", "Accept", "Authorization"]
```

### **Settings Storage**

- **Location**: `~/.config/httprider/httprider.ini` (Linux/Mac), `AppData/...` (Windows)
- **Format**: QSettings INI file
- **What's stored**:
  - Window position/size
  - Last active project
  - Proxy settings
  - Update check preference
  - Timeout settings
  - TLS verification flag

---

## 💾 Storage & Persistence

### **Database Schema (SQLite)**

```
Table: api_call
├── name: "api" (constant)
├── api_call_id: str (UUID)
├── object: json (ApiCall serialized)
└── [indexed on api_call_id]

Table: api_test_case
├── name: "api_test" (constant)
├── api_call_id: str (FK to ApiCall)
├── object: json (ApiTestCase serialized)
└── [indexed on api_call_id]

Table: http_exchange
├── name: "http_exchange" (constant)
├── exchange_id: str (UUID)
├── api_call_id: str (FK to ApiCall)
├── object: json (HttpExchange serialized)
└── [indexed on exchange_id, api_call_id]

Table: environment
├── name: "environment" (constant)
├── env_name: str (unique)
├── object: json (Environment serialized)
└── [indexed on env_name]

Table: project_info
├── name: "project_info" (constant)
├── object: json (ProjectInfo serialized)

Table: app_state
├── name: "app_state" (constant)
├── object: json (AppState serialized)
```

### **Project Structure on Disk**

```
~/Documents/HttpRiderProject/
├── data.db              (SQLite database with all tables)
└── [project metadata]
```

### **Data Loading Flow**

```
Application Start
         │
         ▼
CoreSettings.init() → QSettings loaded from .ini
         │
         ▼
Load project location from QSettings
         │
         ▼
Storage() → dataset.connect() to data.db
         │
         ▼
AppDataReader initialized
AppDataWriter initialized
AppDataCache initialized
         │
         ▼
MainPresenter.after_window_loaded()
         │
         ▼
AppDataCache.load_cache()
  ├── get_all_api_calls_from_db()
  ├── get_api_test_case_from_db() [for each call]
  ├── get_api_call_exchanges_from_db() [for each call]
  └── get_environments_from_db()
         │
         ▼
Cache fully loaded → UI components refresh
```

### **Data Saving Flow**

```
User Action (add/update/delete)
         │
         ▼
CoreInteractor method called
         │
         ▼
AppDataWriter.update_*_in_db()
  ├── Convert to JSON (cattr.unstructure)
  ├── SQLite upsert
  └── Emit signal
         │
         ▼
AppDataCache updates in-memory
         │
         ▼
Presenters/UI auto-refresh (signal-driven)
```

---

## 🔌 Signal Flow (MVP Pattern)

### **Signal Sources** (AppDataWriter, AppDataReader)

```
AppDataWriter.signals:
├── api_call_added(id, call)
├── api_call_removed(ids)
├── api_call_updated(id, call)
├── api_call_tag_added(call, tag)
├── api_call_tag_removed(call, tag)
├── exchange_added(exchange)
├── exchange_changed(id, exchange)
├── environment_added(name)
├── environment_data_changed(name)
├── project_info_updated(info)
└── app_state_updated()

AppDataReader.signals:
├── api_call_change_selection(call)
└── initial_cache_loading_completed()
```

### **Signal Subscribers** (UI Components)

```
MainPresenter
  ├── api_call_added → show_frame()
  └── api_call_removed → show_frame()

RequestPresenter
  ├── api_call_change_selection → refresh()
  ├── exchange_added → on_exchange_added()
  └── environment_data_changed → refresh_completer()

ExchangePresenter
  ├── exchange_added → refresh()
  ├── selected_exchange_changed → on_exchange_changed()
  └── api_call_change_selection → display_last_exchange()

ApiListPresenter
  ├── api_call_added → refresh()
  └── api_call_removed → refresh()

AppDataCache
  ├── [all signals] → on_*() handlers
  └── Updates in-memory state
```

---

## 📋 Entity-Relationship Diagram

```
┌──────────────┐
│  ProjectInfo │ (1 per project)
│──────────────│
│ id, title    │
│ version      │
│ tags[]       │
│ servers[]    │
└──────────────┘
       │
       │ is part of
       │
       ▼
┌──────────────┐      ┌──────────────┐
│   ApiCall    │◄─────│  Environment │
│──────────────│ uses │──────────────│
│ id, title    │ vars │ name, vars[] │
│ http_url     │      │              │
│ http_method  │      └──────────────┘
│ headers[]    │
│ params[]     │
│ tags[]       │      ┌──────────────┐
│ enabled      │◄─────│ ApiTestCase  │
└──────────────┘ has  │──────────────│
       │               │ assertions[] │
       │ produces      │ setup_code   │
       │               │ teardown_code│
       ▼               └──────────────┘
┌──────────────┐
│ HttpExchange │
│──────────────│
│ id           │      ┌──────────────┐
│ request      │────► │ ExchangeReq  │
│ response     │      │──────────────│
│ timestamp    │      │ headers, body│
│ passed?      │      │ query_params │
└──────────────┘      └──────────────┘
       │
       │ recorded          ┌──────────────┐
       └────────────────► │ ExchangeResp │
                          │──────────────│
                          │ status_code  │
                          │ headers, body│
                          │ response_time│
                          └──────────────┘

┌──────────────┐
│  AppState    │
│──────────────│
│ selected_tag │
│ selected_env │
│ search_query │
└──────────────┘
```

---

## 🔄 MVP Pattern Implementation

```
View (UI Layer) ─────────► Presenter ─────────► Model & Data Layer
     │                         │                        │
     │ User action             │ Process logic          │ CRUD
     │ (button click)          │ (business logic)       │ operation
     │                         │                        │
     │◄────────────────────────┼────────────────────────┤
     │                         │                        │
     └─ Display updated        ├─ Format data           ├─ Update
       state via signals       ├─ Validate input       │  cache
                               ├─ Call interactor      │  signal
                               ├─ Refresh view         └─ Emit
                                                        signals
```

### **Example: Request Send**

```
RequestPresenter (Presenter)
├── on_btn_send_request()                      [user action]
├── form_to_object()                           [extract form data]
├── ApiCall object                             [model]
├── RestApiConnector.run()                     [execute]
├── await response                             [async]
└── ExchangePresenter.refresh()                [update view]
    └── update display                         [signal-driven]
```

---

## 🎨 Theme System

- **Location**: `httprider/themes/`
- **Provider**: `ThemeProvider.configure_theme(application)`
- **Supported**: Light & dark themes
- **Applied via**: QApplication stylesheets

---

## 📝 Summary Statistics

- **Total Modules**: ~40
- **Core Interactors**: 4 (API calls, app state, environment, share service)
- **Presenters**: 24+
- **Data Classes**: 12+
- **Exporters**: 13+ formats
- **Importers**: 3 formats
- **UI Dialogs**: 7+
- **Custom Widgets**: 8+

---

## 🔗 Cross-Cutting Concerns

### **Logging**

- Centralized in `CoreSettings.init_logger()`
- Log file: `~/Library/Logs/HttpRider/httprider.log` (macOS)
- Rotating file handler with daily rotation

### **Error Handling**

- `RestApiConnector` catches `RequestsConnectionError`, timeout, SSL errors
- Exceptions propagated via signals
- UI displays error messages in status bar

### **Async Execution**

- `RestApiConnector` extends `QThread`
- Results emitted via signals
- Worker pool in `core/worker_pool.py` for concurrent tasks

### **Data Serialization**

- Uses `cattr` (attrs converter) for type conversion
- JSON serialization for database storage
- All domain models support `.from_json()` / `.to_json()`

### **Variable Resolution**

- Environment variables: `${VAR_NAME}`
- Faker functions: `@faker.first_name()`
- Custom functions: `@function_name()`
- Resolved in `EnvironmentInteractor` before HTTP execution

---

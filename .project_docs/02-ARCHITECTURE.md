# HTTP-Rider System Architecture Document

## Executive Summary

HTTP-Rider is a PyQt6-based REST API testing tool built on a **Signal-Driven MVP Architecture** with a **Hybrid Persistence Model** (in-memory cache + SQLite backend). The design prioritizes:

- **Reactive UI updates** via PyQt signals
- **Data consistency** through event-driven architecture
- **Pluggable extensibility** (exporters/importers)
- **Decoupled testing** through interactor abstraction
- **Single-threaded UI** with async request handling via QThread workers

---

## 1. Architectural Patterns

### 1.1 MVP (Model-View-Presenter) Pattern

HTTP-Rider uses a **layered MVP architecture** with 6 distinct layers:

```
UI Layer (PyQt6 Widgets)
    ↓ (User events)
Presenter Layer (MVP Controllers)
    ↓ (Business logic calls)
Core/Interactor Layer (Orchestrators)
    ↓ (CRUD operations)
Model Layer (Data + Cache)
    ↓ (Persistence)
Storage Layer (SQLite)
    ↓
External Layer (HTTP, Exports, Imports)
```

#### Why MVP?

**Testability**: Presenters are decoupled from PyQt widgets, allowing unit testing without GUI initialization.

**Separation of Concerns**: UI rendering, business logic, and data persistence are isolated.

**Reactive Flow**: Signals flow from storage → cache → presenters → UI, not the reverse.

### Example Flow: Creating a New API Call

```
User types API title in UI
    ↓
RequestPresenter.form_to_object() (reads form data)
    ↓
ApiCallInteractor.add_api_call() (business logic)
    ↓
AppDataWriter.update_api_call_in_db() (persistence)
    ↓
AppDataSignals.api_call_added.emit() (signal broadcast)
    ↓
AppDataCache.on_api_call_added() (cache update)
    ↓
Presenters listen to signals and refresh UI
```

### 1.2 Signal-Driven Reactive Architecture

The entire app is event-driven via **PyQt signals**:

#### Key Signal Sources

```python
# AppDataWriter (persistence events)
class AppDataSignals(QObject):
    api_call_added = pyqtSignal(str, ApiCall)
    api_call_removed = pyqtSignal(list)
    api_call_updated = pyqtSignal(str, ApiCall)
    exchange_added = pyqtSignal(HttpExchange)
    environment_data_changed = pyqtSignal(str)
    # ... 15+ signals total

# AppDataReader (view/query events)
class AppDataReadSignals(QObject):
    api_call_change_selection = pyqtSignal(ApiCall)
    initial_cache_loading_completed = pyqtSignal()

# RestApiConnector (async request events)
class HttpExchangeSignals(QObject):
    request_started = pyqtSignal(str, str)
    request_finished = pyqtSignal(str)
```

#### Why Signals?

1. **Decoupling**: Presenters don't call cache; they listen to signals
2. **Multi-window consistency**: All windows receive the same signals
3. **Undo/filter support**: Cache maintains state independently
4. **Reactive by design**: Changes propagate automatically
5. **Prevents circular dependencies**: DB changes don't directly update UI

### 1.3 Plugin-Based Extensibility (Exporter Pattern)

HTTP-Rider supports **15+ exporters** (Curl, OpenAPI, Postman, Mermaid, etc.) using a simple plugin pattern:

```python
# Base pattern (not explicit interface, but convention)
@attr.s
class ExporterName:
    name: str = "Display Name"
    output_ext: str = "file_extension"

    def export_data(self, api_calls: list[ApiCall]):
        # Transform api_calls to target format
        return formatted_output

# Exporter instantiation
exporter = ExporterName()
```

#### Design Decision: Why attr.s?

- **Simple, immutable-like structure** for stateless exporters
- **Type hints** for clarity
- **No inheritance overhead** - just naming convention
- **Easy to inspect**: name and output_ext are properties, not methods

#### Plugin Discovery

```python
# Loop through exporter modules dynamically
for exporter_module in exporters_directory:
    import exporter_module
    exporter = exporter_module.exporter  # Get singleton instance
    register(exporter)
```

#### Extensibility Example: Adding a New Exporter

To add support for "AWS API Gateway Swagger":

1. Create `exporter_aws_api_gateway.py`
2. Define class with `name`, `output_ext`, `export_data(api_calls)`
3. Instantiate as `exporter = AwsApiGatewayExporter()`
4. Automatic discovery loads it

**No registration code, no factories, no base classes** - just follow the convention.

---

## 2. Core Design Decisions

### 2.1 Hybrid Cache + Database Model

**Architecture Decision**: In-memory cache + SQLite backend (not cache-aside or write-through)

```
User Action
    ↓
Interactor
    ↓
AppDataWriter writes to SQLite
    ↓
Signal emitted
    ↓
AppDataCache updates in-memory copies
    ↓
UI listens to signals and renders
```

#### Why Not Single Database?

1. **SQLite latency**: UI can't block on DB reads/writes
2. **Filtering/search**: Cache enables fast client-side filtering
3. **Undo support**: Cache snapshot enables undo/redo
4. **Multi-tab consistency**: Cache is shared across all views
5. **Startup time**: Load once into cache, serve from memory

#### Cache Strategy

```python
class AppDataCache:
    api_call_list: dict[str, ApiCall] = {}  # All API calls
    api_test_cases: dict[str, ApiTestCase] = {}
    api_http_exchanges: dict[str, list[HttpExchange]] = {}
    environments: dict[str, Environment] = {}
```

- **Load on startup**: `AppDataCache.load_cache()` reads all records once
- **Update on change**: Signal handlers refresh cache items incrementally
- **Filter in memory**: Search queries use Python lambdas, not DB queries
- **No eviction**: All data kept in memory (suitable for local projects)

#### Data Flow Consistency

**Write Path** (ensures DB and Cache always sync):

```
Interactor.update_api_call(api_id, api_call)
    ↓
AppDataWriter.update_api_call_in_db(api_call)  ← DB write first
    ↓
AppDataWriter.signals.api_call_updated.emit(api_id, api_call)  ← Then signal
    ↓
AppDataCache.refresh_cache_item(api_id, api_call)  ← Cache updates last
```

This ordering ensures:

- If signal is received before DB write completes, cache gets stale data (fine, will be refreshed)
- If process crashes after DB write but before signal, cache reloads on restart
- Multi-threaded consistency: signals use PyQt's thread-safe event queue

### 2.2 Why One-Way Data Flow?

```
Interactor → DB → Signal → Cache → Presenter → UI
```

NOT bidirectional:

```
UI ↔ Presenter ↔ Cache  ← ANTI-PATTERN
```

#### Reasons

1. **Single source of truth**: Only the DB is authoritative
2. **Undo/replay**: Can re-emit past signals to replay state
3. **Concurrency safety**: No race conditions on shared state
4. **Testing**: Can test interactors without UI
5. **Consistency**: Both windows loading the same API call get same signal

### 2.3 Thread Safety & Async Patterns

#### PyQt Thread Rule

> Only the main thread can update UI. Background threads can only emit signals.

HTTP-Rider enforces this:

```python
class SafeRestApiInteractor:
    """Singleton: manages HTTP request execution"""

    def make_http_call(self, api_call: ApiCall):
        # Create ApiWorkerData (domain event)
        api_worker_data = ApiWorkerData(
            exchange=exchange,
            on_success=self.__on_success,  ← Slot in main thread
            on_failure=self.__on_failure,   ← Slot in main thread
        )
        self.queue_worker_task(api_worker_data)

    def __process_exchange(self, api_worker_data):
        # Create new QThread (not main thread)
        busy_worker = RestApiConnector(name=random_environment())

        # Connect signals: QThread → main thread's slots
        busy_worker.signals.result.connect(
            api_worker_data.on_success  ← Main thread slot, thread-safe
        )

        busy_worker.start()  ← Runs in QThread, makes HTTP request
```

#### Request Queue Pattern

```python
class SafeRestApiInteractor:
    worker_queue: Queue = Queue()  # Thread-safe queue
    any_worker_running: bool = False

    def queue_worker_task(self, api_worker_data):
        self.worker_queue.put(api_worker_data)
        self.__process_queue()  ← Runs one request at a time

    def __request_finished(self):
        self.any_worker_running = False
        self.__process_queue()  ← Process next queued request
```

**Why a queue?**

- Prevents race conditions if user clicks "Send" multiple times
- Ensures requests execute sequentially (not in parallel)
- Simplifies state management
- Matches user expectation: one active request at a time

### 2.4 AppState & Configuration Persistence

```python
class AppState:
    selected_tag: str | None = None
    selected_env: str | None = None
    selected_search: str | None = None
```

Stored in SQLite, reloaded on app startup. Enables:

- Resume in last position
- Remember selected environment
- Restore search filters

Also persists:

- Window geometry/state
- Proxy settings
- TLS verification flags
- Project location

---

## 3. Module Interaction Patterns

### 3.1 Layer Responsibilities

#### UI Layer (PyQt Widgets)

- Render data
- Capture user input
- Emit user events to presenters

#### Presenter Layer (25+ Presenter Classes)

- Subscribe to signals from core and storage
- Convert form data → domain objects
- Call interactors with business logic
- Update UI based on signal events

Example presenters:

- `RequestPresenter`: API form input/output
- `ApiListPresenter`: List of APIs with filtering
- `ExchangePresenter`: Request/response rendering
- `MainPresenter`: App lifecycle, startup/shutdown

```python
class RequestPresenter:
    def __init__(self, parent_view):
        # Listen to all data changes
        app_settings.app_data_reader.signals.api_call_change_selection.connect(self.refresh)
        app_settings.app_data_writer.signals.api_call_updated.connect(self.on_api_call_refresh)
        app_settings.app_data_writer.signals.exchange_added.connect(self.on_exchange_added)

    def form_to_object(self):
        """Convert form → ApiCall"""
        self.current.title = self.view.txt_api_title.text().strip()
        self.current.http_method = self.view.combo_method.currentText()
        # ... 10+ form fields

    def on_btn_send_request(self):
        """User clicked 'Send' button"""
        self.form_to_object()  # Read form
        rest_api_interactor.make_http_call(self.current)  # Call business logic
        # UI updates via signal chain, not direct calls
```

#### Core Layer (Interactors)

- **ApiCallInteractor**: CRUD for API calls
- **EnvironmentInteractor**: CRUD for environments
- **SafeRestApiInteractor**: Orchestrate HTTP execution
- **ShareServiceInteractor**: Share exchanges

Interactors:

1. Validate input
2. Call persistence layer
3. Emit signals
4. Never directly call UI

```python
class ApiCallInteractor:
    def add_api_call(self, api_call: ApiCall) -> str:
        api_call.id = gen_uuid()

        # Persist to DB
        app_settings.app_data_writer.update_api_call_in_db(api_call)

        # Emit signal - let observers update
        app_settings.app_data_writer.signals.api_call_added.emit(
            api_call.id, api_call
        )

        return api_call.id

    def add_multiple_api_calls(self, api_calls: list[ApiCall]):
        # Suppress signals for each, emit once at end
        doc_ids = [
            self.add_api_call(api_call, suppress_event=True)
            for api_call in api_calls
        ]
        # Batch signal - more efficient
        app_settings.app_data_writer.signals.multiple_api_calls_added.emit(
            doc_ids, api_calls
        )
        return doc_ids
```

#### Model Layer (Data + Cache)

- **AppDataCache**: In-memory snapshot of all data
- **AppDataWriter**: Persist changes + emit signals
- **AppDataReader**: Read from DB
- **Domain Objects**: ApiCall, HttpExchange, Environment, etc.

#### Storage Layer (SQLite via dataset)

- **Storage** class: Wraps dataset library
- **Tables**: api, api_test, http_exchange, environment, project_info, app_state

Schema-less (JSON documents in SQLite):

```python
table.upsert({
    "name": api_call.type,
    "api_call_id": api_call.id,
    "object": json.dumps(api_call.to_json()),  ← Store serialized object
}, ["api_call_id"])
```

#### External Layer

- **RestApiConnector**: QThread-based HTTP executor
- **Requester**: wrapper around `requests` library
- **Exporter modules**: Generate output in various formats
- **Importer modules**: Parse input formats

### 3.2 State Management Across App

```python
# Singleton in CoreSettings
class CoreSettings:
    settings: QSettings = None  ← Platform-aware settings file
    app_data_cache: AppDataCache = None
    app_data_writer: AppDataWriter = None
    app_data_reader: AppDataReader = None

# Global access
app_settings = CoreSettings()
```

All components reference the same `app_settings` singleton:

```python
# In any presenter, interactor, etc.
app_settings.app_data_cache.get_api_call(api_id)
app_settings.app_data_writer.signals.api_call_added.emit(...)
app_settings.load_configuration()
```

### 3.3 Event Flow & Signal Propagation

#### Signal Flow on "Add New API Call"

```
RequestPresenter.save_new_api_call()
    ↓ calls
ApiCallInteractor.add_api_call(api_call)
    ↓ calls
AppDataWriter.update_api_call_in_db(api_call)
    ↓ writes to SQLite
AppDataWriter.signals.api_call_added.emit(api_id, api_call)
    ↓ emits signal to all listeners (main thread)
    ├→ ApiListPresenter.on_api_call_added()  ← Add to list view
    ├→ AppDataCache.on_api_call_added()  ← Update cache
    └→ MainPresenter.show_frame()  ← Show/hide empty state
```

#### Signal Flow on HTTP Response

```
RestApiConnector.run() [QThread]
    ↓ makes HTTP request
    ↓ parseresponce
    ↓
RestApiConnector.signals.result.emit(exchange)  [in QThread]
    ↓ delivers to main thread via Qt event queue
    ↓
SafeRestApiInteractor.__on_success(exchange)  [main thread slot]
    ↓
AppDataWriter.add_http_exchange(exchange)
    ↓
AppDataWriter.signals.exchange_added.emit(exchange)
    ↓
    ├→ ExchangePresenter.on_response_received()  ← Render response
    ├→ AppDataCache.on_api_http_exchange_added()  ← Update cache
    └→ AssertionResultPresenter.evaluate()  ← Run assertions
```

---

## 4. Extensibility & Plugin System

### 4.1 Exporter Architecture

Each exporter is a module following this convention:

```python
# File: httprider/exporters/exporter_curl.py

@attr.s
class CurlExporter:
    name: str = "Curl"
    output_ext: str = "sh"

    def export_data(self, api_calls: list[ApiCall]):
        """Transform API calls to Curl format"""
        output = []
        for api_call in api_calls:
            last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
            curl_command = to_curl(api_call, last_exchange)
            highlighted = highlight(curl_command, BashLexer(), HtmlFormatter())
            output.append(highlighted)
        return "<br/>".join(output)

# Singleton instance for discovery
exporter = CurlExporter()
```

### 4.2 Exporter Discovery & Registration

```python
# In UI, when user selects "Export"
from httprider.exporters import (
    exporter_curl,
    exporter_openapi_v3,
    exporter_markdown,
    # ... auto-importable modules
)

# Build exporter list
exporters = [
    exporter_curl.exporter,
    exporter_openapi_v3.exporter,
    exporter_markdown.exporter,
    # ...
]

# User selects one
selected_exporter = exporters[user_selection_index]

# Generate output
output = selected_exporter.export_data(api_calls)
```

### 4.3 Why This Design?

✅ **Easy to add**: Just create a new module with `export_data()` method

✅ **No factory pattern**: Direct module imports are simpler

✅ **Type hints work**: IDE autocomplete works naturally

✅ **Decoupled**: Exporters don't share state

❌ **No auto-discovery**: Must manually import (trade-off)

### 4.4 Importer Architecture

Similar pattern for importers:

```python
@attr.s
class CurlImporter:
    name: str = "Curl"
    match_extensions: list[str] = attr.Factory(lambda: [".sh", ".curl"])

    def import_data(self, content: str) -> list[ApiCall]:
        """Parse Curl format → ApiCall objects"""
        api_calls = []
        # Parse logic
        return api_calls

importer = CurlImporter()
```

Discovered by file extension or manually selected.

---

## 5. Testing Architecture

### 5.1 GUI Decoupling via Signals & Interactors

Challenge: **PyQt widgets can't be instantiated without QApplication**

Solution: **Test interactors and presenters independently**

#### Unit Test Example: Testing ApiCallInteractor

```python
# No QApplication needed - tests pure logic
def test_add_api_call():
    # Setup
    app_settings.init()  # Initialize singletons
    api_call = ApiCall(title="Test API", http_url="https://api.example.com")

    # Act
    api_id = api_call_interactor.add_api_call(api_call)

    # Assert
    assert api_id is not None
    cached_call = app_settings.app_data_cache.get_api_call(api_id)
    assert cached_call.title == "Test API"

    # Verify signal was emitted
    # (Can mock signals or inspect cache)
```

#### UI Test Example: Testing RequestPresenter

```python
# Requires QApplication but not full main window
def test_form_to_object(qtbot):
    # Setup
    view = create_minimal_view()  # Lightweight form
    presenter = RequestPresenter(view)
    presenter.current = ApiCall()

    # Simulate user input
    view.txt_api_title.setText("My API")
    view.combo_method.setCurrentText("GET")

    # Act
    presenter.form_to_object()

    # Assert
    assert presenter.current.title == "My API"
    assert presenter.current.http_method == "GET"
```

### 5.2 Test Data Setup Patterns

#### Pattern 1: Direct Cache Population

```python
# For testing cache behavior
api_call = ApiCall(id="test1", title="Test", http_url="https://example.com")
app_settings.app_data_cache.api_call_list["test1"] = api_call
```

#### Pattern 2: Through Interactor

```python
# For testing full flow including DB
api_call = ApiCall(title="Test", http_url="https://example.com")
api_id = api_call_interactor.add_api_call(api_call)
# Check both DB and cache updated
```

#### Pattern 3: Mocking Signals

```python
# Verify UI updates on signal
with mock.patch.object(
    app_settings.app_data_writer.signals,
    'api_call_added'
) as mock_signal:
    api_call_interactor.add_api_call(api_call)
    mock_signal.emit.assert_called_once()
```

### 5.3 E2E Testing Notes

**httpbrider does not have built-in UITests**, but would follow:

1. **Record API calls** via UI
2. **Export to Postman/curl/etc.**
3. **Execute external tools** to verify export
4. **Check generated code** compiles

---

## 6. Configuration & Constants

### 6.1 CoreSettings Singleton Pattern

```python
class CoreSettings:
    """Singleton: Initialized once at app startup"""

    def init(self):
        """Platform-aware initialization"""
        self.app_name = QApplication.instance().applicationName().lower()

        # Platform detection
        if platform.system() == "Darwin":
            self.logs_dir = Path.home() / "Library" / "Logs" / app_name
        elif platform.system() == "Windows":
            self.logs_dir = QStandardPaths(...) / "logs"
        else:  # Linux
            self.logs_dir = Path.home() / ".local" / "share" / app_name / "logs"

        # Initialize QSettings (standard location per platform)
        settings_file = f"{self.app_name}.ini"
        self.settings = QSettings(self.app_dir / settings_file, QSettings.Format.IniFormat)

    def init_logger(self):
        """Rotate logs, capture warnings"""
        handlers = [
            logging.handlers.RotatingFileHandler(
                self.logs_dir / "httprider.log",
                maxBytes=1_000_000,
                backupCount=5,
            ),
            logging.StreamHandler(),
        ]
        logging.basicConfig(handlers=handlers, ...)

    def init_app_data(self):
        """Initialize DB and cache layers"""
        # Create DB tables
        storage = Storage(db_location=self.app_dir / "data.db")

        # Create reader/writer/cache
        self.app_data_reader = AppDataReader(storage.db)
        self.app_data_writer = AppDataWriter(storage.db)
        self.app_data_cache = AppDataCache(self.app_data_reader, self.app_data_writer)

# Global singleton
app_settings = CoreSettings()
```

### 6.2 Constants & Enums

```python
# constants.py organized by type

# Record types (database tables)
ENVIRONMENT_RECORD_TYPE = "environment"
PROJECT_INFO_RECORD_TYPE = "project_info"
API_CALL_RECORD_TYPE = "api"
HTTP_EXCHANGE_RECORD_TYPE = "http_exchange"
API_TEST_CASE_RECORD_TYPE = "api_test"

# Assertion matching operators
class AssertionMatchers(Enum):
    EQ = "equalTo"
    NOT_EQ = "notEqualTo"
    CONTAINS = "containsString"
    MATCHES = "matches"
    GT = "greaterThan"
    LT = "lessThan"

# Content type detection
class ContentType(Enum):
    JSON = "application/json"
    XML = "application/xml"
    FORM = "application/x-www-form-urlencoded"

# Response status during execution
class ExchangeResponseStatus(Enum):
    NONE = auto()
    PASSED = auto()
    FAILED = auto()
```

### 6.3 Settings Persistence

```python
# QSettings stores key-value pairs in platform-native format
# macOS: ~/Library/Preferences/com.httprider.httprider.plist
# Windows: HKEY_CURRENT_USER\Software\httprider\httprider
# Linux: ~/.config/httprider/httprider.conf

# Reading settings
window_state = app_settings.settings.value("windowState")
geometry = app_settings.settings.value("geometry")
proxy = app_settings.settings.value("httpProxy")

# Writing settings
app_settings.settings.setValue("windowState", self.view.saveState())
app_settings.settings.sync()  # Force write to disk
```

---

## 7. Performance Considerations

### 7.1 Async Request Handling

**Challenge**: HTTP requests can take seconds; would freeze UI if on main thread

**Solution**: QThread-based worker pool

```python
class RestApiConnector(QThread):
    """Runs in background thread, communicates via signals"""

    def run(self):
        """Overridden by QThread to run in separate thread"""
        # Make HTTP request (blocking but in background)
        response = self.requester.make_request(...)

        # Emit signal to main thread (thread-safe)
        self.signals.result.emit(exchange)

    def make_http_call(self):
        # Main thread code that starts the worker
        self.exchange = exchange
        self.start()  ← Spawns new thread, calls run()
```

### 7.2 Request Queuing

```python
class SafeRestApiInteractor:
    """Prevents race conditions, ensures sequential execution"""
    worker_queue: Queue = Queue()
    any_worker_running: bool = False

    def queue_worker_task(self, api_worker_data):
        self.worker_queue.put(api_worker_data)  # Thread-safe queue
        self.__process_queue()

    def __process_queue(self):
        if self.any_worker_running:
            return  # Worker still busy

        if not self.worker_queue.empty():
            # Dequeue and execute next
            task = self.worker_queue.get()
            self.__process_exchange(task)  # Starts new thread
            self.any_worker_running = True
```

**Result**: Users see "Request in progress..." feedback; multiple clicks don't cause race conditions.

### 7.3 Caching Strategy

```python
class AppDataCache:
    """All-in-memory cache, no eviction policy"""

    def load_cache(self):
        # Startup: Read entire DB once
        self.api_call_list = self.app_data_reader.get_all_api_calls_from_db()
        self.api_http_exchanges = self.app_data_reader.get_all_exchanges_from_db()
        # ~10-50ms for typical projects

    def get_api_call(self, api_id):
        return self.api_call_list.get(api_id)  # O(1) lookup

    def filter_api_calls(self, query=None, tag=None):
        # Filter in memory via lambda
        return filter(self._build_filter_query(query, tag), self.api_call_list.values())
```

**Performance benefit**: Search/filter is instant (no DB queries)

**Trade-off**: Limited to projects that fit in RAM (~1000 API calls = ~50MB)

### 7.4 Signal Batching

```python
def add_multiple_api_calls(self, api_calls: list[ApiCall]) -> list[str]:
    if not api_calls:
        return []

    # Add each call but suppress signals
    doc_ids = [
        self.add_api_call(api_call, suppress_event=True)
        for api_call in api_calls
    ]

    # Emit once for all
    app_settings.app_data_writer.signals.multiple_api_calls_added.emit(
        doc_ids, api_calls
    )

    return doc_ids
```

**Why**: If importing 100 APIs, emitting 100 signals would trigger 100 list updates (slow).
Batch signal allows UI to update once with all 100 items.

### 7.5 Database Optimization

```python
# schema-less JSON storage in SQLite
# All fields stored as serialized object, except queried columns

table.upsert({
    "name": api_call.type,  ← Indexed for lookups
    "api_call_id": api_call.id,  ← Indexed for lookups
    "object": json.dumps(api_call.to_json()),  ← Blob
}, ["api_call_id"])

# Queries (indexed)
find(name=API_CALL_RECORD_TYPE)  ← Uses index
find_one(api_call_id=api_id)  ← Uses index
```

**Benefits**: Flexible schema (any API call can have custom fields)

**Downside**: Can't query nested JSON properties directly; must load into Python

---

## 8. Error Handling & Resilience

### 8.1 Exception Handling Patterns

#### Network Errors

```python
class RestApiConnector(QThread):
    def make_http_call(self):
        try:
            response = self.requester.make_request(...)
        except ConnectionError as e:
            # Network error: Connection refused, timeout, etc.
            self.exchange.response = ExchangeResponse(
                http_status_code=-1,
                response_body=str(e)
            )
            self.exchange.failed()
        except RequestException as e:
            # Other request errors
            self.exchange.response = ExchangeResponse(
                http_status_code=-1,
                response_body=str(e)
            )
            self.exchange.failed()
```

**Result**: HTTP status -1 indicates network error (not HTTP error)

#### Graceful Degradation

```python
class AppDataReader:
    def get_api_call_from_db(self, api_call_id):
        try:
            table = self.ldb[API_CALL_RECORD_TYPE]
            obj_db = table.find_one(api_call_id=api_call_id)
            return ApiCall.from_json(json.loads(obj_db["object"]))
        except (KeyError, json.JSONDecodeError):
            # Missing record or corrupt JSON
            return ApiCall.from_json()  # Return empty object
```

### 8.2 Error Display to User

#### Via Signals (Typed Feedback)

```python
class ExchangePresenter:
    def __init__(self):
        # On success
        rest_api_interactor.signals.result.connect(self.on_response_ok)

        # On failure
        rest_api_interactor.signals.error.connect(self.on_response_error)

    def on_response_error(self, exchange):
        error_message = f"Request failed: {exchange.response.response_body}"
        self.view.status_bar.showMessage(error_message, duration=5000)

        # Also render error in response panel
        self.view.txt_response_body.setText(exchange.response.response_body)
        self.view.txt_response_code.setText(str(exchange.response.http_status_code))
```

#### Connection Errors

```python
# If HTTP status = -1, likely a network error
if exchange.response.http_status_code == -1:
    error_detail = exchange.response.response_body
    # e.g., "Connection refused: Unable to connect to 127.0.0.1:9999"
    user_message = f"Network error: {error_detail}"
```

### 8.3 Recovery Mechanisms

#### State Restoration on Startup

```python
class MainPresenter:
    def refresh_app(self):
        # Load all data from DB
        app_settings.app_data_cache.load_cache()

        # Restore window state
        if app_settings.geometry():
            self.view.restoreGeometry(app_settings.geometry())

        # Restore selected project
        current_project = app_settings.load_current_project()

        # Result: App state fully recovered from last session
```

#### Transaction Safety (via SQLite)

```python
# All writes via AppDataWriter use upsert
table.upsert({...}, ["api_call_id"])

# SQLite upsert is atomic - either commits fully or rolls back
# No partial writes leaving DB in inconsistent state
```

---

## 9. Domain Model & Data Types

### 9.1 Core Domain Objects

```python
@attr.s(auto_attribs=True)
class ApiCall:
    """Single REST API request definition"""
    id: str
    title: str
    description: str
    http_url: str
    http_method: str
    http_headers: dict[str, DynamicStringData]  # Key-value with dynamic values
    http_params: dict[str, DynamicStringData]   # Query parameters
    form_params: dict[str, DynamicStringData]   # Form data
    http_request_body: str
    tags: list[str]
    enabled: bool
    mocked_response: MockedResponse  # For offline testing
    # ... more fields

@attr.s(auto_attribs=True)
class HttpExchange:
    """Single request-response pair (history)"""
    id: str
    api_call_id: str  # Link to ApiCall
    request: ExchangeRequest
    response: ExchangeResponse
    timestamp: datetime

@attr.s(auto_attribs=True)
class ExchangeRequest:
    """Actual request sent (with variable substitution)"""
    http_method: str
    http_url: str
    full_encoded_url: str  # After variable interpolation
    headers: dict
    query_params: dict
    request_body: str
    request_body_type: ContentType

@attr.s(auto_attribs=True)
class ExchangeResponse:
    """Actual response received"""
    http_status_code: int
    response_body: str
    response_headers: dict
    elapsed_time: timedelta
    is_mocked: bool

@attr.s(auto_attribs=True)
class ApiTestCase:
    """Assertions against expected behavior"""
    id: str
    api_call_id: str
    assertions: list[Assertion]

@attr.s(auto_attribs=True)
class Assertion:
    """Single assertion: extract value → match expected"""
    data_from: AssertionDataSource  # "response_body", "response_code", etc.
    selector: str  # JSONPath, XPath, etc.
    matcher: AssertionMatchers  # EQ, CONTAINS, GT, etc.
    expected_value: Any
    result: bool | None  # True/False after evaluation
```

### 9.2 Dynamic String Data (Environment Variables)

```python
@attr.s(auto_attribs=True)
class DynamicStringData:
    """String that may contain ${{VAR}} references"""
    label: str = ""
    value: str = ""
    description: str = ""
    is_enabled: bool = True
    value_type: DynamicValueType = DynamicValueType.STRING

    def display_value(self) -> str:
        """Show **** for secrets"""
        return "****" if self.value_type == DynamicValueType.SECRET else self.value
```

**Use Case**: Headers can reference environment variables

```
Name: Authorization
Value: ${{AUTH_TOKEN}}
Environment:
  AUTH_TOKEN = "Bearer abc123"
```

---

## 10. Key Design Decisions Table

| Decision                   | Why                                  | Trade-offs                    |
| -------------------------- | ------------------------------------ | ----------------------------- |
| **MVP Pattern**            | Separation of concerns, testability  | More boilerplate than MVC     |
| **Signal-driven**          | Decoupling, multi-window consistency | Signal debugging harder       |
| **In-memory cache**        | Fast search/filter                   | Limited to ~50MB projects     |
| **SQLite backend**         | Persistence, cross-session           | Schema migrations needed      |
| **QThread workers**        | Non-blocking UI                      | Threading complexity          |
| **Request queue**          | Sequential execution, race-free      | No parallel requests          |
| **Plugin convention**      | Simple, no factory pattern           | No auto-discovery             |
| **Schema-less JSON**       | Flexible API call fields             | Can't query nested JSON       |
| **Singleton CoreSettings** | Global state access                  | Less testable, harder to mock |
| **AppState in DB**         | Resume session state                 | More DB round-trips           |

---

## 11. Best Practices & Anti-Patterns

### ✅ DO:

1. **Always emit signals after DB writes**

   ```python
   app_data_writer.update_api_call_in_db(api_call)
   app_data_writer.signals.api_call_updated.emit(api_call.id, api_call)
   ```

2. **Let signals drive UI updates**

   ```python
   # Not: presenter.refresh_list()
   # Yes: signal triggers presenter.refresh_list() automatically
   ```

3. **Use batch signals for bulk operations**

   ```python
   # For importing 100 APIs, emit 1 "multiple_added" signal, not 100 "added"
   ```

4. **Keep Interactors focused on single responsibility**

   ```python
   # Not: ApiCallInteractor does API calls + environments
   # Yes: ApiCallInteractor for APIs, EnvironmentInteractor for envs
   ```

5. **Use `suppress_event=True` when internal to interactor**
   ```python
   for api_call in api_calls:
       self.add_api_call(api_call, suppress_event=True)  # No signal noise
   app_data_writer.signals.multiple_api_calls_added.emit(...)  # One signal
   ```

### ❌ DON'T:

1. **Direct UI calls from interactors**

   ```python
   # Not: api_call_interactor.on_success = lambda: view.refresh()
   # Yes: Emit signal, presenter listens and calls view.refresh()
   ```

2. **Circular dependencies between cache and writer**

   ```python
   # Not: Cache calls writer, writer calls cache
   # Yes: Writer emits signal, cache listens
   ```

3. **Mount threading on UI event handlers**

   ```python
   # Not: def on_button_click(): thread = Thread(...); thread.start()
   # Yes: Queue task, SafeRestApiInteractor manages thread lifecycle
   ```

4. **Assume QSettings persistence without sync()**

   ```python
   # Not: settings.setValue(...); return  # May not write to disk
   # Yes: settings.setValue(...); settings.sync()
   ```

5. **Keep uncommitted DB writes in-memory**
   ```python
   # Not: cache[id] = new_item  # Update cache first, write to DB later
   # Yes: Write to DB first, then signal cache to update
   ```

---

## 12. Conclusion

HTTP-Rider's architecture successfully balances:

- **Simplicity** for fast development
- **Testability** through signal-driven decoupling
- **Extensibility** via plugin conventions
- **Performance** with in-memory caching and batch signals
- **Reliability** through one-way data flow and atomic persistence

The signal-driven MVP pattern enables **reactive UI updates without tight coupling**, making the codebase maintainable despite PyQt's complexity. The hybrid cache + database model solves the latency problem of direct SQLite access while enabling localStorage-like functionality.

For future developers adding features:

1. Data changes → Interactor (business logic)
2. Interactor → Database (persistence)
3. Database → Signal (notification)
4. Signal → Cache (in-memory update)
5. Cache → UI (reactive rendering)

Never skip steps; never reverse direction.

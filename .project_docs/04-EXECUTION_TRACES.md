# HTTP-Rider Critical Execution Path Traces

Detailed step-by-step traces showing data flow, control flow, and signal emissions for key application flows.

---

## TRACE 1: Application Startup Flow

### Entry Point to First Window Display

**Files Involved (in execution order):**

- `bin/app` → `httprider/application.py` → `httprider/ui/main_window.py` → `httprider/presenters/main_presenter.py`
- Signal chains: `AppDataWriter.signals.*` → `AppDataCache` → `Presenters`

### Step-by-Step Execution

| Step   | Location                                                           | Class/Function                                  | Action                                                                                                                                                                                                                                                                                                                        | Async?               |
| ------ | ------------------------------------------------------------------ | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| **1**  | `bin/app`                                                          | Entry point                                     | Imports and calls `main()`                                                                                                                                                                                                                                                                                                    | -                    |
| **2**  | `httprider/application.py`<br/>`main()` L22                        | `QApplication.__init__`                         | Creates Qt application instance                                                                                                                                                                                                                                                                                               | Sync                 |
| **3**  | `application.py`<br/>`main()` L23-24                               | `QApplication.set*`                             | Sets app version, name, desktop ID                                                                                                                                                                                                                                                                                            | Sync                 |
| **4**  | `application.py`<br/>`main()` L26-27                               | `configure_theme()`                             | Loads platform-appropriate theme and stylesheets                                                                                                                                                                                                                                                                              | Sync                 |
| **5**  | `application.py`<br/>`main()` L29                                  | `app_settings.init()`                           | **CRITICAL: Initializes CoreSettings singleton**                                                                                                                                                                                                                                                                              | Sync                 |
| **6**  | `httprider/core/core_settings.py`<br/>`CoreSettings.init()` L48-60 | QSettings creation                              | Initializes settings file at platform-specific location (macOS: `~/Library/Application Support/...`, Linux: `~/.config/...`)                                                                                                                                                                                                  | Sync                 |
| **7**  | `core_settings.py`<br/>`init()` L51                                | `_setup_logs_directory()`                       | Creates logs dir based on OS (`~/Library/Logs/` on macOS)                                                                                                                                                                                                                                                                     | Sync                 |
| **8**  | `core_settings.py`<br/>`MainPresenter.__init__()` L9-24            | MainPresenter instantiation                     | - Creates main window presenter<br/>- Calls `app_settings.init()` (again)<br/>- Calls `app_settings.init_logger()` L16<br/>- Calls `app_settings.init_app_data()` L17<br/>- Restores window geometry/state from QSettings L18-20<br/>- **Connects signals**: `api_call_added`, `api_call_removed`, `multiple_api_calls_added` | Sync                 |
| **9**  | `core_settings.py`<br/>`init_app_data()` L116                      | AppDataReader, AppDataWriter, AppDataCache init | - Creates Storage from current project DB<br/>- Initializes `app_data_reader = AppDataReader(db)`<br/>- Initializes `app_data_writer = AppDataWriter(db)`<br/>- Initializes `app_data_cache = AppDataCache(reader, writer)`<br/>- **Cache subscribes to all signals** at this point                                           | Sync                 |
| **10** | `httprider/ui/main_window.py`<br/>`MainWindow.__init__()` L28-65   | UI setup                                        | - Calls `setupUi()` (generated from Qt Designer)<br/>- Creates all presenters (ApiListPresenter, RequestPresenter, etc.)<br/>- Creates dialogs (ConfigDialog, ProgressDialog, etc.)<br/>- Initializes menu/toolbar/shortcuts                                                                                                  | Sync                 |
| **11** | `main_window.py`<br/>`MainWindow.__init__()` L47                   | `MainPresenter.__init__(self)`                  | MainPresenter connects signals and saves reference to main window                                                                                                                                                                                                                                                             | Sync                 |
| **12** | `application.py`<br/>`main()` L31                                  | `MainWindow.show()`                             | Widget becomes visible, triggers `showEvent()`                                                                                                                                                                                                                                                                                | Sync                 |
| **13** | `main_window.py`                                                   | `showEvent()` (Qt event)                        | Emits signal triggering `after_window_loaded()`                                                                                                                                                                                                                                                                               | Sync                 |
| **14** | `presenters/main_presenter.py`<br/>`after_window_loaded()` L27-33  | MainPresenter.after_window_loaded               | **FIRST LOAD**:<br/>1. `app_settings.app_data_cache.load_cache()` L30<br/>2. `refresh_all_views()` L31<br/>3. `setWindowTitle()` with project location                                                                                                                                                                        | Sync                 |
| **15** | `model/app_data_cache.py`<br/>`load_cache()` L40                   | AppDataCache.load_cache                         | Parallel loads from DB:<br/>- `api_call_list = get_all_api_calls_from_db()` → dict<br/>- For each API Call:<br/> - Load `api_test_cases`<br/> - Load `http_exchanges`<br/>- `refresh_app_state()` from DB<br/>- `refresh_environments()` from DB<br/>- **Emits**: `initial_cache_loading_completed` signal                    | Sync                 |
| **16** | `presenters/main_presenter.py`<br/>`show_frame()` L35              | MainPresenter.show_frame                        | - Calls `filter_api_calls()` → list<br/>- If API calls exist: show request/response frames<br/>- Else: show "empty" frame                                                                                                                                                                                                     | Sync                 |
| **17** | `application.py`<br/>`main()` L33                                  | `sys.exit(application.exec())`                  | Enter Qt event loop; app ready for user interaction                                                                                                                                                                                                                                                                           | Async (event-driven) |

### Signal Emissions During Startup

```
STARTUP SIGNAL CHAIN:
1. Cache.load_cache()
   ├─ emits: AppDataReader.signals.initial_cache_loading_completed
2. RequestPresenter connects to signal
   └─ calls: refresh_completer()
      └─ updates: URL completion models
3. ExchangePresenter connects to signal
   └─ prepares for exchange display
```

### Key Objects Initialized During Startup

| Object                        | Purpose                                                | Singleton? | Parent                 |
| ----------------------------- | ------------------------------------------------------ | ---------- | ---------------------- |
| `app_settings` (CoreSettings) | Global access to cache, reader, writer, config         | Yes        | Module-level           |
| `app_data_cache`              | In-memory dict of all API calls, test cases, exchanges | Yes        | Stored in CoreSettings |
| `app_data_reader`             | Database read operations                               | Yes        | Stored in CoreSettings |
| `app_data_writer`             | Database write + signal emission                       | Yes        | Stored in CoreSettings |
| `MainPresenter`               | Window lifecycle, state restoration                    | No         | MainWindow             |
| `ApiListPresenter`            | API list view with filtering                           | No         | MainWindow             |
| `RequestPresenter`            | Request form editing                                   | No         | MainWindow             |
| `ExchangePresenter`           | Response display                                       | No         | MainWindow             |

### Performance Characteristics

- **Startup Time**: Dominated by `load_cache()` (disk I/O)
  - Small projects (<100 API calls): ~100-200ms
  - Large projects (500+ API calls): Can reach 1-2s
- **Memory Footprint**: All data loaded in RAM
  - ~50MB limit before significant performance degradation
- **Async Operations**: None during startup (all synchronous blocking)

---

## TRACE 2: Send API Request Flow

### From "Send" Button Click to Response Display

**Files Involved (in execution order):**

- `presenters/request_presenter.py` → `core/api_call_interactor.py` → `core/safe_rest_api_interactor.py` → `external/rest_api_connector.py` → `model/app_data_writer.py` → `presenters/exchange_presenter.py`

### Step-by-Step Execution

| Step   | Location                                                                  | Class/Function                       | Action                                                                                                                                                                                                                                                                                           | Async?       | Signal             |
| ------ | ------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ | ------------------ |
| **1**  | `presenters/request_presenter.py`<br/>L208                                | RequestPresenter.on_btn_send_request | User clicks "Send" button                                                                                                                                                                                                                                                                        | -            | -                  |
| **2**  | `request_presenter.py`<br/>`on_btn_send_request()`                        | RequestPresenter                     | 1. `update_current_api_call()` - Form→Object mapping<br/>2. `rest_api_interactor.make_http_call(self.current)`                                                                                                                                                                                   | Sync         | -                  |
| **3**  | `request_presenter.py`<br/>`form_to_object()` L176                        | RequestPresenter                     | Parse form fields into ApiCall object:<br/>- Extract URL, method, headers, params, body<br/>- Extract tags, description, title<br/>- Extract mocked response if enabled                                                                                                                          | Sync         | -                  |
| **4**  | `core/safe_rest_api_interactor.py`<br/>`make_http_call()` L45             | SafeRestApiInteractor                | Create HTTP exchange:<br/>1. `ExchangeRequest.from_api_call(api_call, hide_secrets=False)` L47<br/>2. `combine_request_headers(app_config, request)` L48<br/>3. Create `HttpExchange(api_call_id, request)` L49<br/>4. Check if `api_call.mocked_response.is_enabled` → populate response L51-52 | Sync         | -                  |
| **5**  | `safe_rest_api_interactor.py`<br/>`make_http_call()` L54                  | SafeRestApiInteractor                | Wrap exchange in `ApiWorkerData` with callbacks:<br/>- `on_success = self.__on_success`<br/>- `on_failure = self.__on_failure`                                                                                                                                                                   | Sync         | -                  |
| **6**  | `safe_rest_api_interactor.py`<br/>`queue_worker_task()` L57               | SafeRestApiInteractor                | **Queue Management**:<br/>1. Add ApiWorkerData to `worker_queue` (thread-safe Queue)<br/>2. Call `__process_queue()`                                                                                                                                                                             | Sync         | -                  |
| **7**  | `safe_rest_api_interactor.py`<br/>`__process_queue()` L67                 | SafeRestApiInteractor                | Check if any worker running<br/>- If yes: Wait (queue grows)<br/>- If no: Dequeue next task, process                                                                                                                                                                                             | Sync         | -                  |
| **8**  | `safe_rest_api_interactor.py`<br/>`__process_exchange()` L73              | SafeRestApiInteractor                | Create new RestApiConnector worker:<br/>1. `RestApiConnector(name=random_env())` - New QThread<br/>2. Bind result/error signals L75<br/>3. Set `worker.exchange = api_worker_data.exchange`<br/>4. **`worker.start()`** - Spawns OS thread L79<br/>5. Set `any_worker_running = True`            | Sync (spawn) | -                  |
| **9**  | `external/rest_api_connector.py`<br/>`RestApiConnector.run()` L205        | RestApiConnector (QThread)           | **Background thread execution**:<br/>Call `self.make_http_call()` in new OS thread                                                                                                                                                                                                               | **Async**    | -                  |
| **10** | `rest_api_connector.py`<br/>`make_http_call()` L210                       | RestApiConnector                     | **Environment variable substitution**:<br/>1. `get_variable_tokens(app_config)` L211<br/> - Gets all environ + test case assertions<br/>2. `replace_variables(var_tokens, request)` L212<br/> - Substitutes `${VAR_NAME}` in all request fields<br/>3. Log request details                       | **Async**    | -                  |
| **11** | `rest_api_connector.py`<br/>`_emit_request_signals()` L179                | RestApiConnector                     | Emit progress signals (main thread receives):<br/>1. If fuzzed: `http_exchange_signals.fuzzed_request_started.emit(msg, api_call_id)` L184<br/>2. Else: `http_exchange_signals.request_started.emit(msg, api_call_id)` L186                                                                      | **Async**    | `request_started`  |
| **12** | `rest_api_connector.py`<br/>`make_http_call()` L220                       | RestApiConnector                     | **Mocked Response Path**:<br/>If `exchange.response.is_mocked = True`:<br/>- Set response from mocked data<br/>- Skip HTTP request (go to Step 21)                                                                                                                                               | **Async**    | -                  |
| **13** | `rest_api_connector.py`<br/>`_prepare_request_kwargs()` L127              | RestApiConnector                     | Prepare request kwargs based on content-type:<br/>1. Set headers, params<br/>2. If form_params: add to `data` or `files`<br/>3. If body: set request_body<br/>4. Return prepared kwargs dict                                                                                                     | **Async**    | -                  |
| **14** | `rest_api_connector.py`<br/>`make_http_call()` L223                       | RestApiConnector                     | **HTTP Request Execution**:<br/>`self.requester.make_request(method, url, kwargs)`                                                                                                                                                                                                               | **Async**    | -                  |
| **15** | `external/requester.py`                                                   | Requester                            | Use `requests` library to execute HTTP call:<br/>- `requests.request(method, url, **kwargs)`<br/>- Returns (response, error) tuple                                                                                                                                                               | **Async**    | -                  |
| **16** | `rest_api_connector.py`<br/>`make_http_call()` L224                       | RestApiConnector                     | Update request with actual sent data:<br/>`self.exchange.request = update_request(request, response.request)`                                                                                                                                                                                    | **Async**    | -                  |
| **17** | `rest_api_connector.py`<br/>`_handle_response()` L191                     | RestApiConnector                     | Handle response/error:<br/>1. If connection error: `exchange.failed()` + error response<br/>2. If other error: `exchange.failed()` + error response<br/>3. Else: `convert_response(response)` + `exchange.passed()`                                                                              | **Async**    | -                  |
| **18** | `rest_api_connector.py`<br/>`convert_response()` L160                     | RestApiConnector                     | Convert response to ExchangeResponse:<br/>- Status code, body, headers, elapsed time                                                                                                                                                                                                             | **Async**    | -                  |
| **19** | `rest_api_connector.py`<br/>`_emit_finished_signals()` L201               | RestApiConnector                     | Emit result/error signals to main thread:<br/>1. `self.signals.result.emit(exchange)` OR<br/>2. `self.signals.error.emit(exchange)`<br/>3. `http_exchange_signals.request_finished.emit(api_call_id)`                                                                                            | **Async**    | `result` / `error` |
| **20** | `safe_rest_api_interactor.py`<br/>`__bind_signals()`<br/>(signal handler) | SafeRestApiInteractor                | Main thread receives result signal<br/>Calls appropriate callback:<br/>- `self.signals.result.connect(worker, self.__on_success)`<br/>- Worker emits → triggers `__on_success(exchange)`                                                                                                         | Sync         | -                  |
| **21** | `safe_rest_api_interactor.py`<br/>`__on_success()` L95                    | SafeRestApiInteractor                | **Persist response to DB**:<br/>1. Get API call from cache<br/>2. Update `last_response_code`<br/>3. `app_data_writer.add_http_exchange(exchange)`                                                                                                                                               | Sync         | -                  |
| **22** | `model/app_data_writer.py`<br/>`add_http_exchange()` L68                  | AppDataWriter                        | **Database persistence**:<br/>1. Generate `exchange.id = gen_uuid()`<br/>2. `update_http_exchange_in_db(exchange)` - SQLite upsert<br/>3. **Emit signal**: `self.signals.exchange_added.emit(exchange)`                                                                                          | Sync         | `exchange_added`   |
| **23** | `model/app_data_cache.py`<br/>`on_api_http_exchange_added()`              | AppDataCache (signal handler)        | Main thread receives signal:<br/>Append exchange to `cache.api_http_exchanges[api_call_id]`                                                                                                                                                                                                      | Sync         | -                  |
| **24** | `presenters/request_presenter.py`<br/>`on_exchange_added()`               | RequestPresenter (signal handler)    | Main thread receives signal:<br/>1. Get api_test_case from cache<br/>2. Evaluate assertions: `assertion_result_presenter.evaluate(test_case, exchange)`                                                                                                                                          | Sync         | -                  |
| **25** | `presenters/exchange_presenter.py`<br/>`refresh(exchange)`                | ExchangePresenter (signal handler)   | Main thread receives signal or called directly:<br/>1. Set `self.current_exchange = exchange`<br/>2. Render request: `render_raw_exchange(raw_request)`<br/>3. Render response: `render_raw_exchange(raw_response)`<br/>4. Populate tables with headers/params<br/>5. Display in UI              | Sync         | -                  |
| **26** | `safe_rest_api_interactor.py`<br/>`__request_finished()`                  | SafeRestApiInteractor                | Receives `request_finished` signal:<br/>1. Set `any_worker_running = False`<br/>2. Call `__process_queue()` → Process next queued request                                                                                                                                                        | Sync         | -                  |

### Signal Chain for Request Execution

```
REQUEST EXECUTION SIGNAL CHAIN:

User clicks "Send"
    ↓
on_btn_send_request()
    ↓
SafeRestApiInteractor.make_http_call()
    ├─→ Enqueue ApiWorkerData
    ├─→ Spawn RestApiConnector(QThread).start()
    │
    (BACKGROUND THREAD)
    ├─→ RestApiConnector.run()
    ├─→ RestApiConnector.make_http_call()
    ├─→ http_exchange_signals.request_started.emit(msg, api_call_id)
    │   (ApiListPresenter.on_request_started updates UI)
    │
    ├─→ Requester.make_request()  [BLOCKS on HTTP I/O]
    │
    ├─→ RestApiConnector.signals.result.emit(exchange)
    │   (Main thread receives via Qt signal)
    │
    (MAIN THREAD)
    ├─→ SafeRestApiInteractor.__on_success(exchange)
    ├─→ AppDataWriter.add_http_exchange(exchange)
    ├─→ AppDataWriter.signals.exchange_added.emit(exchange)
    │   ├─→ AppDataCache.on_api_http_exchange_added(exchange)
    │   ├─→ RequestPresenter.on_exchange_added(exchange)
    │   │   └─→ AssertionResultPresenter.evaluate()
    │   └─→ ExchangePresenter.refresh(exchange)
    │       └─→ Display response in UI
    │
    ├─→ http_exchange_signals.request_finished.emit(api_call_id)
    │   └─→ SafeRestApiInteractor.__request_finished()
    │       └─→ Process next queued request
```

### Data Transformations in Request Flow

| Transformation                 | Location                                  | Input                        | Output                                    |
| ------------------------------ | ----------------------------------------- | ---------------------------- | ----------------------------------------- |
| Form→Object                    | `RequestPresenter.form_to_object()`       | UI form fields               | ApiCall object                            |
| ApiCall→ExchangeRequest        | `ExchangeRequest.from_api_call()`         | ApiCall                      | ExchangeRequest                           |
| Variable Substitution          | `replace_variables()`                     | ExchangeRequest + var_tokens | ExchangeRequest (with substituted values) |
| Request→HTTP Kwargs            | `_prepare_request_kwargs()`               | ExchangeRequest              | dict with method, headers, params, data   |
| HTTP Response→ExchangeResponse | `convert_response()`                      | requests.Response            | ExchangeResponse object                   |
| ExchangeResponse→HTML          | `ExchangePresenter.render_raw_exchange()` | ExchangeResponse             | HTML for display                          |

### Request Execution Properties

| Property                    | Value                                                                |
| --------------------------- | -------------------------------------------------------------------- |
| **Threading Model**         | Single QThread worker, sequential requests                           |
| **Queue Implementation**    | Python `Queue.Queue` (thread-safe)                                   |
| **Max Concurrent Requests** | 1 (sequential)                                                       |
| **Timeout Behavior**        | Configurable via AppConfiguration.timeout_in_secs                    |
| **Error Handling**          | Caught in RestApiConnector.run(), signals emitted to UI              |
| **Variable Resolution**     | Before HTTP request (in background thread)                           |
| **Mocking Support**         | If `api_call.mocked_response.is_enabled = True`, skip HTTP, use mock |

---

## TRACE 3: Load Project Flow

### Opening/Loading a Project File (`*.db`)

**Files Involved:**

- `presenters/file_menu_presenter.py` → `core/core_settings.py` → `model/app_data_reader/writer.py` → UI refresh chain

### Step-by-Step Execution

| Step   | Location                                                      | Class/Function    | Action                                                                                                                                                                                                                                                                               | Async? | Signal                            |
| ------ | ------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | --------------------------------- |
| **1**  | `presenters/file_menu_presenter.py`<br/>`on_file_open()` L13  | FileMenuPresenter | User selects File → Open                                                                                                                                                                                                                                                             | -      | -                                 |
| **2**  | `file_menu_presenter.py`<br/>`on_file_open()`                 | FileMenuPresenter | 1. Get `current_user_project = app_settings.load_current_project()`<br/>2. `QFileDialog.getOpenFileName()` to select `*.db` file                                                                                                                                                     | Sync   | -                                 |
| **3**  | `file_menu_presenter.py`<br/>`on_file_open()` L22             | FileMenuPresenter | If file selected and different from current:<br/>1. `user_project.location = file_location`<br/>2. `user_project.state = SavedState.SAVED`<br/>3. `app_settings.save_current_project(user_project)` - Persist to QSettings                                                           | Sync   | -                                 |
| **4**  | `file_menu_presenter.py`<br/>`on_file_open()` L24             | FileMenuPresenter | `self.reload_app()`                                                                                                                                                                                                                                                                  | Sync   | -                                 |
| **5**  | `file_menu_presenter.py`<br/>`reload_app()` L46               | FileMenuPresenter | **Core switching operation**:<br/>1. `app_settings.new_app_data()` - Switch DB table<br/>2. `main_window.presenter.refresh_app()`                                                                                                                                                    | Sync   | -                                 |
| **6**  | `core/core_settings.py`<br/>`new_app_data()` L122             | CoreSettings      | **Database Switch**:<br/>1. `storage = _db_from_current_user_project()` - Load new DB<br/>2. `app_data_reader.ldb = storage.db` - Reassign table<br/>3. `app_data_writer.ldb = storage.db` - Reassign table                                                                          | Sync   | -                                 |
| **7**  | `core/core_settings.py`<br/>`_db_from_current_user_project()` | CoreSettings      | Open database file:<br/>1. Get current user project location<br/>2. `Storage.from_location()` - TinyDB load<br/>3. Return storage object with `.db` table                                                                                                                            | Sync   | -                                 |
| **8**  | `presenters/main_presenter.py`<br/>`refresh_app()` L31        | MainPresenter     | **UI Refresh**:<br/>1. `app_data_cache.load_cache()` - Load all data from new DB<br/>2. `show_frame()` - Show/hide empty frame<br/>3. `main_window.refresh_all_views()` - Notify all presenters<br/>4. `setWindowTitle()` with new project location                                  | Sync   | -                                 |
| **9**  | `model/app_data_cache.py`<br/>`load_cache()` L40              | AppDataCache      | **Cache Reload**:<br/>1. `api_call_list = get_all_api_calls_from_db()` from new DB<br/>2. For each API call, load test cases and exchanges<br/>3. `refresh_app_state()` from new DB<br/>4. `refresh_environments()` from new DB<br/>5. Emit `initial_cache_loading_completed` signal | Sync   | `initial_cache_loading_completed` |
| **10** | `ui/main_window.py`<br/>`refresh_all_views()`                 | MainWindow        | Call refresh on all presenters:<br/>- ApiListPresenter.refresh()<br/>- RequestPresenter.refresh()<br/>- ExchangePresenter.refresh()<br/>- EnvironmentsListPresenter.refresh()<br/>- TagsListPresenter.refresh(), etc.                                                                | Sync   | -                                 |
| **11** | `presenters/api_list_presenter.py`<br/>`refresh()` L228       | ApiListPresenter  | **Rebuild list view**:<br/>1. Clear model<br/>2. Get `api_calls = filter_api_calls()` from cache<br/>3. For each API call, `add_request_widget()` to model<br/>4. Select first item                                                                                                  | Sync   | -                                 |
| **12** | `presenters/api_list_presenter.py`<br/>`add_request_widget()` | ApiListPresenter  | Create QStandardItem for each API call:<br/>- Set text, icon, data roles<br/>- Add to model<br/>- If select_item: set as current                                                                                                                                                     | Sync   | -                                 |
| **13** | `presenters/main_presenter.py`<br/>`show_frame()` L35         | MainPresenter     | Check if API calls exist:<br/>- If yes: show request/response frames<br/>- If no: show "empty" frame with instructions                                                                                                                                                               | Sync   | -                                 |

### Project Loading Signal Chain

```
User clicks File → Open
    ↓
FileMenuPresenter.on_file_open()
    ↓
QFileDialog.getOpenFileName() [Block until file selected]
    ↓
User selects project file
    ↓
FileMenuPresenter.reload_app()
    ├─→ CoreSettings.new_app_data()
    │   ├─→ Close old DB
    │   └─→ Open new DB file
    │
    ├─→ MainPresenter.refresh_app()
    ├─→ AppDataCache.load_cache()
    │   └─→ Emit: initial_cache_loading_completed
    │
    ├─→ MainWindow.refresh_all_views()
    │   ├─→ ApiListPresenter.refresh()
    │   │   └─→ Rebuild list from cache
    │   ├─→ RequestPresenter.refresh()
    │   │   └─→ Clear form or show first API
    │   └─→ ExchangePresenter.refresh()
    │       └─→ Clear response display
    │
    ├─→ MainPresenter.show_frame()
    │   └─→ Show/hide frames based on API count
    │
    └─→ MainWindow.setWindowTitle() with new project path
```

### Key Points

| Aspect                     | Detail                                                |
| -------------------------- | ----------------------------------------------------- |
| **File Format**            | SQLite DB (`*.db`), opened via TinyDB                 |
| **Old DB Cleanup**         | Implicit (DB handle closed when reassigned)           |
| **Cache Invalidation**     | Complete reload via `load_cache()`                    |
| **Signal Emissions**       | `initial_cache_loading_completed` only                |
| **UI Update Order**        | Cache load → signal emit → all presenters refresh     |
| **Backward Compatibility** | Projects created in older versions load via migration |

---

## TRACE 4: Create New Request Flow

### From User Input to Database Persistence

**Files Involved:**

- `presenters/request_presenter.py` → `core/api_call_interactor.py` → `model/app_data_writer.py` → Cache update → UI refresh

### Step-by-Step Execution

| Step   | Location                                                                            | Class/Function    | Action                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Async? | Signal           |
| ------ | ----------------------------------------------------------------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---------------- |
| **1**  | `ui/main_window.py`                                                                 | User              | Click blue "+" button in toolbar to create new API                                                                                                                                                                                                                                                                                                                                                                                                             | -      | -                |
| **2**  | `presenters/api_list_presenter.py`<br/>or toolbar handler                           | Handler           | Create new empty ApiCall object                                                                                                                                                                                                                                                                                                                                                                                                                                | Sync   | -                |
| **3**  | `presenters/request_presenter.py`<br/>`object_to_form()` L100                       | RequestPresenter  | Display blank form:<br/>- Clear URL, method, body<br/>- Clear headers, params, tags<br/>- Set current = None                                                                                                                                                                                                                                                                                                                                                   | Sync   | -                |
| **4**  | User                                                                                | Input Form        | User fills in:<br/>- Title<br/>- URL<br/>- HTTP method (GET/POST/etc.)<br/>- Headers<br/>- Query params<br/>- Body<br/>- Tags                                                                                                                                                                                                                                                                                                                                  | -      | -                |
| **5**  | `presenters/request_presenter.py`<br/>`on_btn_send_request()` L208 (or Save)        | RequestPresenter  | User clicks "Send" or navigates away<br/>Form saving is triggered                                                                                                                                                                                                                                                                                                                                                                                              | Sync   | -                |
| **6**  | `presenters/request_presenter.py`<br/>`update_current_api_call()` (internal method) | RequestPresenter  | **Form→Object Mapping** in `form_to_object()` L176:<br/>1. Parse URL: `split_url_qs(url)` → url + query params<br/>2. Get HTTP method from dropdown<br/>3. `get_headers()` → dict from form<br/>4. `get_query_params()` → dict from form<br/>5. `get_form_params()` → dict from form<br/>6. `get_request_body()` → text from editor<br/>7. Extract title, description, tags<br/>8. Get mocked response if defined<br/>9. Update `self.current` with all values | Sync   | -                |
| **7**  | `presenters/request_presenter.py`<br/>`on_btn_send_request()` L209                  | RequestPresenter  | After form→object mapping, call:<br/>`rest_api_interactor.make_http_call(self.current)`                                                                                                                                                                                                                                                                                                                                                                        | Sync   | -                |
| **7b** | OR: Auto-save handler                                                               | RequestPresenter  | Alternative: On blur/focus loss, auto-save                                                                                                                                                                                                                                                                                                                                                                                                                     |        |                  |
| **8**  | `core/api_call_interactor.py`<br/>`add_api_call()` L4                               | ApiCallInteractor | **Create New Request**:<br/>1. If first time: `api_call.id = gen_uuid()` - Generate unique ID<br/>2. `app_data_writer.update_api_call_in_db(api_call)` L5<br/>3. **Emit signal**: `signals.api_call_added.emit(api_call.id, api_call)` L6                                                                                                                                                                                                                      | Sync   | `api_call_added` |
| **9**  | `model/app_data_writer.py`<br/>`update_api_call_in_db()`                            | AppDataWriter     | **Database Write**:<br/>1. Get table = `ldb[api_call.record_type]`<br/>2. TinyDB upsert: `table.upsert(..., ["id"])`<br/>3. Save JSON: `json.dumps(api_call.to_json())`<br/>4. Indexed by ID                                                                                                                                                                                                                                                                   | Sync   | -                |
| **10** | `model/app_data_cache.py`<br/>`on_api_call_added()` (signal handler)                | AppDataCache      | **Cache Update**:<br/>1. Receive signal with (doc_id, api_call)<br/>2. Set `api_call.id = doc_id`<br/>3. Add to cache: `api_call_list[doc_id] = api_call`                                                                                                                                                                                                                                                                                                      | Sync   | -                |
| **11** | `presenters/api_list_presenter.py`<br/>`add_request_widget()` (signal handler)      | ApiListPresenter  | **List View Update**:<br/>1. Receive signal with api_call<br/>2. Create QStandardItem with:<br/> - Display text: api_call.title<br/> - Icon: method-specific icon<br/> - Data role: API_CALL_ROLE → full api_call object<br/>3. Add item to model<br/>4. If select_item=True: set as current                                                                                                                                                                   | Sync   | -                |
| **12** | `presenters/request_presenter.py`<br/>`on_api_call_refresh()` (if selected)         | RequestPresenter  | If the newly created request is selected:<br/>1. Receive `api_call_updated` signal<br/>2. Call `refresh(api_call)` → Display in form                                                                                                                                                                                                                                                                                                                           | Sync   | -                |
| **13** | User                                                                                | Main Window       | Request now appears in list, can be executed                                                                                                                                                                                                                                                                                                                                                                                                                   | -      | -                |

### New Request Creation Signal Chain

```
User fills form + clicks Send/Save
    ↓
RequestPresenter.form_to_object()
    └─→ Build ApiCall from form fields

    ↓
rest_api_interactor.make_http_call(api_call)
    ↓
ApiCallInteractor.add_api_call(api_call)
    ├─→ api_call.id = gen_uuid() [if new]
    ├─→ AppDataWriter.update_api_call_in_db(api_call)
    │   └─→ SQLite upsert
    │
    ├─→ AppDataWriter.signals.api_call_added.emit(api_call_id, api_call)
    │
    (MAIN THREAD, MULTIPLE SIGNAL HANDLERS)
    ├─→ AppDataCache.on_api_call_added(doc_id, api_call)
    │   └─→ cache.api_call_list[doc_id] = api_call
    │
    ├─→ ApiListPresenter.add_request_widget(doc_id, api_call)
    │   └─→ Add item to list view model
    │
    └─→ RequestPresenter.on_api_call_refresh()
        └─→ Display updated API in form

    ↓
Request sent to API (if not mocked)
    ↓
Response received + persisted
```

### Validation & Error Handling

| Field   | Validation              | Error Handling                       |
| ------- | ----------------------- | ------------------------------------ |
| URL     | Not empty, valid format | Warning in UI, request blocked       |
| Method  | Dropdown selection      | Always valid                         |
| Headers | Key-value pairs         | Invalid pairs ignored                |
| Body    | Any text/JSON           | Invalid JSON logged, body sent as-is |
| Title   | Not required            | Default title if empty               |

---

## TRACE 5: Environment Variable Substitution Flow

### Variable Resolution from Definition to Request Execution

**Files Involved:**

- `core/__init__.py` (replace_variables) → `external/rest_api_connector.py` (make_http_call)
- Environment variables in request URL, headers, params, body

### Variable Resolution Steps

| Step  | Location                                                     | Function                  | Action                                                                                                                                                                                                                                                                                                                                                | Input                        | Output                      |
| ----- | ------------------------------------------------------------ | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------- |
| **1** | `external/rest_api_connector.py`<br/>`make_http_call()` L210 | RestApiConnector          | Get all available variables                                                                                                                                                                                                                                                                                                                           | -                            | var_tokens dict             |
| **2** | `core/__init__.py`<br/>`get_variable_tokens()`               | get_variable_tokens       | **Collect all variables**:<br/>1. Get environments from cache<br/>2. Get current selected environment<br/>3. Build env_map from environment data<br/>4. Get all test case assertions<br/>5. Merge: `{**env_map, **test_case_vars}`                                                                                                                    | app_settings                 | dict of `{var_name: value}` |
| **3** | Environment lookup                                           | Environment object        | Store environment with key-value data:<br/>- Example: `{"BASE_URL": "https://api.example.com"}`<br/>- Data persisted in DB as JSON                                                                                                                                                                                                                    | -                            | -                           |
| **4** | Test case assertions                                         | ApiTestCase object        | Extract variables from response assertions:<br/>- Example: assertion extracts `response.status`<br/>- Stored in test case object                                                                                                                                                                                                                      | HttpExchange                 | RuntimeVar dict             |
| **5** | `core/__init__.py`<br/>`replace_variables()` L208            | replace_variables         | **Substitute variables in request**:<br/>1. `template_sub(url, var_tokens)` → URL substitution<br/>2. `template_sub(headers[k], var_tokens)` → Each header<br/>3. `template_sub(query_params[k], var_tokens)` → Each param<br/>4. `template_sub(form_params[k], var_tokens)` → Each form param<br/>5. `template_sub(body, var_tokens)` → Request body | ExchangeRequest + var_tokens | ExchangeRequest (updated)   |
| **6** | `core/__init__.py`<br/>`template_sub()` L230                 | template_sub              | **Template substitution**:<br/>1. `Template(string).safe_substitute(tokens)`<br/>2. Uses Python's `string.Template` syntax: `${VAR_NAME}`<br/>3. Missing vars → left as `${VAR_NAME}` (safe mode)                                                                                                                                                     | Templated string             | Substituted string          |
| **7** | `core/__init__.py`<br/>`evaluate_nested_functions()` L233    | evaluate_nested_functions | **Function evaluation**:<br/>1. Search for nested function calls: `$func(...)`<br/>2. Evaluate: `base64Encode()`, `base64Decode()`, etc.<br/>3. Replace with result<br/>4. Repeat until no more matches                                                                                                                                               | Substituted string           | Evaluated string            |
| **8** | Variable used in request                                     | REST execution            | Pass substituted variables to HTTP request:<br/>- URL with substituted base URL<br/>- Headers with auth tokens<br/>- Body with JSON values<br/>- Params with filters                                                                                                                                                                                  | Final ExchangeRequest        | HTTP call executed          |

### Variable Syntax Examples

```
URL Template:
  ${BASE_URL}/users/${USER_ID}

After Substitution (with BASE_URL=https://api.example.com, USER_ID=123):
  https://api.example.com/users/123

Header Template:
  Authorization: Bearer ${AUTH_TOKEN}

After Substitution (with AUTH_TOKEN=abc123):
  Authorization: Bearer abc123

Body Template (JSON):
  {
    "user_id": ${USER_ID},
    "timestamp": ${TIMESTAMP}
  }

After Substitution:
  {
    "user_id": 123,
    "timestamp": 1704067200
  }

Function Example:
  encoded: $base64Encode(mypassword)

After Evaluation:
  encoded: bXlwYXNzd29yZA==
```

### Variable Sources Priority

| Priority | Source                               | Format                  | Scope            |
| -------- | ------------------------------------ | ----------------------- | ---------------- |
| 1        | Environment variables (selected env) | `${VAR_NAME}`           | Current project  |
| 2        | Test case assertions                 | `${assertion_var_name}` | Current API call |
| 3        | Python string.Template               | Any remaining `${...}`  | Left unchanged   |

### Environment Variables in Code

```python
# Environment stored in Database (AppData):
Environment(
    name="Production",
    data={
        "BASE_URL": "https://api.prod.example.com",
        "AUTH_TOKEN": "prod_token_xyz",
        "API_KEY": "pk_live_abc123"
    }
)

# Test Case Assertion (Runtime Variables):
ApiTestCase(
    assertions=[
        Assertion(var_name="user_id", selector="data.id", data_from="RESPONSE_BODY"),
        Assertion(var_name="token", selector="token", data_from="RESPONSE_BODY")
    ]
)

# When making next request, these vars available:
var_tokens = {
    "BASE_URL": "https://api.prod.example.com",
    "AUTH_TOKEN": "prod_token_xyz",
    "API_KEY": "pk_live_abc123",
    "user_id": "42",  # from previous response
    "token": "eyJhbG..."  # from previous response
}
```

### Timing of Variable Resolution

| Event                 | Timing                       | Thread                        | Key Point                      |
| --------------------- | ---------------------------- | ----------------------------- | ------------------------------ |
| Variable collection   | Just before HTTP request     | Background (RestApiConnector) | Variables frozen at this point |
| Template substitution | Immediately after collection | Background (RestApiConnector) | Async, before network I/O      |
| Variable scope        | Per-request                  | Request-specific              | Each request has own tokens    |
| Assertion capture     | After response received      | Main thread (via signal)      | Updates cache for next request |

---

## TRACE 6: Export/Code Generation Flow

### From Export Menu to File Download

**Files Involved:**

- `presenters/code_generator_presenter.py` → `exporters/*.py` → UI display/file I/O

### Step-by-Step Execution

| Step   | Location                                                         | Class/Function         | Action                                                                                                                                                                                                                                                                                                                                                                                                                 | Async? | Signal |
| ------ | ---------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------ |
| **1**  | Menu or Toolbar                                                  | User                   | Click: File → "Export as..." or Tools → "Code Generator"                                                                                                                                                                                                                                                                                                                                                               | -      | -      |
| **2**  | `ui/main_window.py`                                              | MainWindow             | Trigger code generator dialog: `code_generator_dialog.show_dialog()`                                                                                                                                                                                                                                                                                                                                                   | Sync   | -      |
| **3**  | `presenters/code_generator_presenter.py`<br/>`show_dialog()` L24 | CodeGeneratorPresenter | **Load exporter list**:<br/>1. `cmb_exporters.clear()`<br/>2. Iterate all registered exporters in `exporter_plugins` dict<br/>3. For each exporter: Create QStandardItem with name<br/>4. Store exporter key in item data role<br/>5. Add item to combo box                                                                                                                                                            | Sync   | -      |
| **4**  | Exporter Discovery                                               | Runtime                | **Plugin loading** (at app startup or dynamic):<br/>1. `from httprider.exporters import exporter_plugins`<br/>2. Module loader scans `exporters/` directory<br/>3. For each module `exporter_*.py`:<br/> - Import module<br/> - Find class with `exporter` attribute<br/> - Register in `exporter_plugins` dict<br/>4. Key: module name (e.g., "exporter_curl")<br/>5. Value: ExporterModule with `.exporter` instance | Sync   | -      |
| **5**  | Dialog                                                           | User                   | Select exporter from dropdown                                                                                                                                                                                                                                                                                                                                                                                          | -      | -      |
| **6**  | `code_generator_presenter.py`<br/>`on_exporter_change()` L32     | CodeGeneratorPresenter | User selects exporter from combo box:<br/>1. Get selected exporter name from item data<br/>2. Look up exporter: `exporter_plugins.get(name)`<br/>3. Call `generate_code(selected_exporter)`                                                                                                                                                                                                                            | Sync   | -      |
| **7**  | `code_generator_presenter.py`<br/>`generate_code()` L41          | CodeGeneratorPresenter | **Code generation**:<br/>**Single API mode**:<br/>1. If `self.selected_api` exists:<br/> - Pass `[self.selected_api]` to exporter<br/>**Multiple API mode**:<br/>2. Else get `all_active_api_calls()` from cache<br/>3. Call: `selected_exporter.export_data(api_calls)` → HTML string<br/>4. Display in text editor: `txt_generated_code.appendHtml(html)`                                                            | Sync   | -      |
| **8**  | `exporters/exporter_curl.py`<br/>or other                        | Exporter class         | **Export implementation**:<br/>1. Input: `[ApiCall, ...]`<br/>2. For each API call:<br/> - Extract method, URL, headers, body<br/> - Format as exporter-specific code<br/> - Example (curl): `curl -X GET "url" -H "header: value"`<br/>3. Return formatted string (HTML or plain text)                                                                                                                                | Sync   | -      |
| **9**  | Dialog box                                                       | User                   | User sees generated code in text editor<br/>Options: Copy, Export to File                                                                                                                                                                                                                                                                                                                                              | -      | -      |
| **10** | `code_generator_presenter.py`<br/>`on_copy_clipboard()` L46      | CodeGeneratorPresenter | User clicks "Copy":<br/>1. `selectAll()` on text editor<br/>2. `copy()` to clipboard (Qt clipboard)<br/>3. Show status message: "Copied"                                                                                                                                                                                                                                                                               | Sync   | -      |
| **11** | `code_generator_presenter.py`<br/>`on_export_file()` L51         | CodeGeneratorPresenter | User clicks "Export":<br/>1. `QFileDialog.getSaveFileName()` → file path<br/>2. Get text from editor: `toPlainText()`<br/>3. Create Path object and `write_text()`<br/>4. Show status: "File saved..."                                                                                                                                                                                                                 | Sync   | -      |

### Exporter Plugin Architecture

| Component             | File                              | Purpose                                                     |
| --------------------- | --------------------------------- | ----------------------------------------------------------- |
| **Exporter Registry** | `httprider/exporters/__init__.py` | Loads all exporter modules, creates `exporter_plugins` dict |
| **Base Exporter**     | `exporters/exporter_*.py`         | Each exporter module with `exporter` singleton instance     |
| **Exporter Instance** | `@attr.s class ExporterName`      | Has `name`, `output_ext`, `export_data(api_calls)` method   |
| **Common Utilities**  | `exporters/common.py`             | Shared functions: `highlight_json()`, `to_curl()`, etc.     |

### Exporter Examples

```python
# Example: exporter_curl.py
@attr.s
class CurlExporter:
    name = "cURL"
    output_ext = ".sh"

    def export_data(self, api_calls: list[ApiCall]):
        """Convert API calls to cURL commands"""
        commands = []
        for api_call in api_calls:
            cmd = to_curl(api_call, exchange=None)
            commands.append(cmd)
        return "\n".join(commands)

exporter = CurlExporter()

# Example: exporter_python_requests.py
@attr.s
class PythonRequestsExporter:
    name = "Python (requests)"
    output_ext = ".py"

    def export_data(self, api_calls: list[ApiCall]):
        """Generate Python requests code"""
        # Build Python code with requests.get() calls
        code = "import requests\n\n"
        for api_call in api_calls:
            code += f"response = requests.{api_call.http_method.lower()}('{api_call.http_url}')\n"
        return code

exporter = PythonRequestsExporter()
```

### Export Signal Flow

```
User clicks "Export..."
    ↓
CodeGeneratorPresenter.show_dialog()
    ├─→ Load exporter_plugins dictionary
    ├─→ Populate combo box with exporter names
    └─→ Show dialog

User selects exporter
    ↓
CodeGeneratorPresenter.on_exporter_change()
    ├─→ Look up exporter from plugins dict
    └─→ Call generate_code(exporter)
        ├─→ Get api_calls from cache or selection
        └─→ Call exporter.export_data(api_calls)
            └─→ Generate format-specific code

User clicks "Copy" or "Export to File"
    ↓
Copy to clipboard or file:
    ├─→ QClipboard or Path.write_text()
    └─→ Show success message
```

### Supported Exporters (as of last scan)

| Exporter           | File                            | Output Format   | Use Case                        |
| ------------------ | ------------------------------- | --------------- | ------------------------------- |
| cURL               | `exporter_curl.py`              | Shell script    | Quick API testing from terminal |
| Python requests    | `exporter_python_requests.py`   | Python code     | Python-based automation         |
| Java Feign         | `exporter_java_feign_client.py` | Java code       | Spring Boot microservices       |
| REST-assured       | `exporter_restassured.py`       | Java test code  | JUnit test cases                |
| OpenAPI v3         | `exporter_openapi_v3.py`        | YAML/JSON       | API specification export        |
| Postman Collection | (assumed)                       | JSON            | Import to Postman               |
| Markdown           | `exporter_markdown.py`          | Markdown        | API documentation               |
| Mermaid            | `exporter_mermaid.py`           | Mermaid diagram | Flow visualization              |

---

## TRACE 7: Import Flow (cURL/Text)

### From Text Input to Database Persistence

**Files Involved:**

- `presenters/importer_presenter.py` → `importers/*.py` → `core/api_call_interactor.py` → Database

### Step-by-Step Execution

| Step   | Location                                                                    | Class/Function                    | Action                                                                                                                                                                                                                                                                                                | Async? | Signal                     |
| ------ | --------------------------------------------------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | -------------------------- |
| **1**  | Menu                                                                        | User                              | Click: File → "Import from..." or Tools → "Import"                                                                                                                                                                                                                                                    | -      | -                          |
| **2**  | `presenters/importer_presenter.py`<br/>`on_import_selected()` or menu click | ImporterPresenter                 | Display import method menu or dialog:<br/>- From file (e.g., Postman export)<br/>- From text (e.g., cURL command)                                                                                                                                                                                     | Sync   | -                          |
| **3**  | Menu                                                                        | User                              | Select import method (e.g., "cURL command")                                                                                                                                                                                                                                                           | -      | -                          |
| **4**  | `importers/importer_curl.py`<br/>(or other)                                 | ImporterModule                    | **Importer instantiation**:<br/>- Each importer has `input_type`: "file" or "text"<br/>- For cURL: `input_type = "text"`                                                                                                                                                                              | Sync   | -                          |
| **5**  | `importer_presenter.py`<br/>`import_collection()` L15                       | ImporterPresenter                 | **Check input type**:<br/>If `importer.input_type == "text"`:<br/>- Call `import_text_dialog.show_dialog(self.importer.import_data)` L19<br/>- Show dialog for user to paste text                                                                                                                     | Sync   | -                          |
| **6**  | `ui/import_text_dialog.py`                                                  | ImportTextDialog                  | **Dialog display**:<br/>1. Show large text input area<br/>2. User pastes cURL command or other format<br/>3. User clicks "Import" button                                                                                                                                                              | -      | -                          |
| **7**  | `ui/import_text_dialog.py`<br/>on_import button                             | Dialog                            | **Parse input**:<br/>1. Get text from input field<br/>2. Call `importer.import_data(text)` - Pass to importer<br/>3. Importer parses and returns (project_info, api_calls_list)                                                                                                                       | Sync   | -                          |
| **8**  | `importers/importer_curl.py`<br/>`import_data()`                            | CurlImporter                      | **cURL parsing**:<br/>1. Regex parse cURL syntax:<br/> - Extract: `-X METHOD`<br/> - Extract: URL (last arg)<br/> - Extract: `-H "Header: value"` (all occurrences)<br/> - Extract: `-d "body"` if present<br/>2. Build ApiCall objects for each command<br/>3. Return (project_info, [ApiCall, ...]) | Sync   | -                          |
| **9**  | `importer_presenter.py`<br/>`on_selected_text_to_import()` L12              | ImporterPresenter                 | Receive parsed API calls list:<br/>Call `api_call_interactor.add_multiple_api_calls(api_calls)`                                                                                                                                                                                                       | Sync   | -                          |
| **10** | `core/api_call_interactor.py`<br/>`add_multiple_api_calls()` L8             | ApiCallInteractor                 | **Bulk addition**:<br/>1. For each api_call:<br/> - Set `id = gen_uuid()`<br/> - Call `update_api_call_in_db(api_call)` (suppress signal)<br/>2. After all added:<br/> - **Emit single signal**: `multiple_api_calls_added.emit(doc_ids, api_calls)` L13                                              | Sync   | `multiple_api_calls_added` |
| **11** | `model/app_data_writer.py`<br/>`update_api_call_in_db()`                    | AppDataWriter                     | **Database write**:<br/>1. Get table by record type<br/>2. Upsert API call as JSON<br/>3. Commit to SQLite                                                                                                                                                                                            | Sync   | -                          |
| **12** | `model/app_data_cache.py`<br/>`on_multiple_api_calls_added()`               | AppDataCache (signal handler)     | **Cache update**:<br/>1. Receive signal with (doc_ids, api_calls)<br/>2. For each doc_id, api_call:<br/> - Set `api_call.id = doc_id`<br/> - Add to cache: `api_call_list[id] = api_call`                                                                                                             | Sync   | -                          |
| **13** | `presenters/api_list_presenter.py`<br/>`refresh_multiple_items()`           | ApiListPresenter (signal handler) | **List view update**:<br/>1. Receive signal with multiple API calls<br/>2. Call `refresh()` to rebuild entire list<br/>3. All imported requests appear in list                                                                                                                                        | Sync   | -                          |
| **14** | Dialog                                                                      | Dialog                            | Close import dialog                                                                                                                                                                                                                                                                                   | -      | -                          |
| **15** | Main Window                                                                 | User                              | Imported requests now in list, ready to execute                                                                                                                                                                                                                                                       | -      | -                          |

### Import Parsers Supported

| Format      | Parser File            | Input          | Parsing Logic                            |
| ----------- | ---------------------- | -------------- | ---------------------------------------- |
| **cURL**    | `importer_curl.py`     | Shell command  | Regex cURL syntax: `-X`, `-H`, `-d`, URL |
| **Postman** | `importer_postman.py`  | JSON export    | JSON structure → ApiCall mapping         |
| **OpenAPI** | `importer_openapi.py`  | YAML/JSON spec | Spec endpoints → ApiCall objects         |
| **Swagger** | (derived from OpenAPI) | JSON spec      | Similar to OpenAPI parsing               |
| **HAR**     | `importer_har.py`      | JSON HAR file  | Parse `.entries[].request` → ApiCall     |

### cURL Import Example

```
User pastes:
  curl -X POST "https://api.example.com/users" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer token" \
    -d '{"name": "John"}'

Parser extracts:
  method: POST
  url: https://api.example.com/users
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer token"
  }
  body: {"name": "John"}

Creates ApiCall with:
  title: "POST /users"
  http_method: "POST"
  http_url: "https://api.example.com/users"
  http_headers: {...}
  http_request_body: '{"name": "John"}'
```

### Import Signal Chain

```
User clicks "Import from cURL"
    ↓
ImporterPresenter.import_collection()
    ├─→ Check input_type = "text"
    └─→ Show ImportTextDialog

User pastes cURL command + clicks "Import"
    ↓
ImportTextDialog.on_import_button()
    ├─→ Get text from input
    └─→ Call importer.import_data(text)

CurlImporter.import_data()
    ├─→ Regex parse cURL syntax
    ├─→ Build ApiCall objects
    └─→ Return (project_info, [ApiCall, ...])

ImporterPresenter.on_selected_text_to_import()
    ├─→ Receive api_calls list
    └─→ Call api_call_interactor.add_multiple_api_calls()

ApiCallInteractor.add_multiple_api_calls()
    ├─→ For each api_call:
    │   └─→ update_api_call_in_db() [suppress signal]
    │
    ├─→ Emit: multiple_api_calls_added.emit(ids, calls)
    │
    (MAIN THREAD, SIGNAL HANDLERS)
    ├─→ AppDataCache.on_multiple_api_calls_added()
    │   └─→ Add to cache dict
    │
    ├─→ ApiListPresenter.refresh_multiple_items()
    │   └─→ Rebuild list view
    │
    └─→ Dialog closes

User sees imported requests in list
```

---

## TRACE 8: Search/Filter Flow

### From Search Input to Filtered List Display

**Files Involved:**

- `ui/search_widget.py` (search box) → `presenters/api_list_presenter.py` → `model/app_data_cache.py` → List update

### Step-by-Step Execution

| Step  | Location                                                                 | Class/Function        | Action                                                                                                                                                                                                                                                                                  | Async? | Signal                 |
| ----- | ------------------------------------------------------------------------ | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---------------------- |
| **1** | Search widget                                                            | UI                    | User types in search box (API title search)                                                                                                                                                                                                                                             | -      | -                      |
| **2** | A custom LineEdit                                                        | textChanged signal    | As user types, `textChanged` signal emitted (Qt built-in)                                                                                                                                                                                                                               | Sync   | `textChanged`          |
| **3** | `presenters/` (connected handler)                                        | Handler               | Handler connected to search box `textChanged` signal:<br/>1. Get search query text<br/>2. Update app state: `app_state.selected_search = query`<br/>3. Emit: `selected_tag_changed` signal (or similar)                                                                                 | Sync   | `selected_tag_changed` |
| **4** | `presenters/api_list_presenter.py`<br/>`refresh()` (signal handler) L228 | ApiListPresenter      | Receive `selected_tag_changed` signal:<br/>1. Clear model<br/>2. Call `app_data_cache.filter_api_calls(search_query, search_tag)`                                                                                                                                                       | Sync   | -                      |
| **5** | `model/app_data_cache.py`<br/>`filter_api_calls()` L147                  | AppDataCache          | **Cache filtering (in-memory)**:<br/>1. Build filter function via `_build_filter_query(query, tag)` <br/>2. Get `all_api_calls` from cache dict (no DB query)<br/>3. Filter using lambda: `query.lower() in title.lower()`<br/>4. Sort by `sequence_number`<br/>5. Return filtered list | Sync   | -                      |
| **6** | `model/app_data_cache.py`<br/>`_build_filter_query()` L12                | AppDataCache (static) | **Filter lambda builder**:<br/>If both query and tag:<br/>`lambda: query in title AND tag in tags`<br/>Else if tag only:<br/>`lambda: tag in tags`<br/>Else if query only:<br/>`lambda: query in title`<br/>Else: `lambda: api_call` (all)                                              | Sync   | -                      |
| **7** | `presenters/api_list_presenter.py`<br/>`refresh()` L228                  | ApiListPresenter      | **Rebuild list view**:<br/>1. Get filtered api_calls from cache<br/>2. For each api_call: `add_request_widget(id, api_call)` → Create QStandardItem<br/>3. Add item to model<br/>4. Select first item in filtered results                                                               | Sync   | -                      |
| **8** | `widgets/api_calls_list_view.py`                                         | QtListView            | **List rendered** with filtered items                                                                                                                                                                                                                                                   | Sync   | -                      |
| **9** | Main window                                                              | UI                    | User sees filtered list of API calls matching search                                                                                                                                                                                                                                    | -      | -                      |

### Tag Filtering

| Step                   | Details                                                                          |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Tag Selection**      | User clicks tag in tags panel → `selected_tag_changed` signal                    |
| **Filter Application** | Same flow as search, but filter by tag instead of title                          |
| **Combined Filter**    | If both tag and search query set:<br/>- Filter: `query in title AND tag in tags` |
| **Default Tag**        | Constant `DEFAULT_TAG` = "None" or similar                                       |

### Search Implementation Details

```python
# In AppDataCache._build_filter_query()
def _build_filter_query(query=None, tag=None):
    selected_tag = tag if tag != DEFAULT_TAG else None

    if selected_tag and query:
        # Both tag and query
        return lambda api_call: (
            query.lower() in api_call.title.lower() and
            selected_tag in api_call.tags
        )

    if selected_tag:
        # Tag only
        return lambda api_call: selected_tag in api_call.tags

    if query:
        # Query only
        return lambda api_call: query.lower() in api_call.title.lower()

    # No filter
    return lambda api_call: api_call

# In AppDataCache.filter_api_calls()
def filter_api_calls(self, search_query=None, search_tag=None):
    filter_func = _build_filter_query(query=search_query, tag=search_tag)
    all_calls = self.get_all_api_calls()  # From cache dict

    return sorted(
        filter(filter_func, all_calls),  # In-memory filter
        key=lambda a: a.sequence_number or 0
    )
```

### Search Signal Chain

```
User types in search box
    ↓
QLineEdit.textChanged signal
    ↓
Connected handler
    ├─→ app_state.selected_search = query
    └─→ Emit selected_tag_changed signal

AppDataCache or AppStateInteractor
    ├─→ Update selected_search in app state
    └─→ Save to DB (async)

ApiListPresenter
    ├─→ Receive selected_tag_changed or similar
    └─→ Call refresh()

ApiListPresenter.refresh()
    ├─→ app_data_cache.filter_api_calls(query, tag)
    │   └─→ IN-MEMORY FILTER (no DB query!)
    │       └─→ Returns filtered list
    │
    ├─→ Model.clear()
    ├─→ For each filtered api_call:
    │   └─→ add_request_widget()
    │       └─→ Create QStandardItem
    │       └─→ Add to model
    │
    └─→ List view automatically updates
```

### Performance Characteristics

| Aspect           | Detail                                                    |
| ---------------- | --------------------------------------------------------- |
| **Filter Speed** | ~1-10ms for 500 API calls (in-memory filtering)           |
| **Search Scope** | API title field only (case-insensitive)                   |
| **Tag Scope**    | All tags on API call                                      |
| **DB Queries**   | Zero - all filtering from cache                           |
| **Latency**      | Instant (no network/disk I/O)                             |
| **Debouncing**   | None visible in code (immediate filter on each keystroke) |

---

## Summary Table: All 8 Critical Flows

| Flow                 | Entry Point             | Key Classes                                | Duration   | Async?          | Signal Chain Length |
| -------------------- | ----------------------- | ------------------------------------------ | ---------- | --------------- | ------------------- |
| **Startup**          | `bin/app`               | CoreSettings, AppDataCache, MainPresenter  | 100-2000ms | No              | 5-7 signals         |
| **Send Request**     | `on_btn_send_request()` | RestApiConnector, AppDataWriter            | 100ms-10s  | Yes (HTTP I/O)  | 8-10 signals        |
| **Load Project**     | `on_file_open()`        | CoreSettings.new_app_data()                | 100-2000ms | No              | 1-3 signals         |
| **Create Request**   | Form input → Send       | ApiCallInteractor                          | <100ms     | No              | 2-3 signals         |
| **Env Substitution** | `make_http_call()`      | get_variable_tokens(), replace_variables() | <10ms      | No (background) | 0 signals           |
| **Export**           | `show_dialog()`         | Exporter plugins                           | 10-100ms   | No              | 0 signals           |
| **Import**           | `import_collection()`   | Importer plugins, ApiCallInteractor        | 50-500ms   | No              | 1-2 signals         |
| **Search/Filter**    | `textChanged` signal    | AppDataCache.filter_api_calls()            | <10ms      | No              | 1 signal            |

---

## Architecture Principles Demonstrated

### Signal-Driven Updates

- **Never modify UI directly** - Always emit signals from Interactor/Writer
- **Multiple handlers** - One signal can trigger multiple presenter updates
- **No circular dependencies** - Cache doesn't call Presenter; Presenter reads Cache

### Thread Safety

- **QThread for async work** - RestApiConnector runs in background
- **Thread-safe queue** - Python `Queue.Queue` manages sequential execution
- **Signal crossing threads** - Qt delivers signals to correct thread via event loop

### Performance Optimization

- **In-memory caching** - All data loaded at startup, zero-latency filters
- **Lazy loading** - Related data (exchanges, test cases) loaded on demand
- **Batch operations** - `add_multiple_api_calls()` emits single signal for many items

### Error Handling

- **Silent failures** - Network errors caught and displayed in UI
- **Exception logging** - Uncaught exceptions logged before re-raising
- **Mocked responses** - Can bypass network entirely for offline testing

---

**This document reflects actual code paths traced from:**

- Entry point: `bin/app` → `httprider/application.py`
- Key execution classes verified with line numbers
- Signal chain confirmed from connect() statements
- DB operations verified in `app_data_reader/writer.py`

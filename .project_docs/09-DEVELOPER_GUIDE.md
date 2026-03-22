# Developer Guide: HTTP-Rider

A practical guide for developers contributing to or extending HTTP-Rider.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Code Organization](#code-organization)
3. [Making Your First Change](#making-your-first-change)
4. [Architecture Principles](#architecture-principles)
5. [Testing Guidelines](#testing-guidelines)
6. [Code Style & Quality](#code-style--quality)
7. [Contributing](#contributing)
8. [Common Tasks](#common-tasks)
9. [Troubleshooting](#troubleshooting)

---

## Development Setup

### Prerequisites

- **Python 3.11+** - Check version: `python3 --version`
- **uv package manager** - Install via: `brew install uv` (macOS) or see [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- **Git** - For version control

### Initial Setup

```bash
# 1. Clone the repository
git clone https://github.com/namuan/http-rider.git
cd http-rider

# 2. Install dependencies and dev tools
make install

# 3. Run the application
make run

# 4. Run tests
make test

# 5. Check code quality
make check
```

### Makefile Commands

| Command        | Purpose                               |
| -------------- | ------------------------------------- |
| `make install` | Install deps + setup pre-commit hooks |
| `make run`     | Run the application                   |
| `make test`    | Run pytest suite                      |
| `make check`   | Lint, format check, test              |
| `make format`  | Auto-format code with black           |
| `make lint`    | Run ruff linter                       |
| `make package` | Build executable with PyInstaller     |

### IDE Setup

#### VS Code

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  }
}
```

#### PyCharm

- Run `make install` first
- Mark `httprider/` as "Sources Root"
- Configure Python interpreter to `.venv/bin/python`

---

## Code Organization

### Directory Structure

```
httprider/
├── __init__.py              # Package initialization
├── application.py           # App entry point & initialization
├── debug_app.py            # Debug/dev launcher
│
├── core/                    # ⭐ Business logic (MOST IMPORTANT)
│   ├── api_call_interactor.py      # REST API CRUD operations
│   ├── app_state_interactor.py     # App state management
│   ├── safe_rest_api_interactor.py # Async HTTP execution
│   ├── json_data_generator.py      # Test data generation (Faker)
│   ├── environment_interactor.py   # Environment variable handling
│   ├── app_state.py                # App state data model
│   ├── constants.py                # Enums & app constants
│   ├── core_settings.py            # Singleton config object (⚠️ avoid!)
│   └── ...
│
├── model/                   # Data structures & persistence
│   ├── app_data.py         # Core data classes (ApiCall, HttpExchange)
│   ├── app_configuration.py # App config data
│   ├── storage.py          # SQLite persistence layer
│   ├── app_data_cache.py   # In-memory cache with filtering
│   ├── app_data_writer.py  # Signals + DB writes
│   └── app_data_reader.py  # Cache queries
│
├── ui/                      # Window & dialog UI
│   ├── main_window.py      # Primary window
│   ├── dialogs/            # 10+ dialog forms
│   └── ...
│
├── presenters/              # MVP controllers (30+ files)
│   ├── main_presenter.py   # Primary UI controller
│   ├── request_presenter.py # Request form handler
│   ├── api_list_presenter.py # API list management
│   └── ...
│
├── widgets/                 # Reusable UI components
│   ├── api_calls_list_view.py
│   ├── json_tree_widget.py
│   └── ...
│
├── external/                # HTTP & external services
│   ├── rest_api_connector.py  # Async HTTP + QThread worker
│   └── requester.py         # requests library wrapper
│
├── exporters/               # Code generation (16+ formats)
│   ├── common.py
│   ├── exporter_*.py (15 files)
│   └── ...
│
├── importers/               # Import from external formats
│   ├── common.py
│   └── importer_*.py (3 files)
│
└── codegen/                 # Code generation utilities
    └── ...
```

### Where to Make Different Changes

| Task                          | Location                                         |
| ----------------------------- | ------------------------------------------------ |
| **Add a new API feature**     | `httprider/core/api_call_interactor.py`          |
| **Change data persistence**   | `httprider/model/app_data.py` or `storage.py`    |
| **Add UI dialog**             | `httprider/ui/dialogs/`                          |
| **Add export format**         | `httprider/exporters/exporter_newformat.py`      |
| **Add import format**         | `httprider/importers/importer_newformat.py`      |
| **Fix UI responsiveness**     | `httprider/external/safe_rest_api_interactor.py` |
| **Change assertion matchers** | `httprider/core/assertion*.py`                   |

---

## Making Your First Change

### Example: Add a new assertion matcher type

**Goal**: Support "does not equal" assertion matcher

#### Step 1: Understand the data model

Read `httprider/model/app_data.py`:

```python
@dataclass
class AssertionMatch:
    assert_matcher: str  # "equals", "contains", "regex", etc.
    assert_property: str  # "body", "status_code", "header"
    assert_expected: str  # The value to match
```

Read `httprider/core/constants.py`:

```python
class AssertionMatcher(str, Enum):
    EQUALS = "equals"
    CONTAINS = "contains"
    REGEX = "regex"
    # ... others
```

#### Step 2: Update constants

Edit `httprider/core/constants.py`:

```python
class AssertionMatcher(str, Enum):
    # ... existing
    NOT_EQUALS = "not_equals"  # ADD THIS
```

#### Step 3: Implement matching logic

Find assertion matching in `httprider/core/` - likely `assertion*.py` or search for `AssertionMatch` usage:

```bash
grep -r "assert_matcher ==" httprider/core/
```

Look for the evaluation logic and add:

```python
elif assertion.assert_matcher == AssertionMatcher.NOT_EQUALS:
    return assertion.assert_expected != actual_value
```

#### Step 4: Update the UI (optional)

In `httprider/ui/` or `httprider/generated/`, find the assertion dialog and add the new matcher to the dropdown list.

#### Step 5: Add a test

Create/update `httprider/tests/core/test_assertions.py`:

```python
def test_not_equals_assertion():
    assertion = AssertionMatch(
        assert_matcher="not_equals",
        assert_property="status_code",
        assert_expected="400"
    )
    # Evaluate and assert...
```

#### Step 6: Test manually

```bash
make run
# Create request, add "not_equals" assertion, send request, verify result
```

#### Step 7: Submit PR

```bash
git add .
git commit -m "feat: add not_equals assertion matcher"
git push origin my-feature-branch
# Open PR on GitHub
```

---

## Architecture Principles

### 📋 Critical Principles (From: [02-ARCHITECTURE.md](02-ARCHITECTURE.md))

**✅ DO:**

1. **Emit signals after DB writes**

   ```python
   # Good: Write to DB, then emit signal
   storage.add_request(api_call)
   self.signals.api_call_added.emit(api_call.id, api_call)

   # BAD: Direct cache update
   self.cache.requests[api_call.id] = api_call  # Don't do this
   ```

2. **Let signals drive UI updates**

   ```python
   # Good: Presenter listens to signals
   class RequestPresenter:
       def __init__(self):
           self.signals.api_call_added.connect(self.on_api_call_added)

       def on_api_call_added(self, api_id: str, api_call: ApiCall):
           # Update UI
           self.update_list()

   # BAD: Presenter calls UI directly
   self.main_window.add_request_to_list(api_call)  # Don't do this
   ```

3. **Use interactors for all business logic**

   ```python
   # Good: All logic in interactor
   class APICallInteractor:
       def add_api_call(self, request_data):
           # Validate
           # Transform
           # Persist
           # Emit signal

   # BAD: Presenter has business logic
   class RequestPresenter:
       def save_request(self):
           # Don't put complex logic here
   ```

4. **Keep modules focused on single responsibility**
   - `api_call_interactor.py` → API CRUD only
   - `app_state_interactor.py` → App state only
   - Don't mix concerns

**❌ DON'T:**

1. **Create circular dependencies**

   ```python
   # BAD: Cache calls writer, writer updates cache
   # Use signals instead - they decouple
   ```

2. **Call UI directly from interactors**

   ```python
   # BAD:
   class ApiCallInteractor:
       def add_request(self, ...):
           self.ui.add_to_list()  # NEVER DO THIS

   # Good: Use signals and presenters
   ```

3. **Create threads on UI events**

   ```python
   # BAD:
   def on_send_clicked(self):
       thread = Thread(target=self.send_request)  # NEVER

   # Good: Use SafeRestApiInteractor
   self.executor.execute_request(api_call)
   ```

4. **Ignore the signal-driven architecture**
   - Always ensure: DB write → Signal emit → Cache update → UI refresh
   - Never shortcut this chain

---

## Testing Guidelines

### Test Structure

```
httprider/tests/
├── __init__.py
├── conftest.py          # pytest fixtures
├── core/                # Tests for httprider/core/
│   ├── test_api_call_interactor.py
│   └── ...
├── exporters/           # Tests for exporters
├── presenters/          # [MINIMAL - needs improvement]
└── ...
```

### Current Test Status ⚠️

- **Coverage**: ~4% (Critical gap!)
- **Strong areas**: Export/import logic
- **Weak areas**: Presenters, UI, error handling

### Writing Tests

#### Test a Presenter

Currently difficult (PyQt coupling), but here's how:

```python
# Always test in isolation (no QApplication)
def test_request_presenter_save():
    # Don't create Qt widgets
    presenter = RequestPresenter()

    # Mock the interactor
    presenter.interactor = Mock()

    # Mock signals
    presenter.signals = Mock()

    # Call method
    presenter.save_request()

    # Verify calls
    presenter.interactor.add_api_call.assert_called_once()
    presenter.signals.request_saved.emit.assert_called_once()
```

#### Test an Interactor

Easiest to test:

```python
def test_api_call_interactor():
    # Create instance directly
    interactor = ApiCallInteractor(mock_storage, mock_signals)

    # Execute method
    interactor.add_api_call({"method": "GET", "url": "http://example.com"})

    # Verify storage was called
    mock_storage.add_api_call.assert_called_once()

    # Verify signal was emitted
    mock_signals.api_call_added.emit.assert_called_once()
```

#### Test an Exporter

```python
def test_python_exporter():
    api_call = ApiCall(
        method="GET",
        url="http://api.example.com/users",
        headers={"Authorization": "Bearer token"}
    )

    exporter = PythonRequestsExporter()
    code = exporter.export(api_call)

    # Verify output contains correct Python code
    assert "import requests" in code
    assert 'requests.get("http://api.example.com/users"' in code
    assert '"Authorization": "Bearer token"' in code
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest httprider/tests/core/test_api_call_interactor.py -v

# Run with coverage
pytest --cov=httprider httprider/tests/

# Run single test
pytest httprider/tests/core/test_api_call_interactor.py::test_add_api_call -v
```

---

## Code Style & Quality

### Formatting & Linting

```bash
# Format code automatically
black httprider/

# Check style violations
ruff check httprider/

# Fix simple issues
ruff check --fix httprider/
```

### Pre-commit Hooks

Make is automatically set up by `make install`. It will:

- Format with black
- Check with ruff
- Validate lock file

### Type Hints (Improving!)

Currently <10% coverage. When writing new code, include type hints:

```python
# Good:
def add_api_call(self, request_data: dict) -> ApiCall:
    """Add a new API call to the project.

    Args:
        request_data: Dictionary with method, url, headers, body

    Returns:
        The created ApiCall object
    """
    # ...
    return api_call

# Less helpful:
def add_api_call(self, request_data):
    return api_call
```

---

## Contributing

### Before Starting

1. **Check existing issues** - Search GitHub issues for similar requests
2. **Read architecture docs** - Review [02-ARCHITECTURE.md](02-ARCHITECTURE.md)
3. **Understand current code** - Use execution traces in [04-EXECUTION_TRACES.md](04-EXECUTION_TRACES.md)

### PR Workflow

1. **Fork & branch**

   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes**

   - Keep commits focused and small
   - Write clear commit messages
   - Add tests for new code
   - Update docs if needed

3. **Verify quality**

   ```bash
   make check  # Linting, formatting, tests
   make test   # Full test suite
   ```

4. **Push & create PR**

   ```bash
   git push origin feature/my-feature
   # Open PR on GitHub with description
   ```

5. **Address feedback**
   - Review comments promptly
   - Push additional commits

### PR Guidelines

- **Title**: Clear, lowercase (`fix: resolve assertion timing issue`)
- **Description**: Explain what and why
- **Tests**: Always include tests
- **Size**: Keep PRs focused (not >500 lines)

---

## Common Tasks

### Add a New Exporter

1. Create `httprider/exporters/exporter_myformat.py`
2. Inherit from exporter base class (see `exporter_python_requests.py`)
3. Implement `export(api_call: ApiCall) -> str` method
4. Add test in `httprider/tests/exporters/test_exporter_myformat.py`
5. It's automatically discovered! (No registration needed)

### Add a New Importer

1. Create `httprider/importers/importer_myformat.py`
2. Implement parse logic
3. Return list of `ApiCall` objects
4. Add tests
5. Automatically discovered!

### Add a New Setting

1. Add field to `CoreSettings` class
2. Update UI settings dialog
3. Add persistence in `app_configuration.py`
4. Update presenter to use setting

### Debug a Feature

1. Find entry point in [06-FEATURE_CODE_REFERENCE.md](06-FEATURE_CODE_REFERENCE.md)
2. Trace execution in [04-EXECUTION_TRACES.md](04-EXECUTION_TRACES.md)
3. Add print statements or use debugger
4. Use `make run` (default) or `make debug` (if available)

---

## Troubleshooting

### Common Issues

**Q: Import errors when running `make run`**

```bash
# Solution: Reinstall
make install
source .venv/bin/activate
python -m httprider.application
```

**Q: Tests fail locally but pass in CI**

```bash
# Solution: Ensure clean cache
rm -rf .pytest_cache __pycache__
make test
```

**Q: Type hints not working in IDE**

```bash
# Solution: Run mypy or add stubs
# Or check IDE is using correct Python interpreter path
```

**Q: PyQt6 import errors**

```bash
# Solution: Ensure Qt platform plugin installed
pip install PyQt6  # Already done by make install
# On Linux: sudo apt install qt6-qpa-plugins
```

**Q: Changes not reflected when running app**

```bash
# Solution: Clear cache
rm -rf httprider/__pycache__
make run
```

### Getting Help

1. **Check documentation**: [README.md](README.md) and linked docs
2. **Search code**: `grep -r "my_error_message" httprider/`
3. **Read execution traces**: [04-EXECUTION_TRACES.md](04-EXECUTION_TRACES.md)
4. **Ask on GitHub**: Open an issue with details

---

## Next Steps

- ✅ Set up development environment (`make install`)
- ✅ Read [02-ARCHITECTURE.md](02-ARCHITECTURE.md) overview
- ✅ Run the app (`make run`) and explore features
- ✅ Pick a small bug or feature
- ✅ Use this guide to make your first change
- ✅ Submit a PR!

**Questions?** Check the documentation index in [README.md](README.md).

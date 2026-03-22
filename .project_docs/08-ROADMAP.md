# HTTP-Rider Quality Assessment - SCORECARD & ACTION ITEMS

## Executive Scorecard

```
╔════════════════════════════════════════════════════════════╗
║                 ENGINEERING QUALITY REPORT                 ║
║                    HTTP-RIDER V0.6.4                       ║
╚════════════════════════════════════════════════════════════╝

OVERALL QUALITY GRADE: 6.4/10 (FAIR)

┌─────────────────────────────────────────────────────────────┐
│ Dimension              │ Score │ Trend │ Status            │
├───────────────────────┼───────┼───────┼───────────────────┤
│ Maintainability       │ 6.5/10│  →    │ 🟡 Moderate       │
│ Scalability           │ 5.0/10│  ↓    │ 🔴 Limited        │
│ Testability           │ 3.5/10│  ↓↓   │ 🔴 Critical       │
│ Safety & Security     │ 6.0/10│  ↓    │ 🟡 Concerns       │
│ DevOps & Build        │ 7.5/10│  ↑    │ 🟢 Good foundation│
│ Performance           │ 6.5/10│  →    │ 🟡 Acceptable     │
│ Developer Experience  │ 6.0/10│  →    │ 🟡 Moderate       │
│ Documentation         │ 7.0/10│  ↑    │ 🟢 Solid arch docs│
└─────────────────────────────────────────────────────────────┘

Legend:
  🔴 CRITICAL/MAJOR ISSUE
  🟠 HIGH-PRIORITY FIX NEEDED
  🟡 MEDIUM-PRIORITY IMPROVEMENT
  🟢 GOOD / ON TRACK
```

---

## Critical Issues (Must Fix)

### 1. Type Hints Coverage: <10%

**Impact**: IDE cannot autocomplete; refactoring blind; runtime errors
**Files Affected**: 140+ modules
**Effort**: 80 hours
**Priority**: 🔴 CRITICAL

```
Current state:
└─ ~75 type hints across 11,550 LOC
Expected:
└─ 500+ type hints (80% coverage)

Fix:
1. Run mypy/pyright to identify missing types
2. Add types to all public function signatures
3. Enable ANN101-ANN999 in ruff
4. Enforce in pre-commit hook
```

### 2. Insufficient Error Handling

**Impact**: Silent failures; poor user feedback; crash on edge cases
**Coverage**: Only ~55 try/except for 11,550 LOC (0.48%)
**Effort**: 40 hours
**Priority**: 🔴 CRITICAL

```
Problem areas:
├─ HTTP request execution (no timeout handling)
├─ JSON parsing (exceptions swallowed)
├─ File I/O (no permission checks)
├─ Credential validation (no format checks)
└─ Bare except: except: in main_window.py L122

Fix:
1. Audit all network operations for error cases
2. Add typed exception handlers (ConnectionError, Timeout, etc.)
3. Replace bare except with except Exception
4. Provide meaningful error messages to users
5. Add logging for all exception paths
```

### 3. Secrets in Plaintext

**Impact**: API keys vulnerable to theft; data breach risk
**Files Affected**: app_data.py, app_data_writer.py, storage
**Effort**: 20 hours
**Priority**: 🔴 CRITICAL
**Compliance**: OWASP A2 (Cryptographic Failures)

```
Current:
├─ Secrets stored in SQLite unencrypted
├─ Secrets logged via logging.debug(api_call)
├─ Secrets in JSON serialization
└─ Secrets visible in debugger/memory dump

Fix:
1. Encrypt sensitive fields at rest (use cryptography library)
2. Redact secrets from logging (no logging of full objects)
3. Redact secrets from to_json() serialization
4. Mask secrets in UI display (already partially done)
5. Use keyring library for OS credential storage (future)
6. Clear secrets from memory on app exit
```

### 4. Bare Except Clause

**Impact**: Catches SystemExit, KeyboardInterrupt; hard to debug
**Location**: [httprider/ui/main_window.py](httprider/ui/main_window.py#L122)
**Effort**: 1 hour
**Priority**: 🔴 CRITICAL (Quick win!)

```python
# CURRENT (BAD)
try:
    self.presenter.after_window_loaded()
except:
    traceback.print_exc()

# FIXED
try:
    self.presenter.after_window_loaded()
except Exception as e:
    logger.exception(f"Error in window load: {e}")
    # Show user-friendly error dialog
    QMessageBox.critical(self, "Error", "Failed to load window. Check logs.")
```

---

## High-Priority Issues (within 3 months)

### 5. <5% Test Coverage

**Impact**: Cannot safely refactor; regressions undetected; fragile
**Current**: 4 test files for 144 modules
**Target**: 50%+ coverage (80 test modules)
**Effort**: 100 hours
**Priority**: 🟠 HIGH

```
Coverage by layer:
├─ Core (interactors, models): 20–40% ← Need more
├─ Presenters: 0% (ZERO) ← CRITICAL GAP
├─ Exporters: 5% ← Need 20+
├─ Cache/persistence: 0% ← CRITICAL GAP
└─ Async/threading: 0% ← Hard but essential

Roadmap:
Phase 1 (Month 1):
  ├─ Add pytest-qt fixtures
  ├─ Create 10 presenter tests (mock app_settings)
  ├─ Create 5 cache tests
  └─ Automate with pytest --cov

Phase 2 (Month 2):
  ├─ Add 20 exporter tests
  ├─ Add async execution tests
  └─ Target 40% coverage

Phase 3 (Month 3):
  ├─ Presenter decouple (enable unit tests)
  ├─ Add 30+ unit tests
  └─ Target 60% coverage
```

### 6. God Object: `core/__init__.py` (312 lines)

**Impact**: Difficult to find utilities; poor code organization; coupling
**Contains**: 50+ unrelated functions
**Effort**: 15 hours
**Priority**: 🟠 HIGH

```
Current structure:
core/__init__.py
├─ UUID utils (gen_uuid, abbreviate)
├─ Template/variable substitution (template_sub, evaluate_nested_functions)
├─ JSON utilities (json_path, format_json, compact_json)
├─ Formatting (elapsed_time_formatter, response_code_formatter)
├─ Encoding (str_to_base64, mask_secret, rot13)
├─ Type conversion (str_to_int, str_to_bool)
├─ Request utilities (combine_request_headers, replace_variables)
└─ File/path utilities (truncate, split_url_qs)

Refactored:
core/
├─ __init__.py (re-exports for backward compat)
├─ uuid_utils.py (gen_uuid, abbreviate)
├─ template_utils.py (template_sub, variable substitution)
├─ json_utils.py (json_path, format_json)
├─ encoding_utils.py (base64, rot13, mask_secret)
├─ request_utils.py (combine headers, replace variables)
├─ type_utils.py (type conversion)
└─ path_utils.py (truncate, split_url_qs)
```

### 7. Wildcard Imports (46 instances)

**Impact**: Name collisions; unclear dependencies; poor linting
**Effort**: 10 hours
**Priority**: 🟠 HIGH

```
Current (BAD):
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from httprider.core.constants import *

Fixed:
from PyQt6.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QListView, QMainWindow, QMessageBox, QFileDialog,
)
from httprider.core.constants import DEFAULT_TAG, ENVIRONMENT_RECORD_TYPE

Also:
└─ Remove ANN and F403/F405 from ruff ignore list
```

### 8. Presenter Testing Barrier

**Impact**: Cannot unit test any presenter; no confidence in refactors
**Root Cause**: Presenters inherit PyQt patterns; cannot instantiate without QApplication
**Effort**: 30 hours (decouple) + 50 hours (add tests)
**Priority**: 🟠 HIGH

```
Phase 1: Extract presenter logic to separate layer
┌─ Current ────────────┐
│ Presenter            │ ← Tightly bound to Qt widgets
│ __init__(parent_view)│ ← Needs QMainWindow reference
│ self.view.btn_send  │ ← Direct widget access
└─────────────────────┘

┌─ Target ──────────────────────────────┐
│ RequestPresenterModel (pure logic)    │
│ ├─ __init__(callback_handler)         │
│ ├─ on_send_request(form_data)         │
│ └─ get_form_data() -> dict             │
│                                        │
│ RequestPresenter (Qt layer)            │
│ ├─ __init__(parent_view, model)       │
│ ├─ wireup() → self.view.btn_send → .. │
│ └─ delegate to model                   │
└────────────────────────────────────────┘

Phase 2: Test logic independently
def test_request_presenter_logic():
    model = RequestPresenterModel(on_success=mock)
    model.on_send_request({
        'url': 'http://...',
        'method': 'GET'
    })
    # Assert without QApplication
```

---

## Medium-Priority Issues (6–12 months)

### 9. Sequential HTTP Requests (No Parallelization)

**Impact**: User waits for each request; slow load testing
**Current**: One QThread worker; queue processes one at a time
**Target**: Worker pool (configurable 1–10 workers)
**Effort**: 30 hours
**Priority**: 🟡 MEDIUM

```
Design proposal:
class WorkerPool(QObject):
    def __init__(self, num_workers=3):
        self.workers = [RestApiConnector(...) for _ in range(num_workers)]
        self.queue = Queue()

    def submit_request(self, api_call):
        self.queue.put(api_call)
        self.__distribute_work()

    def __distribute_work(self):
        for worker in self.workers:
            if worker.idle and not self.queue.empty():
                request = self.queue.get()
                worker.execute(request)

Benefit:
├─ Run 3–10 requests in parallel
├─ Useful for load testing
└─ Still serializable per request (for dependent chains)
```

### 10. Tight Presenter-to-Qt Coupling

**Impact**: Hard to extract business logic; presenters not testable
**Affected**: 30+ presenter modules
**Effort**: 150 hours (significant refactor)
**Priority**: 🟡 MEDIUM (long-term)

```
Strategy: Dependency Injection
Current:
  Presenter(MyWindow) → MyWindow.txt_url, MyWindow.btn_send, ...

Target:
  Presenter(form_model, action_handler)
  ├─ form_model provides: get_url(), set_url(val), ...
  └─ action_handler receives: on_send_request(request)

Presenter doesn't know it's Qt; just knows abstract interface.

Benefits:
├─ Can test without Qt
├─ Can swap UI (web, CLI, mobile)
└─ Cleaner MVVM or MVC pattern
```

### 11. Insufficient Validation

**Impact**: Invalid inputs may crash; header injection; URL injection
**Areas**: URL, headers, JSON paths, file paths
**Effort**: 15 hours
**Priority**: 🟡 MEDIUM

```
Checklist:
├─ URL validation (use urllib.parse.urlparse)
├─ Header validation (no \r\n injection)
├─ JSON path validation (jsonpath_ng safety)
├─ File path validation (no path traversal)
├─ Port validation (1–65535)
├─ Content-Type header validation
└─ Request body size limits
```

### 12. PyQt6 Version Pinning

**Impact**: Breaking changes in PyQt6 7.0; hard to debug
**Current**: `PyQt6` (unpinned; auto-upgrades)
**Target**: `PyQt6>=6.4,<7.0`
**Effort**: 1 hour
**Priority**: 🟡 MEDIUM (preventive)

---

## Low-Priority Issues (12+ months, nice-to-have)

### 13. Documentation Gaps

**Current**:

- ✅ [ARCHITECTURE.md](ARCHITECTURE.md) — Excellent
- ✅ [EXECUTION_TRACES.md](EXECUTION_TRACES.md) — Great
- ✅ [FEATURE_ANALYSIS.md](FEATURE_ANALYSIS.md) — Comprehensive
- ❌ No code docstrings (`"""..."""`)
- ❌ No contribution guidelines
- ❌ No API documentation (Sphinx)

**Effort**: 20 hours
**Priority**: 🟢 LOW

### 14. Memory Scalability

**Current Limit**: ~50MB projects (all in memory)
**Target**: Lazy-load exchanges; support 500+ API calls
**Effort**: 40 hours
**Priority**: 🟢 LOW (not immediate blocker)

---

## Risk Assessment Matrix

```
┌────────────────────┬──────────┬─────────────────────────┐
│ Risk               │ Severity │ Current Mitigation      │
├────────────────────┼──────────┼─────────────────────────┤
│ Secrets theft      │ 🔴 HIGH  │ ???                     │
│ Refactoring breaks │ 🔴 HIGH  │ Manual testing (fragile)│
│ Silent failures    │ 🔴 HIGH  │ User sees generic errors│
│ PyQt lock-in       │ 🟠 MED   │ Architecture stable ✓   │
│ Large projects     │ 🟠 MED   │ Not target audience     │
│ Import chaos       │ 🟡 LOW   │ Ruff linting (ignored)  │
│ Person dependency  │ 🟡 LOW   │ Open source; community  │
└────────────────────┴──────────┴─────────────────────────┘
```

---

## Implementation Timeline

### MONTH 1 (Stability & Security)

```
Week 1:
  □ Add type hints to core APIs (interactors, models)
  □ Fix bare except clause in main_window.py
  □ Encrypt secrets at rest (prototyp cryptography lib)

Week 2:
  □ Redact secrets from logging
  □ Redact secrets from JSON serialization
  □ Enable ANN in ruff (fail on missing types)

Week 3:
  □ Add comprehensive error handling to HTTP execution
  □ Add error handling to JSON parsing
  □ Create error handling patterns document

Week 4:
  □ Add 5–10 presenter tests with pytest-qt
  □ Set up pytest --cov in CI
  □ Document "How to Test" in CONTRIBUTING.md

Deliverables:
├─ 300+ type annotations
├─ 20+ try/except blocks
├─ Secrets encrypted
└─ Bare except fixed
```

### MONTH 2 (Testability)

```
Week 1–2:
  □ Refactor core/__init__.py into submodules
  □ Replace all wildcard imports with explicit imports

Week 3:
  □ Remove F403, F405, ANN from ruff ignore
  □ Force CI to enforce type hints

Week 4:
  □ Add 20–30 exporter tests
  □ Add 10–15 cache/persistence tests
  □ Target 40% coverage

Deliverables:
├─ core/__init__.py → 5 submodules
├─ 0 wildcard imports
├─ 40% test coverage
└─ All types enforced
```

### MONTH 3 (Scalability & Polish)

```
Week 1–2:
  □ Prototype presenter decouple (extract logic layer)
  □ Add validation to URL, headers, file paths

Week 3:
  □ Add unit tests for decoupled presenter logic
  □ Document presenter testing patterns

Week 4:
  □ Pin PyQt6 version
  □ Review all error messages for user clarity
  □ 60% test coverage target

Deliverables:
├─ First 5 presenters decoupled + testable
├─ Input validation throughout
├─ 60% coverage
└─ User-friendly error messages
```

---

## Success Metrics

| Metric              | Current   | Target      | Timeline |
| ------------------- | --------- | ----------- | -------- |
| Type Hints Coverage | <10%      | 80%         | Month 1  |
| Test Coverage       | <5%       | 60%         | Month 3  |
| Exceptions/100 LOC  | 0.48      | 3.0         | Month 1  |
| Error Handling      | 55 blocks | 200+ blocks | Month 2  |
| Wildcard Imports    | 46        | 0           | Month 2  |
| Bare Excepts        | 1         | 0           | Week 1   |
| Secrets Encrypted   | ❌        | ✅          | Week 2   |
| Presenter Tests     | 0         | 30+         | Month 3  |
| Code Quality Score  | 6.4/10    | 8.5+/10     | Month 3  |

---

## Resources & References

- **Python Type Hints**: [PEP 484](https://www.python.org/dev/peps/pep-0484/), [MyPy Docs](https://mypy.readthedocs.io/)
- **Testing**: [pytest Docs](https://docs.pytest.org/), [pytest-qt](https://pytest-qt.readthedocs.io/)
- **Secrets**: [cryptography.io](https://cryptography.io/), [keyring](https://keyring.readthedocs.io/)
- **Security**: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- **Code Quality**: [ruff Docs](https://docs.astral.sh/ruff/), [black Docs](https://black.readthedocs.io/)

---

**Prepared**: March 22, 2026
**Assessment Grade**: 6.4/10 (FAIR)
**Next Review**: After Month 1 implementation

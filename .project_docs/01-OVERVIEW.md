# HTTP-Rider: Project Overview

**HTTP-Rider** is a cross-platform desktop client for REST API testing, documentation, and code generation. Think of it as an open-source alternative to Postman with a focus on test automation, code generation, and API documentation.

## Quick Facts

| Property             | Value                                                                |
| -------------------- | -------------------------------------------------------------------- |
| **Project Name**     | HTTP-Rider                                                           |
| **Version**          | 0.6.4                                                                |
| **License**          | MIT                                                                  |
| **Repository**       | [github.com/namuan/http-rider](https://github.com/namuan/http-rider) |
| **Primary Language** | Python 3.11+                                                         |
| **GUI Framework**    | PyQt6                                                                |
| **Target Platforms** | macOS, Windows, Linux                                                |
| **Project Type**     | Desktop Application (GUI)                                            |
| **Code Size**        | ~11,550 lines of Python                                              |
| **Module Count**     | ~40 modules, 9 subsystems                                            |

## What It Does

### 🎯 Core Capabilities

1. **REST API Testing**

   - Create and edit HTTP requests (GET, POST, PUT, DELETE, PATCH, etc.)
   - Send requests and inspect responses
   - View request/response headers, status codes, and body content
   - Request history tracking and re-execution

2. **Advanced Testing Features**

   - **Assertions/Validations** (10 matcher types)
     - Assert response status, headers, body content (regex, JSON path)
     - Response time assertions
     - Variable extraction from responses
   - **Environments** - Manage API keys, base URLs, and variables per environment
   - **Data Generation** - Faker-based test data (names, emails, addresses, UUIDs)
   - **Fuzzing/Chaos Testing** - Automated request mutation and testing

3. **Code Generation (16+ Export Formats)**

   - **Languages**: Python (requests), Java (Feign, RestAssured, Spring Boot), JavaScript
   - **Testing Frameworks**: Locust, RestAssured, Spring Cloud Contract Tests
   - **Standards**: OpenAPI 3.0, Postman Collection
   - **Other**: cURL, Markdown documentation, Mermaid diagrams, PlantUML, ApicKli

4. **API Import**

   - Import from cURL commands
   - Import from Postman Collections
   - Import from OpenAPI 3.0 specifications

5. **Organization & Discovery**

   - Projects for grouping related APIs
   - Tag-based filtering and search
   - Tree-structured API organization

6. **UI/UX Features**
   - Syntax highlighting (JSON, XML, etc.)
   - Pretty-print formatting
   - Light and dark themes
   - Keyboard shortcuts

## Architecture Highlights

### Design Philosophy: Signal-Driven MVP

HTTP-Rider uses a **6-layer signal-driven Model-View-Presenter architecture**:

```
┌─────────────────────────────────────────┐
│  UI Layer (PyQt6)                       │
│  ├─ Main Window                         │
│  ├─ Dialogs                             │
│  └─ Widgets                             │
├─────────────────────────────────────────┤
│  Presenter Layer (MVP - 30+ presenters) │
│  └─ Handles UI events & data binding    │
├─────────────────────────────────────────┤
│  Core Business Logic                    │
│  ├─ API execution                       │
│  ├─ Data generation                     │
│  └─ Assertions                          │
├─────────────────────────────────────────┤
│  Model (Data Structures)                │
│  └─ ApiCall, HttpExchange, Response    │
├─────────────────────────────────────────┤
│  Storage (SQLite + In-Memory Cache)     │
│  └─ Persistence + Fast filtering        │
├─────────────────────────────────────────┤
│  External APIs                          │
│  ├─ HTTP client (requests library)      │
│  ├─ Importers (3 formats)               │
│  └─ Exporters (16+ formats)             │
└─────────────────────────────────────────┘
```

### Key Architectural Principles

1. **Signal-Driven Reactivity** - All UI updates driven by PyQt signals, not direct calls
2. **One-Way Data Flow** - Interactor → Database → Signal → Cache → UI
3. **Plugin System** - Exporters and importers are auto-discovered; easy to add new formats
4. **Async HTTP Execution** - Non-blocking requests via QThread worker
5. **In-Memory Caching** - SQLite for persistence, Python dicts for fast queries/filtering

## Technology Stack

### Core Dependencies

- **PyQt6** - Desktop GUI framework
- **requests** - HTTP client library
- **dataset** - SQLite abstraction layer
- **Faker** - Test data generation
- **prance** - OpenAPI parsing
- **attrs & cattrs** - Data serialization

### Development Tools

- **uv** - Fast Python package manager
- **pytest** - Testing framework
- **black** - Code formatter
- **ruff** - Linter
- **pyinstaller** - Desktop app bundler
- **pre-commit** - Git hooks

### Build & Packaging

- **Makefile** - Development commands (install, run, test, package)
- **PyInstaller** - Builds standalone `.app`, `.exe`, `.AppImage`
- **Install scripts** - macOS bundler ([install-macosx.sh](scripts/install-macosx.sh))

## Project Statistics

| Metric                 | Value                                                                             |
| ---------------------- | --------------------------------------------------------------------------------- |
| **Total LOC**          | ~11,550                                                                           |
| **Module Count**       | ~40                                                                               |
| **Test Files**         | 4                                                                                 |
| **Test Coverage**      | ~4% ⚠️                                                                            |
| **Code Quality Score** | 6.4/10 (Fair)                                                                     |
| **Major Subsystems**   | 9 (core, ui, model, presenters, external, exporters, importers, codegen, widgets) |
| **Presenter Count**    | 30+                                                                               |
| **Exporter Formats**   | 16+                                                                               |
| **Python Version**     | 3.11+                                                                             |

## Module Organization

### Core Subsystems

| Subsystem                | Purpose                                         | Key Files                                                                     |
| ------------------------ | ----------------------------------------------- | ----------------------------------------------------------------------------- |
| **httprider/core**       | Business logic (API execution, data generation) | `api_call_interactor.py`, `json_data_generator.py`, `app_state_interactor.py` |
| **httprider/model**      | Data structures and persistence                 | `app_data.py`, `storage.py`, `app_configuration.py`                           |
| **httprider/ui**         | Main window and dialogs                         | `main_window.py`, `dialog_*.py`                                               |
| **httprider/widgets**    | Reusable UI components                          | `api_calls_list_view.py`, `json_tree_widget.py`                               |
| **httprider/presenters** | MVP controllers (30+ files)                     | `main_presenter.py`, `request_presenter.py`                                   |
| **httprider/external**   | HTTP client and networking                      | `rest_api_connector.py`, `requester.py`                                       |
| **httprider/exporters**  | Code generation (16+ formats)                   | `exporter_*.py`                                                               |
| **httprider/importers**  | API import (3 formats)                          | `importer_*.py`                                                               |
| **httprider/codegen**    | Code generation utilities                       | `schema_to_java_generator.py`                                                 |

## Getting Started

### Prerequisites

- Python 3.11+
- `uv` package manager (macOS: `brew install uv`)

### Installation & Running

```bash
# Install dependencies
make install

# Run the application
make run

# Run tests
make test

# Check code quality
make check

# Build packaged application
make package
```

### First Steps for Developers

1. Clone repository
2. Run `make install` to set up environment
3. Run `make run` to launch the app
4. Read [Developer Guide](09-DEVELOPER_GUIDE.md) for contribution guidelines
5. Review [System Architecture](02-ARCHITECTURE.md) for code organization

## Current State & Quality

### Strengths ✅

- **Clean Architecture** - Well-separated MVP pattern with signal-driven reactivity
- **Feature-Rich** - 16+ export formats, 3 import formats, comprehensive assertion system
- **Plugin System** - Easy to extend with new exporters/importers
- **Modern Build** - Uses modern tools (uv, ruff, type checking ready)
- **Cross-Platform** - Builds for macOS, Windows, Linux

### Areas for Improvement 🔴

- **Testing** - Only ~4% test coverage; virtually no unit tests for presenters
- **Type Hints** - <10% coverage; no IDE autocomplete benefits
- **Error Handling** - Minimal input validation; cryptic error messages
- **Security** - API keys stored unencrypted; logged in plaintext
- **Scalability** - Sequential request processing; ~50MB SQLite limit

### Quality Score: 6.4/10 (Fair)

See [Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md) for detailed analysis and improvement roadmap.

## Team & Governance

- **Maintainer**: Namuan (GitHub)
- **License**: MIT (open-source friendly)
- **Contributing**: Pull requests welcome
- **Development**: Active, feature development ongoing
- **Community**: Growing user base

## Roadmap & Vision

### Short Term (3 months)

1. Improve test coverage (target: 40%)
2. Add type hints to all public APIs
3. Encrypt credentials at rest
4. Fix security audit findings

### Medium Term (6 months)

1. Decouple GUI from business logic (improve testability)
2. Add request templating/scripting
3. Performance optimization for large projects
4. Parallel request execution

### Long Term (12+ months)

1. Web-based version
2. Team/cloud sync features
3. CI/CD integration
4. Workflow automation

## Key Facts for Decision Makers

| Question                               | Answer                                                                                   |
| -------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Is this production-ready?**          | Yes, for individual users. Team features not yet available.                              |
| **Is this being actively maintained?** | Yes, regular updates and feature additions.                                              |
| **Can we rely on this long-term?**     | Yes, but needs investment in testing and security before enterprise use.                 |
| **What are the risks?**                | Low test coverage, unencrypted credentials, PyQt6 dependency.                            |
| **How hard is it to extend?**          | Easy for exporters/importers. Medium for core features.                                  |
| **Comparison to Postman?**             | Similar core features, no team collaboration, better code generation for some languages. |

## Additional Resources

- **Full Architecture Documentation**: [02-ARCHITECTURE.md](02-ARCHITECTURE.md)
- **Module Dependencies**: [03-MODULE_MAP.md](03-MODULE_MAP.md)
- **Execution Traces**: [04-EXECUTION_TRACES.md](04-EXECUTION_TRACES.md)
- **Complete Feature List**: [05-FEATURE_ANALYSIS.md](05-FEATURE_ANALYSIS.md)
- **Quality Audit**: [07-CODE_QUALITY_ASSESSMENT.md](07-CODE_QUALITY_ASSESSMENT.md)
- **Developer Setup**: [09-DEVELOPER_GUIDE.md](09-DEVELOPER_GUIDE.md)

---

_For questions or clarifications, refer to the documentation index in [README.md](README.md)._

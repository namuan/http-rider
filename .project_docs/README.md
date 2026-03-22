# HTTP-Rider Project Documentation

Comprehensive technical documentation for the HTTP-Rider desktop REST API client application.

## Quick Navigation

### 📋 **Start Here**

- **[Reading Guide](#reading-guide)** - Choose documentation based on your role
- **[Project Overview](01-OVERVIEW.md)** - Executive summary, project goals, and key facts

### 🏗️ **Architecture & Design**

- **[System Architecture](02-ARCHITECTURE.md)** - High-level design, patterns, philosophies
- **[Module Map](03-MODULE_MAP.md)** - Detailed module dependencies and relationships
- **[Execution Traces](04-EXECUTION_TRACES.md)** - Step-by-step tracing of critical flows

### ✨ **Features & Capabilities**

- **[Feature Analysis](05-FEATURE_ANALYSIS.md)** - Complete inventory of user-facing features
- **[Feature Architecture](06-FEATURE_ARCHITECTURE.md)** - How features are implemented

### 🔧 **Development & Quality**

- **[Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md)** - Engineering health, risks, and technical debt
- **[Implementation Roadmap](08-ROADMAP.md)** - Recommendations for improvements
- **[Developer Guide](09-DEVELOPER_GUIDE.md)** - Getting started for contributors

---

## Reading Guide

Choose your starting point based on your role:

### 👨‍💼 **Project Managers / Business Stakeholders**

1. [Project Overview](01-OVERVIEW.md) - 5 min read
2. [Feature Analysis](05-FEATURE_ANALYSIS.md) - Skim the feature table (15 min)
3. [Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md) - Executive Summary section only (10 min)

**Total**: 30 minutes | **Goal**: Understand what the product does and its current health

---

### 🏗️ **Architects / Tech Leads**

1. [Project Overview](01-OVERVIEW.md) - 5 min
2. [System Architecture](02-ARCHITECTURE.md) - Full read (25 min)
3. [Module Map](03-MODULE_MAP.md) - Skim diagrams, read subsystem descriptions (15 min)
4. [Execution Traces](04-EXECUTION_TRACES.md) - Read "App Startup" and "Send Request" flows (15 min)
5. [Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md) - Focus on "Architecture Health" section (10 min)

**Total**: 70 minutes | **Goal**: Understand system design and architectural decisions

---

### 👨‍💻 **New Developers / Contributors**

1. [Project Overview](01-OVERVIEW.md) - Full read (5 min)
2. [Developer Guide](09-DEVELOPER_GUIDE.md) - Full read (20 min)
3. [System Architecture](02-ARCHITECTURE.md) - Read sections 1-3 (15 min)
4. [Module Map](03-MODULE_MAP.md) - Read "Module Summary" and study diagrams (15 min)
5. Pick a feature:
   - [Feature Code Reference](06-FEATURE_CODE_REFERENCE.md) - Find your feature (5 min)
   - [Execution Traces](04-EXECUTION_TRACES.md) - Read relevant flow (10 min)

**Total**: 70 minutes | **Goal**: Understand codebase enough to make first PR

---

### 🔍 **Code Reviewers**

1. [Module Map](03-MODULE_MAP.md) - 5 min (refresh module relationships)
2. [Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md) - Full read (30 min)
3. [System Architecture](02-ARCHITECTURE.md) - Section "Critical Principles for Developers" (5 min)

**Total**: 40 minutes | **Goal**: Know code quality standards and architectural constraints

---

### 🚀 **Performance Engineers / DevOps**

1. [Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md) - "Performance & Scalability" section (10 min)
2. [Execution Traces](04-EXECUTION_TRACES.md) - Read performance implications (10 min)
3. [System Architecture](02-ARCHITECTURE.md) - "Performance Decisions" section (10 min)

**Total**: 30 minutes | **Goal**: Understand scaling limits and optimization points

---

## Key Facts at a Glance

| Aspect                | Detail                                           |
| --------------------- | ------------------------------------------------ |
| **Language**          | Python 3.11+                                     |
| **Framework**         | PyQt6 (Desktop GUI)                              |
| **Architecture**      | Signal-Driven MVP + Layered                      |
| **Module Count**      | ~40 modules, 9 core subsystems                   |
| **Test Coverage**     | ~4% (critical improvement area)                  |
| **Code Quality**      | 6.4/10 (Fair)                                    |
| **Lines of Code**     | ~11,550 (Medium codebase)                        |
| **Key Dependencies**  | PyQt6, requests, faker, dataset, attrs           |
| **Build Tool**        | PyInstaller, `uv` package manager                |
| **Supported Exports** | 16+ formats (Java, Python, OpenAPI, etc.)        |
| **Primary Use Case**  | REST API testing, documentation, code generation |
| **Maturity**          | v0.6.4 - Active development                      |

---

## Document Descriptions

### 01-OVERVIEW.md

Executive summary of the project. What it does, why it matters, key metrics, and project status.

### 02-ARCHITECTURE.md

Deep dive into system design. Explains the signal-driven MVP architecture, design patterns, why decisions were made, and critical principles for developers.

### 03-MODULE_MAP.md

Detailed breakdown of all ~40 modules: dependencies, responsibilities, key classes, and data flow pathways.

### 04-EXECUTION_TRACES.md

Step-by-step execution paths through the system. Covers app startup, sending requests, importing APIs, exporting code, and more. Shows actual file paths, method names, and signal emissions.

### 05-FEATURE_ANALYSIS.md

Complete feature inventory organized by category. Covers 100+ features across 12 categories: core testing, advanced testing, code generation, imports/exports, organization, configuration, etc.

### 06-FEATURE_ARCHITECTURE.md

How features are implemented. Shows MVP hierarchy, signal flow, and code entry points for each major feature.

### 07-CODE_QUALITY_ASSESSMENT.md

Comprehensive code quality audit. Identifies risks, technical debt, code metrics, security concerns, testing gaps, and provides remediation recommendations.

### 08-ROADMAP.md

8-week improvement roadmap based on quality assessment. Prioritizes critical fixes, testability improvements, and scaling enhancements.

### 09-DEVELOPER_GUIDE.md

Getting started guide for new developers. How to set up dev environment, understand code structure, make your first change, and contribute.

---

## How to Use This Documentation

### For Understanding a Specific Feature

1. Search [Feature Code Reference](06-FEATURE_CODE_REFERENCE.md) for feature name
2. Note the files involved
3. Read the relevant execution trace in [Execution Traces](04-EXECUTION_TRACES.md)
4. Review files using [Module Map](03-MODULE_MAP.md) for context

### For Making an Architectural Change

1. Read [System Architecture](02-ARCHITECTURE.md) "Critical Principles" section
2. Check [Module Map](03-MODULE_MAP.md) for affected modules
3. Review [Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md) for related issues
4. Check [Execution Traces](04-EXECUTION_TRACES.md) for ripple effects

### For Debugging an Issue

1. Locate the feature in [Feature Code Reference](06-FEATURE_CODE_REFERENCE.md)
2. Trace execution path in [Execution Traces](04-EXECUTION_TRACES.md)
3. Check error handling in [Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md) for known issues
4. Review relevant presenter/interactor in actual source files

### For Performance Optimization

1. Check [Code Quality Assessment](07-CODE_QUALITY_ASSESSMENT.md) "Performance" section
2. Read [Execution Traces](04-EXECUTION_TRACES.md) for performance characteristics
3. Review [System Architecture](02-ARCHITECTURE.md) "Performance Decisions" section

---

## Quick Links

- **Project Repository**: [namuan/http-rider](https://github.com/namuan/http-rider)
- **Python Version**: 3.11+
- **Build Command**: `make install && make run`
- **Test Command**: `make test`
- **Code Quality**: `make check`

---

## Contributing

See [Developer Guide](09-DEVELOPER_GUIDE.md) for contribution guidelines.

---

_Documentation generated on: March 22, 2026_
_For updates, consult the project repository and architecture team._

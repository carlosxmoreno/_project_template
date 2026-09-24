# 03 - Architecture — {{PROJECT_NAME}}

<!-- This document defines the HOW of the system: components, structure, dependencies
     and design decisions. Architectural choices have a direct impact on maintainability,
     portability and performance efficiency (ISO/IEC 25010). Record every significant
     decision here so it can be reviewed and challenged.
     Requirements that drive architectural decisions are in 02-requirements.md. -->

## Component diagram

```
<!-- Draw a simple ASCII diagram of the main components and their relationships -->
```

## Components

<!-- Describe each component: responsibility, inputs, outputs, key decisions -->

### 1. <!-- Component name -->
-

## Technical constraints

- Language: Python
- <!-- Add constraints: free/opensource only, lightweight, local LLM, etc. -->

## Design decisions

<!-- Record each significant design decision and its rationale -->
<!-- Use this format: -->
<!-- - **Decision**: what was decided -->
<!-- - **Rationale**: why -->
<!-- - **Alternatives considered**: what else was evaluated -->

## File naming conventions

<!-- Define prefixes or patterns for source files if applicable -->
<!-- Example from Ports & Adapters pattern: -->
<!-- - `core_`    → Interfaces (ABCs) -->
<!-- - `adapter_` → Concrete implementations -->
<!-- - `orch_`    → Orchestrator -->

## Project structure

```
{{PROJECT_NAME}}/
├── specs/                  → Specification documents
├── config/                 → YAML configuration files
├── data/                   → Input/output data
├── logs/                   → Runtime logs
├── references/             → External reference documents
├── src/                    → Source code
├── tests/
│   ├── unit/
│   ├── integration/
│   └── sandbox/            → Throwaway scripts
├── utilities/
│   ├── logger.py
│   ├── timestamp.py
│   └── api_errors.py
├── .amazonq/rules/dev-rules.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Utilities

Three shared modules are provided by the project template and available from the start:

- `utilities/logger.py` — logging with timestamp, level and caller name. Writes to stdout/stderr and to `logs/<project>.log`. Call `configure()` at startup.
- `utilities/timestamp.py` — generates a `ddmmyy_HHMM` timestamp string for output file naming (`now_stamp()`).
- `utilities/api_errors.py` — classifies LLM API HTTP errors: `is_retryable(error)` and `error_message(error)`. Compatible with any exception that exposes `status_code` and `model_name`.

All three have no external dependencies.

## Main dependencies

```
# Add dependencies as they are decided
# pyyaml     → YAML configuration
# pathlib    → built-in, cross-platform paths
```

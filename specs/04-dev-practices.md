# 04 - Development Practices — {{PROJECT_NAME}}

<!-- This document defines HOW the team works: design principles, coding standards,
     testing strategy, branching, commits and review criteria. It operationalises the
     quality attributes defined in 02-requirements.md § Quality attributes (ISO/IEC 25010),
     particularly maintainability, reliability and security. -->

## Design principles

<!-- Foundational guidelines that drive every design and implementation decision.
     Maps to: ISO/IEC 25010 — Maintainability (modularity, reusability, modifiability). -->

- **Single Responsibility (SRP)**: each module, class or function does one thing.
- **Separation of Concerns**: business logic, I/O, configuration and presentation
  live in separate layers. Never mix them.
- **High cohesion, low coupling**: a component's internals are closely related;
  its dependencies on other components are minimal and explicit.
- **Dependency Inversion**: depend on abstractions (protocols / interfaces),
  not on concrete implementations. Inject dependencies; do not instantiate them
  inside the consumer.
- **Composition over inheritance**: prefer composing behaviours via delegation
  rather than deep class hierarchies.
- **DRY** (Don't Repeat Yourself): extract shared logic into a single source of truth.
  Check for existing implementations before creating new ones.
- **YAGNI** (You Aren't Gonna Need It): implement only what is required by the
  current approved increment. Do not build for speculative future needs.
- **Immutability by default**: prefer `dataclass(frozen=True)`, `NamedTuple`
  or read-only structures. Mutate only when the design explicitly requires it.

## General rules

- All configuration in YAML files. No hardcoded values in code.
- No emojis in code or any project file.
- When in doubt, ask before acting.
- Before making a change, propose it and wait for approval.

## Code style

### Linter and formatter
- ruff (lint + format, configured in `pyproject.toml`)
- Run: `ruff check .` and `ruff format .`

### Naming
- Variables and functions: snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Files: prefix + snake_case (see conventions in 03-architecture.md)

### Imports
- Order: stdlib → third-party → local
- ruff handles this automatically

### Type hints
- Use type annotations on all public function signatures (parameters and return type).
- Use modern syntax (`list[str]`, `X | None`) for Python ≥ 3.10.
  Import from `typing` only when targeting older runtimes.
- Run a type checker (mypy or pyright) when the project reaches integration maturity.

## Code documentation

### Docstrings
- Format: Google style.
- Required in: module header, classes, public methods and functions.

### Module header
Every source file must include a top-level docstring:
```python
"""
{{PROJECT_NAME}} - <brief module description>
Component: <core|adapter|orch|cli|config|...>
"""
```

### README
- One README.md at the root: project description, how to install, how to run.
- Update when something relevant changes.

## Error handling

### Exceptions
- Define custom exceptions per component when they add clarity.
- For generic errors (file not found, invalid config): use standard Python exceptions.

### Logging
- Use `utilities/logger.py` in all components.
- Levels: INFO for normal operations, WARNING for recoverable situations, ERROR for failures.
- Never use `print()` for status messages; only for direct user output.

## Testing

### Framework
- pytest

### Structure
```
tests/
├── unit/
├── integration/
└── sandbox/
```

### Naming conventions
- Files: `test_<module_name>.py`
- Functions: `test_<expected_behaviour>()`

### Testing strategy
- **Unit**: each component in isolation. May use simplified data.
- **Integration**: combined components. Always with real data.
- **End-to-end**: full flow as the user would experience it.

### Rules
- Do not create a test script without checking if an existing one covers the same purpose.
- Each component must have at least one unit test.
- Tests always produce verifiable output on disk.
- Run all tests before merging to main.

### When to run tests
- **Unit**: every time a component is modified.
- **Integration**: when a new component is added, an adapter changes, or config parameters change.
- **Regression (all)**: before merge to main, and when refactoring shared code.

## Security

<!-- Pre-written baseline rules that apply to every project.
     Extend this section with project-specific rules as needed.
     Maps to: ISO/IEC 25010 — Security (confidentiality, integrity, non-repudiation). -->

- Never commit credentials, API keys or secrets to the repository.
- All secrets go in `.env` (excluded from git via `.gitignore`). Use `.env.example` as the template.
- Validate all external inputs before processing (files, API responses, user arguments).
- Do not log sensitive data (keys, tokens, personal information).
- Dependencies: review before adding. Prefer well-maintained packages with known provenance.
- If the project exposes an API: authenticate all endpoints; never expose internal errors to callers.

## Performance

<!-- Pre-written baseline guidelines. Define project-specific targets in
     02-requirements.md § Quality attributes — Performance efficiency.
     Maps to: ISO/IEC 25010 — Performance efficiency (time behaviour, resource utilisation). -->

- Log execution time for any operation expected to take > 1 s.
- Do not load entire datasets into memory if streaming or pagination is feasible.
- Avoid redundant LLM calls: cache or reuse results within a session where correct to do so.
- Define a response time target per operation in 02-requirements.md before optimising.
- Profile before optimising: measure first, then act.

## Dependency management

- `pyproject.toml` is the single source of truth for project metadata and dependencies.
- Pin direct dependencies to a compatible range (e.g. `pydantic>=2.0,<3`).
- Review changelogs before upgrading a dependency.
- Run `pip-audit` or equivalent to check for known vulnerabilities before releases.

## Branching and commits

### Strategy
- `main`: tested and functional code
- `dev`: work in progress

### Flow
```
dev (work) → tests pass locally → merge to main → push
```

### Commit messages
Format: `<type>: <short description>`

Types:
- `feat:` — new functionality
- `fix:` — bug fix
- `spec:` — specification change
- `refactor:` — restructuring without functional change
- `test:` — add or modify tests
- `docs:` — documentation
- `config:` — configuration changes

## Code review

- Each increment is proposed before implementing.
- After implementing, reviewed together (VERIFY step).
- Criteria to accept an increment:
  - Tests pass
  - Docstrings present
  - No hardcoded values
  - No duplication
  - Complies with the corresponding spec

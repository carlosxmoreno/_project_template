# 04 - Development Practices — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 04-dev-practices.md as your starting point. -->

## General principles

- All configuration in YAML files. No hardcoded values in code.
- Do not duplicate methods or services. Check before creating.
- No emojis in code or any project file.
- When in doubt, ask before acting.
- Before making a change, propose it and wait for approval.

## Testing

### Framework
- pytest

### Structure
```
tests/
├── unit/
│   ├── test_pdf_extractor.py
│   ├── test_llm_parser.py
│   └── test_csv_exporter.py
├── integration/
│   └── test_pipeline.py
└── sandbox/
```

### Naming conventions
- Files: `test_<module_name>.py`
- Functions: `test_<expected_behaviour>()`

### Testing strategy
- **Unit**: each component in isolation. pdf_extractor and csv_exporter use fixture files. llm_parser uses a mock LLM response.
- **Integration**: full pipeline with real PDFs from references/. Requires LLM API key.
- **End-to-end**: `python main.py --input references/ --output data/output/test.csv` and inspect output.

### Rules
- Do not create a test script without checking if an existing one covers the same purpose.
- Each component (pdf_extractor, llm_parser, csv_exporter) must have at least one unit test.
- Tests always produce verifiable output on disk (CSV or log file).
- Run all tests before merging to main.

### When to run tests
- **Unit**: every time a component is modified.
- **Integration**: when llm.yaml changes (model or prompt), when a new PDF format is added.
- **Regression (all)**: before merge to main.

## Code documentation

### Docstrings
- Format: Google style.
- Required in: module header, classes, public methods and functions.

### Module header
Every script must include:
```python
"""
InvoiceParser - <brief module description>
Version: 0.1.0
Component: <pdf_extractor|llm_parser|csv_exporter|cli|config>
"""
```

### README
- One README.md at the root: project description, how to install, how to run, folder structure.
- Update when something relevant changes.

## Code style

### Linter and formatter
- ruff (lint + format, configured in `pyproject.toml`)
- Run: `ruff check .` and `ruff format .`

### Naming
- Variables and functions: snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Files: no prefix for orchestration, `adapter_` for external service wrappers

### Imports
- Order: stdlib → third-party → local
- ruff handles this automatically

## Security

- Never commit the LLM API key. It lives in `.env` only.
- Do not log invoice content — invoices may contain sensitive financial data.
- Validate PDF file paths before opening (must exist, must be .pdf extension).
- Dependencies: pdfplumber, pydantic-ai — both well-maintained, reviewed before adoption.

## Performance

- Log processing time per invoice at DEBUG level.
- If a single invoice takes > 15 s, log a WARNING.
- Do not load all PDFs into memory simultaneously — process one at a time.
- LLM call is the bottleneck: do not add redundant calls. One call per invoice.

## Error handling

### Exceptions
- `PDFExtractionError`: raised by pdf_extractor when pdfplumber fails or returns empty text.
- `LLMParsingError`: raised by llm_parser when the LLM response fails Pydantic validation after retries.
- Both are caught in main.py, logged, and the file is added to the error report.

### Logging
- Use `utilities/logger.py` in all components.
- INFO: file processed successfully, batch summary.
- WARNING: invoice took > 15 s, field missing but recoverable.
- ERROR: extraction failed, LLM error after retries.
- Never log invoice content or API keys.

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

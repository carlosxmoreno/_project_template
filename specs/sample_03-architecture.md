# 03 - Architecture — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 03-architecture.md as your starting point. -->

## Component diagram

```
CLI (main.py)
    │
    ├── pdf_extractor.py   → extracts raw text from PDF
    │       │
    │       └── pdfplumber (third-party)
    │
    ├── llm_parser.py      → sends text to LLM, returns Invoice object
    │       │
    │       ├── llm_client.py (shared utility)
    │       └── LLM Provider API (Gemini / OpenAI)
    │
    └── csv_exporter.py    → writes Invoice list to CSV
            │
            └── data/output/ (filesystem)
```

## Components

### 1. pdf_extractor
- **Responsibility**: read a PDF file and return its text content as a string.
- **Input**: Path to a PDF file.
- **Output**: Raw text string.
- **Key decision**: uses pdfplumber (not pypdf2) for better layout handling on invoice formats.
- **Limitation**: does not support scanned/image PDFs (out of scope v1).

### 2. llm_parser
- **Responsibility**: send extracted text to the LLM and return a validated Invoice object.
- **Input**: Raw text string from pdf_extractor.
- **Output**: Invoice Pydantic model (see 05-data-model.md).
- **Key decision**: uses pydantic-ai for structured output — LLM response is validated against the Invoice schema before returning.
- **Error handling**: retries on 429/503. Raises on 401/400. See utilities/api_errors.py.

### 3. csv_exporter
- **Responsibility**: write a list of Invoice objects to a CSV file.
- **Input**: list[Invoice], output Path.
- **Output**: CSV file with header row.
- **Key decision**: uses Python stdlib csv module — no pandas dependency.

### 4. main.py (CLI)
- **Responsibility**: parse CLI arguments, orchestrate the pipeline, report results.
- **Input**: --input (file or directory), --output (CSV path).
- **Output**: CSV file + console summary (N processed, N errors).

## Technical constraints

- Language: Python 3.11+
- No database — all I/O via filesystem.
- No GUI — CLI only in v1.
- Free/open-source dependencies only (except LLM API, which is pay-per-use).

## Design decisions

- **pdfplumber over pypdf2**: better handling of invoice table layouts and whitespace. Evaluated both on 10 sample invoices — pdfplumber produced cleaner text in 8/10 cases.
- **pydantic-ai for LLM calls**: structured output validation without manual JSON parsing. Consistent with other projects in this workspace.
- **No pandas for CSV**: stdlib csv is sufficient for flat tabular output. Avoids a heavy dependency for a simple use case.
- **One CSV per run**: simpler than appending to an existing file. User can merge CSVs manually if needed.

## File naming conventions

- `core_`    → interfaces / ABCs (if needed in future)
- `adapter_` → concrete implementations of external services
- No prefix  → orchestration and CLI scripts

## Project structure

```
InvoiceParser/
├── specs/
├── config/
│   ├── settings.yaml
│   └── llm.yaml
├── data/
│   ├── input/             → PDF invoices to process
│   └── output/            → generated CSV files
├── logs/
├── references/            → sample invoices for testing
├── src/
│   ├── pdf_extractor.py
│   ├── llm_parser.py
│   ├── csv_exporter.py
│   └── config.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── sandbox/
├── utilities/
│   ├── logger.py
│   ├── timestamp.py
│   └── api_errors.py
├── main.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── requirements.txt
```

## Utilities

Three shared modules provided by the project template:

- `utilities/logger.py` — logging with timestamp, level and caller name.
- `utilities/timestamp.py` — timestamp string for output file naming.
- `utilities/api_errors.py` — LLM API error classification and retry logic.

## Main dependencies

```
pdfplumber    → PDF text extraction
pydantic-ai   → structured LLM calls with output validation
pydantic      → Invoice data model
pyyaml        → YAML configuration
python-dotenv → .env loading
```

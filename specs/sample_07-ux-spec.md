# 07 - UX Spec — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 07-ux-spec.md as your starting point. -->

## Interface type

CLI (command-line interface). Single entry point: `main.py`.

## User flows

### Flow 1: Process a single invoice

```
User runs: python main.py --input data/input/invoice_001.pdf --output data/output/result.csv
    │
    ├── System validates input path (exists, is .pdf)
    ├── System extracts text from PDF
    ├── System calls LLM to parse fields
    ├── System writes CSV
    └── System prints summary:
        "1 file processed. 1 successful. 0 errors. Output: data/output/result.csv"
```

### Flow 2: Process a directory of invoices

```
User runs: python main.py --input data/input/ --output data/output/batch.csv
    │
    ├── System lists all .pdf files in directory (e.g. 12 files found)
    ├── System prints: "Processing 12 invoices..."
    ├── For each file: extract → parse → collect result
    │       └── Progress: "  [1/12] invoice_001.pdf ... OK"
    │                     "  [2/12] invoice_002.pdf ... ERROR: empty text layer"
    ├── System writes CSV with all results (successes + errors)
    └── System prints summary:
        "12 files processed. 11 successful. 1 error. Output: data/output/batch.csv"
```

### Flow 3: Missing or invalid input

```
User runs: python main.py --input data/input/missing.pdf
    │
    └── System prints: "ERROR: File not found: data/input/missing.pdf"
        Exits with code 1. No CSV written.
```

## Commands / Screens

### main.py

```
Usage: python main.py --input <path> [--output <path>]

Arguments:
  --input   Path to a PDF file or a directory containing PDF files. Required.
  --output  Path for the output CSV file.
            Default: data/output/invoices_<timestamp>.csv

Examples:
  python main.py --input data/input/invoice_001.pdf
  python main.py --input data/input/ --output data/output/march_2025.csv
```

### Console output format

Per-file progress (batch mode):
```
Processing 12 invoices...
  [1/12] invoice_001.pdf ... OK
  [2/12] invoice_002.pdf ... ERROR: empty text layer (scanned PDF not supported)
  [3/12] invoice_003.pdf ... OK
  ...
```

Final summary:
```
--------------------------------------------------
12 files processed. 11 successful. 1 error.
Output: data/output/invoices_150126_1430.csv
--------------------------------------------------
```

## Error messages

| Situation                        | Message shown to user                                              |
|----------------------------------|--------------------------------------------------------------------|
| Input path not found             | ERROR: File not found: <path>                                      |
| Input directory empty            | ERROR: No PDF files found in: <path>                               |
| Scanned PDF (no text layer)      | ERROR: <filename>: empty text layer (scanned PDFs not supported)   |
| LLM API key missing              | ERROR: LLM API key not set. Check your .env file.                  |
| LLM API auth failure             | ERROR: LLM authentication failed (401). Check your API key.        |
| LLM parsing failed after retries | ERROR: <filename>: LLM could not extract fields after 3 attempts.  |
| Output directory not found       | ERROR: Output directory does not exist: <path>                     |

All errors are also written to logs/invoiceparser.log.

## Design constraints

- Text output only. No colours, no progress bars, no interactive prompts.
- Single command, no subcommands.
- Non-zero exit code on any error (including partial batch failures).
- Output CSV path printed at the end so the user can find it easily.

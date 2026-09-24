# 06 - Pipelines — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 06-pipelines.md as your starting point. -->

## Pipeline: Invoice extraction pipeline

The main pipeline processes one or more PDF invoices and produces a CSV file.
It is orchestrated by main.py and executed sequentially (one invoice at a time).

### Steps

```
Input (PDF file or directory)
    │
    ▼
Step 1: Resolve input files
    │   List all .pdf files from the input path (file or directory).
    │
    ▼
Step 2: Extract text (pdf_extractor.py)
    │   Read PDF with pdfplumber, return raw text string.
    │   → On failure: log PDFExtractionError, add to error list, skip to next file.
    │
    ▼
Step 3: Parse with LLM (llm_parser.py)
    │   Send raw text to LLM with structured output schema (Invoice).
    │   Retry on 429/503 (max 3 attempts). Raise on 401/400.
    │   → On failure: log LLMParsingError, add to error list, skip to next file.
    │
    ▼
Step 4: Collect results
    │   Append Invoice object (or error record) to results list.
    │
    ▼
Step 5: Export to CSV (csv_exporter.py)
    │   Write all results (successful and failed) to CSV.
    │   Filename: invoices_<timestamp>.csv in data/output/.
    │
    ▼
Step 6: Print summary
        N files processed. N successful. N errors. Output: <csv_path>.
```

### Step details

#### Step 1: Resolve input files
- **Input**: CLI argument `--input` (file path or directory path).
- **Output**: list[Path] of .pdf files to process.
- **Component**: main.py
- **Notes**: raises ValueError if path does not exist or no .pdf files found.

#### Step 2: Extract text
- **Input**: Path to a single PDF file.
- **Output**: raw text string.
- **Component**: src/pdf_extractor.py
- **Notes**: pdfplumber opens the file, concatenates text from all pages. Returns empty string if no text layer found (scanned PDF) — this triggers a PDFExtractionError.

#### Step 3: Parse with LLM
- **Input**: raw text string.
- **Output**: Invoice Pydantic object.
- **Component**: src/llm_parser.py → utilities/llm_client.py
- **Notes**: prompt instructs the LLM to extract exactly the fields defined in the Invoice schema. pydantic-ai validates the response. Max 3 retries on transient errors.

#### Step 4: Collect results
- **Input**: Invoice object or exception.
- **Output**: list[ExtractionResult].
- **Component**: main.py
- **Notes**: both successes and failures are collected. The pipeline never aborts mid-batch.

#### Step 5: Export to CSV
- **Input**: list[ExtractionResult].
- **Output**: CSV file at data/output/invoices_<timestamp>.csv.
- **Component**: src/csv_exporter.py
- **Notes**: writes header row first. Errors appear as rows with extraction_error populated and other fields empty.

#### Step 6: Print summary
- **Input**: list[ExtractionResult].
- **Output**: console output.
- **Component**: main.py
- **Notes**: always printed, even if all files failed.

## Error handling per step

| Step | Error type          | Behaviour                                              |
|------|---------------------|--------------------------------------------------------|
| 1    | Path not found      | Abort with clear error message before processing starts|
| 2    | PDFExtractionError  | Log error, skip file, continue batch                   |
| 3    | LLMParsingError     | Log error after retries, skip file, continue batch     |
| 3    | API 401/400         | Abort entire batch — credentials or config issue       |
| 5    | CSV write error     | Abort with error — output directory may not exist      |

## Configuration

Configurable parameters via config/settings.yaml and config/llm.yaml:

- `llm.max_retries`: number of retry attempts on transient LLM errors (default: 3).
- `llm.model`: LLM model name.
- `llm.provider`: active provider (gemini, openai).
- `paths.output_dir`: directory for CSV output (default: data/output/).

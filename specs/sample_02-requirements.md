# 02 - Requirements — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 02-requirements.md as your starting point. -->

---

## Functional requirements

<!-- Traceability: each FR maps to a capability in 01-vision.md § Capabilities. -->

| ID    | Description                                                                                      | Source                        | Verification                                                                 |
|-------|--------------------------------------------------------------------------------------------------|-------------------------------|------------------------------------------------------------------------------|
| FR-01 | The system shall extract issuer name, invoice number, date, total amount and currency from a PDF. | Extract core fields           | Integration test: 50 real invoices, 95% field accuracy.                      |
| FR-02 | The system shall process a single PDF file passed as a CLI argument.                             | Process single or batch       | Unit test: valid PDF path → Invoice object with all fields populated.        |
| FR-03 | The system shall process all PDF files in a directory passed as a CLI argument.                  | Process single or batch       | Integration test: directory of 10 PDFs → CSV with 10 rows.                  |
| FR-04 | The system shall export extracted data to a CSV file with a header row.                          | Export to CSV                 | Integration test: output CSV is readable by Excel, contains correct headers. |
| FR-05 | The system shall log and report extraction errors per file without stopping the batch.           | Report errors without stopping| Integration test: batch with 1 corrupt PDF → remaining files processed, error logged. |

---

## Non-functional requirements

| ID     | Description                                                                                  | Verification                                                    |
|--------|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| NFR-01 | The system shall run on Windows 11 and Ubuntu 22.04 without code changes.                   | Manual test on both OS after each release.                      |
| NFR-02 | The system shall require only packages listed in requirements.txt (no system dependencies).  | Fresh venv install + run on CI.                                 |
| NFR-03 | The LLM provider, model and prompt shall be configurable via config/llm.yaml without code changes. | Change provider in YAML, re-run, verify output unchanged. |

---

## Quality attributes (ISO/IEC 25010)

<!-- For each characteristic: fill in Target and remove the Not applicable line.
     If not applicable: remove Target and replace Not applicable with the reason. -->

### Functional suitability
<!-- Does the system do what it is supposed to do, correctly and completely? -->
- Target: FR-01 to FR-05 all pass their defined verification tests.

### Performance efficiency
<!-- Response time, throughput, resource usage under expected load. -->
- Target: Single invoice processed in < 10 s on standard laptop. Batch of 50 invoices in < 10 min.

### Compatibility
<!-- Can the system coexist and interoperate with other systems? -->
- Target: CSV output importable by Excel and Google Sheets without formatting issues.

### Usability
<!-- How easy is it to learn, operate and recover from errors? -->
- Target: Finance analyst can run a batch following README in < 10 min (OKR KR2).

### Reliability
<!-- Availability, fault tolerance, recoverability. -->
- Target: One failed invoice does not abort the batch. All errors logged with filename and reason.

### Security
<!-- Confidentiality, integrity, authentication, non-repudiation. -->
- Target: API key never written to logs or CSV output. Loaded exclusively from .env.
- See also: 04-dev-practices.md § Security

### Maintainability
<!-- How easy is it to analyse, modify, test and reuse the code? -->
- Target: Each component (pdf_extractor, llm_parser, csv_exporter) has independent unit tests. No function exceeds 40 lines.
- See also: dev-rules.md, 04-dev-practices.md

### Portability
<!-- How easily can the system be moved to a different environment? -->
- Target: Runs on Windows and Linux without code changes (NFR-01).
- See also: dev-rules.md (pathlib, UTF-8)

# 09 - Test Log — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 09-test-log.md as your starting point. -->

## Format

Each entry: test ID, date, component, what was tested, result, conclusion.

---

## Test 001

- **Date**: 2025-01-16
- **Component**: pdf_extractor
- **What was tested**: Unit test — extract text from a valid single-page PDF invoice.
- **Result**: PASS. Raw text returned, contains issuer name and invoice number.
- **Conclusion**: pdfplumber handles standard PDF invoices correctly.

---

## Test 002

- **Date**: 2025-01-16
- **Component**: pdf_extractor
- **What was tested**: Unit test — attempt to extract text from a scanned (image-only) PDF.
- **Result**: PASS. PDFExtractionError raised with message "empty text layer".
- **Conclusion**: error handling for scanned PDFs works as specified in FR-05.

---

## Test 003

- **Date**: 2025-01-17
- **Component**: llm_parser
- **What was tested**: Unit test — parse a known text fixture, verify Invoice fields match expected values.
- **Result**: PASS. All 5 fields extracted correctly. invoice_date in ISO 8601 format.
- **Conclusion**: LLM prompt produces consistent structured output for standard invoice text.

---

## Test 004

- **Date**: 2025-01-17
- **Component**: llm_parser
- **What was tested**: Unit test — LLM returns malformed JSON (simulated with mock). Verify LLMParsingError raised.
- **Result**: PASS. LLMParsingError raised after 3 retries.
- **Conclusion**: retry and error propagation logic works correctly.

---

## Test 005

- **Date**: 2025-01-17
- **Component**: csv_exporter
- **What was tested**: Unit test — export list of 3 Invoice objects to CSV. Verify header and row count.
- **Result**: PASS. CSV contains header + 3 rows. All fields present.
- **Conclusion**: csv_exporter produces correct output for standard cases.

---

## Test 006

- **Date**: 2025-01-18
- **Component**: Full pipeline (integration)
- **What was tested**: Integration test — process directory of 10 real PDF invoices. Verify CSV output.
- **Result**: PASS. 9 successful, 1 error (scanned PDF). CSV contains 10 rows. Error row has extraction_error populated.
- **Conclusion**: pipeline handles mixed batch correctly. FR-03, FR-04, FR-05 verified.

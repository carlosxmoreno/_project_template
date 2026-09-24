# 01 - Vision — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 01-vision.md as your starting point. -->

## Problem

Small finance teams spend significant time manually extracting data from supplier
invoices (PDF format) to enter into spreadsheets or accounting systems. The process
is error-prone, repetitive and does not scale with invoice volume.

## Solution

A CLI tool that reads one or more PDF invoices, uses an LLM to extract structured
fields (issuer, amount, date, invoice number, line items), and exports the results
to a CSV file ready for import into accounting tools.

## Users and stakeholders

<!-- Inspired by ISO/IEC/IEEE 29148 stakeholder identification. -->

- **Finance analyst**: processes 20-100 invoices per week. Needs reliable extraction
  with minimal manual correction. Not technical — runs the tool via a simple command.
- **Finance manager**: needs the CSV output to be compatible with the accounting system.
  Cares about accuracy and auditability, not the tool itself.
- **Developer / maintainer**: sets up the tool, manages API keys, updates the LLM
  prompt when extraction quality degrades.

## Scope v1

### Capabilities
- Extract issuer name, invoice number, invoice date, total amount and currency from PDF invoices.
- Process a single PDF or a directory of PDFs in one command.
- Export extracted data to a single CSV file with a header row.
- Report extraction errors per file without stopping the batch.

### Out of scope v1
- Line item extraction (individual products/services on the invoice).
- Support for scanned PDFs (image-based, requires OCR).
- Direct integration with accounting systems (QuickBooks, Xero, etc.).
- Web interface or GUI.
- Multi-language invoices (English only in v1).

## OKRs — How we know the product works

**Objective 1**: The system reliably extracts the core fields from standard invoices.
- KR1: 95% of fields correctly extracted across a test set of 50 real invoices.
- KR2: Zero silent failures — every extraction error is logged and reported.

**Objective 2**: A non-technical user can run the tool without developer assistance.
- KR1: A finance analyst can process a batch following the README in under 10 minutes.
- KR2: Error messages are human-readable and suggest a corrective action.

## Future scope

- Line item extraction (v2).
- OCR support for scanned invoices via Tesseract (v2).
- JSON export format (v2).
- Confidence score per extracted field (v2).

## Design principles

- Configurable: LLM provider, model and prompt configurable via YAML, no code changes needed.
- Fault tolerant: one failed invoice does not stop the batch.
- Auditable: every extraction logged with input file, output fields and timestamp.
- Lightweight: no database, no server, runs locally.

## Requirements and quality

See [02-requirements.md](02-requirements.md) for functional requirements,
non-functional requirements and quality attribute targets (ISO/IEC 25010).

## Technical constraints

See [03-architecture.md](03-architecture.md) for technical decisions and stack.

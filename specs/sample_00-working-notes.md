# 00 - Working Notes — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 00-working-notes.md as your starting point. -->

## Project context

**Name**: InvoiceParser
**Domain**: Finance / Document processing
**Goal**: Extract structured data from PDF invoices using an LLM and export to CSV.

---

## Agent Memory (Current State)

<!-- Agents: Read this section first when starting a new session. This is your "memory.md". -->
**Last Updated**: 2025-01-16 18:00
**Development Time Tracked**: 4 hours
**Current Phase**: Implementing Core Components

**Where we left off**: 
- We finished defining the architecture and selected pdfplumber.
- FR-01 to FR-05 are approved.

**Next Immediate Steps**:
- Begin implementation of `pdf_extractor` component.
- Write unit tests for `pdf_extractor`.
---

## Pending decisions

- Evaluate pdfplumber vs pypdf2 for PDF text extraction (see 03-architecture.md).
- Decide whether to support multi-page invoices in v1 or defer to v2.

---

## Confirmed decisions

- 2025-01-15: Use Gemini 2.0 Flash as LLM provider. Rationale: low cost per token, good structured output support via pydantic-ai.
- 2025-01-15: Output format is CSV only in v1. JSON export deferred to v2.
- 2025-01-16: Use pdfplumber for PDF extraction. Rationale: better table and layout handling than pypdf2 for invoice formats.

---

## Session history

### Session 1 — 2025-01-15
- Project created from template.
- Vision and requirements drafted.
- LLM provider decided: Gemini 2.0 Flash.

### Session 2 — 2025-01-16
- Architecture defined: pdf_extractor, llm_parser, csv_exporter components.
- PDF library decided: pdfplumber.
- FR-01 to FR-05 reviewed and approved.

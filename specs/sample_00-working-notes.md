# 00 - Working Notes — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 00-working-notes.md as your starting point. -->

## Project context

**Name**: InvoiceParser
**Domain**: Finance / Document processing
**Goal**: Extract structured data from PDF invoices using an LLM and export to CSV.

---

## How to use this framework

This project uses a spec-driven, incremental development framework.
Specs are written before code. Code is written to satisfy specs. Tests verify compliance.

### Spec profiles

**Minimum** — included in every project. Sufficient for most projects.

```
specs/
├── 00-working-notes.md   ← THIS DOCUMENT (work diary, decisions, session history)
├── 01-vision.md          → Problem, solution, users, scope, OKRs, design principles
├── 02-requirements.md    → Functional requirements (FR), non-functional requirements (NFR),
│                            quality attribute targets (ISO/IEC 25010)
├── 03-architecture.md    → Components, structure, dependencies, design decisions
└── 04-dev-practices.md   → Testing strategy, code style, commits, branching, security
```

**Extended** — add individual files as the project needs them.

```
specs/
├── 05-data-model.md      → Entities, schemas, storage design
├── 06-pipelines.md       → Data flows and processing pipelines
├── 07-ux-spec.md         → User interaction (CLI, web, API)
├── 08-api-spec.md        → LLM and external API contracts
├── 09-test-log.md        → Formal test log (when volume justifies it)
└── 10-environment.md     → Environment setup, deployment, compatibility
```

### Traceability chain

```
01-vision § Capabilities
    └── 02-requirements § FR / NFR / Quality attributes
            └── 03-architecture § Components
                    └── src/ (implementation)
                            └── tests/ (verification)
```

### Development process

**Phases per increment:**
1. **SPEC** — Write or update the relevant spec
2. **REVIEW** — Validate together, resolve ambiguities
3. **IMPL** — Code according to the approved spec
4. **VERIFY** — Run tests, confirm compliance with spec

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

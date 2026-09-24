# 08 - API / LLM Spec — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 08-api-spec.md as your starting point. -->

## Overview

InvoiceParser uses one external API: a generative LLM for structured field extraction.
No other external APIs are used in v1.

## LLM configuration

**Config file**: `config/llm.yaml`

```yaml
active_provider: gemini
model: gemini-2.0-flash
temperature: 0.0        # deterministic output preferred for data extraction
max_output_tokens: 512  # invoice fields are short, no need for long responses
max_retries: 3
providers:
  gemini:
    api_key_env: GEMINI_API_KEY
    provider_class: pydantic_ai.providers.google_gla.GoogleGLAProvider
    model_class: pydantic_ai.models.gemini.GeminiModel
```

## Contracts

### Request: Invoice field extraction

- **Component**: src/llm_parser.py via utilities/llm_client.py
- **Trigger**: once per PDF invoice, after text extraction.
- **Input fields**:
  - `raw_text` (str): full text extracted from the PDF by pdfplumber.
- **Output schema** (Pydantic model `Invoice`):
  - `issuer` (str): company name of the invoice issuer.
  - `invoice_number` (str): invoice identifier as printed.
  - `invoice_date` (str): date in ISO 8601 format (YYYY-MM-DD).
  - `total_amount` (float): total amount due, numeric only.
  - `currency` (str): ISO 4217 currency code.
- **Validation**: pydantic-ai validates the LLM response against the Invoice schema before returning. If validation fails, LLMParsingError is raised.

### System prompt

```
You are a data extraction assistant. Extract the following fields from the invoice text
provided. Return only the structured data — no explanation, no commentary.

Fields to extract:
- issuer: the name of the company that issued the invoice.
- invoice_number: the invoice identifier (e.g. INV-2025-001).
- invoice_date: the invoice date in ISO 8601 format (YYYY-MM-DD).
- total_amount: the total amount due as a number (no currency symbol).
- currency: the currency as an ISO 4217 code (e.g. EUR, USD, GBP).

If a field cannot be found, return an empty string for text fields and 0.0 for numeric fields.
```

## Error handling

| Error code | Type        | Behaviour                                              |
|------------|-------------|--------------------------------------------------------|
| 429        | Retryable   | Wait 10 s, retry up to max_retries times.              |
| 503        | Retryable   | Wait 10 s, retry up to max_retries times.              |
| 401        | Fatal       | Abort batch. Log: "LLM authentication failed (401)."   |
| 400        | Fatal       | Abort file. Log: "Invalid LLM request (400)."          |
| Validation | Fatal       | Raise LLMParsingError after max_retries exhausted.     |

See `utilities/api_errors.py` for `is_retryable()` and `error_message()` helpers.

## Providers implemented

| Provider | Status      | Notes                              |
|----------|-------------|------------------------------------|
| Gemini   | Implemented | Default. gemini-2.0-flash.         |
| OpenAI   | Pending     | Config structure ready, not tested.|

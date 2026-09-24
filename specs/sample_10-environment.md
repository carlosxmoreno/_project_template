# 10 - Environment — InvoiceParser

<!-- This is a sample spec file for the InvoiceParser example project.
     It illustrates how to fill in this template for a real project.
     Do not copy this file — use 10-environment.md as your starting point. -->

## Development environment

- **OS**: Windows 11 (primary), Ubuntu 22.04 (tested)
- **Python version**: 3.11
- **Virtual environment**: venv (.venv)
- **Key dependencies**: see requirements.txt

## Setup instructions

```bash
# Clone the repo
git clone <repo_url>
cd InvoiceParser

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Copy and fill in environment variables
copy .env.example .env        # Windows
cp .env.example .env          # Linux/macOS
# Edit .env and set GEMINI_API_KEY=<your_key>
```

## Environment variables

Copy `.env.example` to `.env` and fill in the values.

| Variable        | Required | Description                        |
|-----------------|----------|------------------------------------|
| GEMINI_API_KEY  | Yes      | API key for Gemini LLM provider.   |
| OPENAI_API_KEY  | No       | Only needed if switching provider. |

## Deployment

InvoiceParser is a local CLI tool — no server deployment in v1.

Distribution options for sharing with the finance team:
- Share the repository and have each user run setup instructions above.
- Package as a standalone executable with PyInstaller (future consideration).

## Compatibility notes

- **Windows**: use `.venv\Scripts\activate`. Path separators handled via pathlib throughout.
- **Linux/macOS**: use `source .venv/bin/activate`. No known issues.
- **Scanned PDFs**: not supported in v1. pdfplumber requires a text layer. OCR support planned for v2.
- **Python 3.10 or earlier**: not tested. pydantic-ai requires Python 3.11+.

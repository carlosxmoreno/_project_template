# {{PROJECT_NAME}}

<!-- One sentence describing what this project does -->

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
copy .env.example .env        # Windows
cp .env.example .env          # Linux/macOS
# Edit .env and fill in real values
```

## Usage

```bash
# Add usage instructions here
python main.py
```

## Project structure

```
{{PROJECT_NAME}}/
├── specs/          → Specification documents
├── config/         → YAML configuration
├── src/            → Source code
├── tests/          → Tests (unit, integration, sandbox)
├── utilities/      → Shared utilities (logger, timestamp, api_errors)
├── data/           → Input/output data
├── logs/           → Runtime logs
└── references/     → External reference documents
```

## Specs

See [specs/01-vision.md](specs/01-vision.md) for goals, scope and OKRs.
See [specs/02-requirements.md](specs/02-requirements.md) for functional and non-functional requirements.
See [specs/03-architecture.md](specs/03-architecture.md) for technical decisions.
See [specs/00-working-notes.md](specs/00-working-notes.md) for the full spec index and how to use this framework.

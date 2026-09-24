# _project_template

A Python project template for spec-driven, incremental development.
Includes a setup script, a structured spec framework, shared utilities and example specs.

## What this is

A reusable starting point for Python projects that follow a spec-first approach:
specs are written before code, code is written to satisfy specs, tests verify compliance.

The framework is aligned with:
- **ISO/IEC/IEEE 29148** — requirements engineering (functional and non-functional requirements).
- **ISO/IEC 25010** — software product quality (quality attribute targets).

## How to use

**1. Clone this repository**

```bash
git clone https://github.com/carlosxmoreno/_project_template.git
cd _project_template
```

**2. Edit `setup_config.yaml`**

```yaml
destination_parent: "D:/Dev"   # where your new project will be created
specs_profile: "minimum"       # minimum | extended
linter: true                   # include ruff configuration
python_env: "venv"             # venv | conda | none
python_version: "3.11"
venv_system_packages: false    # true saves disk space, less isolation
git_init: true
```

**3. Run the setup script**

```bash
python setup_project.py MyProjectName
```

The script will:
- Copy the template to `destination_parent/MyProjectName`.
- Replace `{{PROJECT_NAME}}` in all spec and config files.
- Apply the selected specs profile and linter settings.
- Create a Python virtual environment.
- Optionally initialize a git repository.

**4. Start with the specs**

Open `specs/01-vision.md` and fill in the problem, solution and scope.
Then `specs/02-requirements.md` for functional and non-functional requirements.
See `specs/00-working-notes.md` for the full framework guide.

## Spec framework

### Minimum set — included in every project

| File | Purpose |
|------|---------|
| `specs/00-working-notes.md` | Work diary, decisions, session history, framework guide |
| `specs/01-vision.md` | Problem, solution, users, scope, OKRs |
| `specs/02-requirements.md` | Functional requirements, NFR, quality attributes (ISO 25010) |
| `specs/03-architecture.md` | Components, structure, design decisions |
| `specs/04-dev-practices.md` | Testing, code style, security, commits |

### Extended set — activate as needed

| File | When to use |
|------|-------------|
| `specs/05-data-model.md` | Non-trivial entities or storage |
| `specs/06-pipelines.md` | Multi-step data flows |
| `specs/07-ux-spec.md` | User interface beyond a simple CLI |
| `specs/08-api-spec.md` | LLM or external API usage |
| `specs/09-test-log.md` | Formal test log when volume justifies it |
| `specs/10-environment.md` | Specific deployment or environment requirements |

Set `specs_profile: extended` in `setup_config.yaml` to include all files.

## Example specs

The `specs/` directory contains a complete set of filled-in example specs for a
fictional project called **InvoiceParser** (a CLI tool that extracts structured data
from PDF invoices using an LLM and exports to CSV).

| File | Description |
|------|-------------|
| `specs/sample_00-working-notes.md` | Example work diary with real decisions and session history |
| `specs/sample_01-vision.md` | Example vision with stakeholders, OKRs and design principles |
| `specs/sample_02-requirements.md` | Example FR/NFR table and quality attribute targets |
| `specs/sample_03-architecture.md` | Example component diagram and design decisions |
| `specs/sample_04-dev-practices.md` | Example testing strategy and security rules |
| `specs/sample_05-data-model.md` | Example Invoice entity and CSV schema |
| `specs/sample_06-pipelines.md` | Example extraction pipeline with error handling |
| `specs/sample_07-ux-spec.md` | Example CLI flows and error messages |
| `specs/sample_08-api-spec.md` | Example LLM config, prompt and error handling |
| `specs/sample_09-test-log.md` | Example test log entries |
| `specs/sample_10-environment.md` | Example environment setup and compatibility notes |

Sample files are never copied to destination projects.

## Project structure (destination project)

```
MyProjectName/
├── specs/                  → Specification documents
├── config/                 → YAML configuration
├── src/                    → Source code
├── tests/
│   ├── unit/
│   ├── integration/
│   └── sandbox/            → Throwaway scripts
├── utilities/
│   ├── logger.py           → Logging with timestamp and caller name
│   ├── timestamp.py        → Timestamp string for file naming
│   └── api_errors.py       → LLM API error classification
├── data/                   → Input/output data
├── logs/                   → Runtime logs
├── references/             → External reference documents
├── .amazonq/rules/         → Amazon Q dev rules (auto-loaded in IDE)
├── .env.example
├── .gitignore
├── pyproject.toml
└── requirements.txt
```

## Shared utilities

Three utilities are included in every project, with no external dependencies:

- `utilities/logger.py` — logging with timestamp, level and caller name. Writes to stdout/stderr and `logs/<project>.log`.
- `utilities/timestamp.py` — `now_stamp()` returns a `ddmmyy_HHMM` string for output file naming.
- `utilities/api_errors.py` — `is_retryable(error)` and `error_message(error)` for LLM API HTTP errors.

## Re-running setup on an existing project

If you change `setup_config.yaml` and want to apply the new settings to an existing project:

```bash
python setup_project.py MyProjectName
```

The script detects the existing project and offers to overwrite only the setup files
(specs, config, pyproject.toml, README, utilities). Source code, data, logs and `.venv`
are never touched.

> No automatic backup is created. Make a manual copy if needed before re-running.

# 09 - Environment — {{PROJECT_NAME}}

## Development environment

- **OS**: <!-- e.g. Windows 11 + Ubuntu -->
- **Python version**:
- **Virtual environment**: <!-- venv | conda -->
- **Key dependencies**: see requirements.txt

## Setup instructions

```bash
# Clone the repo
git clone <repo_url>
cd {{PROJECT_NAME}}

# Create virtual environment (venv)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

## Environment variables

Copy `.env.example` to `.env` and fill in the values.

## Deployment

<!-- How is this project run in production or shared with others? -->

## Compatibility notes

<!-- Known issues or requirements per OS or environment -->

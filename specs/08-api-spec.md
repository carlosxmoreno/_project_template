# 07 - API / LLM Spec — {{PROJECT_NAME}}

## Overview

<!-- What external APIs or LLMs does this project use? -->

## LLM configuration

<!-- If using an LLM, describe: provider, model, parameters, config file location -->

**Config file**: `config/llm.yaml`

```yaml
# Example structure
active_provider: <!-- gemini | openai | ollama -->
model: <!-- model name -->
temperature: 0.1
max_output_tokens: 8192
```

## Contracts

### Request: <!-- Name -->
- **Input fields**:
- **Output fields**:
- **Validation**:

## Error handling

<!-- Retryable errors, fatal errors, timeouts. Reference utilities/api_errors.py -->

## Providers implemented

<!-- List providers and their status: implemented / pending -->

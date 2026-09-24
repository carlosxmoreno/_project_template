# Development Rules — {{PROJECT_NAME}}

## Code

- All configuration in YAML files. No hardcoded values.
- Do not duplicate methods or services. Verify it does not exist before creating.
- No emojis in code or files.
- Use the logger (utilities/logger.py) in all components.
- Use pathlib for paths (Windows/Linux compatibility).
- Explicit UTF-8 encoding when reading/writing files.
- Mandatory header in every script: project name, version, component.
- Google style docstrings in modules, classes and public methods.

## Tests

- Tests always produce verifiable output on disk (files a human can inspect).
- Unit tests: may use simplified data.
- Integration tests: always with real data.
- Regression tests: re-run previous tests when adding a new component.
- Run integration tests when: a new component is added, an adapter changes, or configuration parameters change.
- Run all tests before merging to main.
- Do not create a test script without checking if an existing one can serve the same purpose.

## Process

- Propose changes before executing them. Wait for approval.
- Ask when in doubt.
- Incremental development: small functional additions decided together.
- Do not write code without an approved spec.
- Throwaway/sandbox scripts go in tests/sandbox/.
- Always from analysis to design: define functional requirements first, then technical design.
- Always test new or modified code before marking a step as complete.
- Keep the workspace clean. No loose files outside the project structure.

## Specs

- Re-read the full file before adding content. Do not create sections that overlap or duplicate existing content.
- Each piece of data has one single place. If it already exists in another spec file, reference it, do not repeat it.
- Each spec covers only its own scope.
- Decisions are recorded in 08-test-log.md (tests) or 00-working-notes.md (history).

# 00 - Working Notes — {{PROJECT_NAME}}

## Project context

**Name**: {{PROJECT_NAME}}
**Domain**: <!-- e.g. Education, Finance, DevTools -->
**Goal**: <!-- One sentence describing what this project achieves -->

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

When to activate an extended spec:
- `05-data-model` : when the project has non-trivial entities or storage.
- `06-pipelines`  : when there are defined multi-step data flows.
- `07-ux-spec`    : when there is a user interface beyond a simple CLI.
- `08-api-spec`   : when the project uses an LLM or external APIs.
- `09-test-log`   : when the number of tests justifies a formal log.
- `10-environment`: when there are specific deployment or environment requirements.

### Traceability chain

```
01-vision § Capabilities
    └── 02-requirements § FR / NFR / Quality attributes
            └── 03-architecture § Components
                    └── src/ (implementation)
                            └── tests/ (verification)
```

Each FR in `02-requirements.md` must have a verification criterion.
Each test must trace back to at least one FR or quality attribute target.

### Development process

**Phases per increment:**
1. **SPEC** — Write or update the relevant spec
2. **REVIEW** — Validate together, resolve ambiguities
3. **IMPL** — Code according to the approved spec
4. **VERIFY** — Run tests, confirm compliance with spec

**Rules:**
- No code without an approved spec.
- The spec is the contract; changes require updating the spec first.
- One increment at a time.
- This document does not repeat information from other specs — reference, do not duplicate.

---

## Pending decisions

<!-- List open questions and decisions not yet made -->
-

---

## Confirmed decisions

<!-- Record decisions here as they are made, with date and rationale -->
-

---

## Session history

### Session 1
- Project created from template

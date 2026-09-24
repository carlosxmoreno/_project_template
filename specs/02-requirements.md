# 02 - Requirements — {{PROJECT_NAME}}

<!-- This document defines WHAT the system must do (functional requirements) and
     HOW WELL it must do it (non-functional requirements and quality attributes).
     It bridges the strategic vision (01-vision.md) and the technical design
     (03-architecture.md and domain specs).

     Inspired by ISO/IEC/IEEE 29148 (requirements engineering).
     Quality attributes follow ISO/IEC 25010.

     Traceability:
     - Each capability in 01-vision.md § Capabilities maps to one or more FR here.
     - Each FR maps to one or more components in 03-architecture.md.
     - Each FR has a verification criterion that feeds into tests (unit or integration).

     A good requirement is: necessary, unambiguous, complete, singular, verifiable,
     feasible and consistent with other requirements (ISO/IEC/IEEE 29148 § 5.2.5). -->

---

## Functional requirements

<!-- One row per requirement. ID format: FR-NN.
     - Description: "The system shall..." (active voice, single behaviour).
     - Source: capability in 01-vision.md it traces to.
     - Verification: how to confirm it is met (test type and pass condition). -->

| ID    | Description                        | Source      | Verification                        |
|-------|------------------------------------|-------------|-------------------------------------|
| FR-01 | The system shall <!-- ... -->      | <!-- cap --> | <!-- e.g. Integration test: ... --> |
| FR-02 | The system shall <!-- ... -->      | <!-- cap --> | <!-- e.g. Unit test: ... -->        |

---

## Non-functional requirements

<!-- One row per requirement. ID format: NFR-NN.
     Covers constraints not captured by quality attributes below:
     e.g. technology stack, licensing, data volume, compliance. -->

| ID     | Description                              | Verification                     |
|--------|------------------------------------------|----------------------------------|
| NFR-01 | The system shall <!-- ... -->            | <!-- how to verify -->           |

---

## Quality attributes (ISO/IEC 25010)

<!-- Defines measurable quality targets for this project.
     For each characteristic: fill in Target and remove the Not applicable line.
     If not applicable: remove Target and replace Not applicable with the reason.
     Targets here are the acceptance criteria for non-functional verification. -->

### Functional suitability
<!-- Does the system do what it is supposed to do, correctly and completely? -->
- Target: <!-- e.g. All FR pass their defined verification tests -->
- Not applicable:

### Performance efficiency
<!-- Response time, throughput, resource usage under expected load. -->
- Target: <!-- e.g. Each unit of work processed in < 5 s on reference hardware -->
- Not applicable:

### Compatibility
<!-- Can the system coexist and interoperate with other systems? -->
- Target: <!-- e.g. Compatible with Python 3.11+, Windows and Linux -->
- Not applicable:

### Usability
<!-- How easy is it to learn, operate and recover from errors? -->
- Target: <!-- e.g. A new user can run the system following README in < 10 min -->
- Not applicable:

### Reliability
<!-- Availability, fault tolerance, recoverability. -->
- Target: <!-- e.g. No data loss on unexpected exit; recoverable from last checkpoint -->
- Not applicable:

### Security
<!-- Confidentiality, integrity, authentication, non-repudiation. -->
- Target: <!-- e.g. No credentials in source code; all secrets via .env -->
- Not applicable:
- See also: 04-dev-practices.md § Security

### Maintainability
<!-- How easy is it to analyse, modify, test and reuse the code? -->
- Target: <!-- e.g. Each component has unit tests; cyclomatic complexity < 10 per function -->
- Not applicable:
- See also: dev-rules.md, 04-dev-practices.md

### Portability
<!-- How easily can the system be moved to a different environment? -->
- Target: <!-- e.g. Runs on Windows and Linux without code changes -->
- Not applicable:
- See also: dev-rules.md (pathlib, UTF-8)

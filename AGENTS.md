# Agent Instructions

Welcome! You are an AI agent working on this project. This repository follows a strict spec-driven, incremental development framework.

## Your First Steps
1. **Restore Context (Memory)**: Read `specs/00-working-notes.md` immediately. This acts as your `memory.md` to understand the current project state, active goals, tracked development time, and exactly where the last session ended.
2. **Understand the Project**: Review the core specs in the `specs/` directory:
   - `01-vision.md` (Vision and Goals)
   - `02-requirements.md` (Functional & Non-Functional Requirements)
   - `03-architecture.md` (Architecture and Components)
3. **Follow the Rules**: Read `specs/04-dev-practices.md` for coding style, testing, and branching strategies.

## Project Workflow

Follow this incremental workflow for every project and feature:

1. **Specify**: Work with the user to define or update the vision, scope and
   requirements in `specs/01-vision.md` and `specs/02-requirements.md`.
   Complete any applicable extended specs (`05`–`10`). Present the affected
   specifications and wait for the user's explicit approval before continuing
   to planning or implementation.

2. **Plan**: Define the components, technical decisions and verification approach
   in `specs/03-architecture.md` and applicable specs. Record pending and confirmed
   decisions in `specs/00-working-notes.md`.

3. **Tasks**: Break approved work into small, traceable increments. Record the
   immediate next step in `specs/00-working-notes.md`; each increment must reference
   its requirement(s) and verification.

4. **Implement**: Implement only the approved increment. Follow
   `specs/04-dev-practices.md` and add or update the tests required by the relevant
   requirements.

5. **Converge**: Run the applicable checks and tests. Update affected specs, the
   README and, when used, `specs/09-test-log.md`. Finish by updating
   `specs/00-working-notes.md` with progress, decisions and the next step.

## Rules of Engagement
- **Spec First**: Never write code without an approved spec. If a requirement is missing, update the relevant spec and ask the user for approval first.
- **Update Memory**: At the end of every work session, you MUST update `specs/00-working-notes.md` with the progress made, pending decisions, and next steps for the next session. Make sure to update the "Last Updated" timestamp and increment the "Development Time Tracked".
- **Traceability**: Ensure every code change satisfies a requirement in `02-requirements.md`. Every test must trace back to a functional requirement or quality attribute.

# Agent Instructions

Welcome! You are an AI agent working on this project. This repository follows a strict spec-driven, incremental development framework.

## Your First Steps
1. **Restore Context (Memory)**: Read `specs/00-working-notes.md` immediately. This acts as your `memory.md` to understand the current project state, active goals, tracked development time, and exactly where the last session ended.
2. **Understand the Project**: Review the core specs in the `specs/` directory:
   - `01-vision.md` (Vision and Goals)
   - `02-requirements.md` (Functional & Non-Functional Requirements)
   - `03-architecture.md` (Architecture and Components)
3. **Follow the Rules**: Read `specs/04-dev-practices.md` for coding style, testing, and branching strategies.

## Rules of Engagement
- **Spec First**: Never write code without an approved spec. If a requirement is missing, update the relevant spec and ask the user for approval first.
- **Update Memory**: At the end of every work session, you MUST update `specs/00-working-notes.md` with the progress made, pending decisions, and next steps for the next session. Make sure to update the "Last Updated" timestamp and increment the "Development Time Tracked".
- **Traceability**: Ensure every code change satisfies a requirement in `02-requirements.md`. Every test must trace back to a functional requirement or quality attribute.

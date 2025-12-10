# Rules for AI Collaboration and OpenSpec

## 1. Purpose

All development in this repository follows Lich Architecture and is coordinated through OpenSpec. A single OpenSpec instance exists in the project root, acting as the shared source of truth for human-AI collaboration.

## 2. Required Context Files

Every AI assistant or developer must read and understand the following documents before writing code:

1.  `openspec/design-guidelines.md`: Technical and design conventions (Lich Architecture).
2.  `openspec/architecture.md`: High-level system architecture and module responsibilities.
3.  `openspec/rules.md`: Collaboration and workflow principles (this file).

These documents together define how all modules (frontend, backend, admin-panel, infra) must be built and maintained.

## 3. Core Principles

- Each feature begins as an OpenSpec change file under `openspec/spec/changes/`.
- Code must implement *only* what is defined in the corresponding spec.
- Before coding, AI should read all active specs (`changes/`) and follow the latest guidelines.
- Humans validate and approve changes before merge.
- Archived specs in `openspec/spec/archived/` are immutable.

## 4. Development Workflow

1.  **Describe Feature**: Developer or AI creates a change entry via chat or CLI.
2.  **Draft Spec**: AI writes summary, details, and validation steps in `openspec/spec/changes/`.
3.  **Approval**: Once reviewed, coding starts.
4.  **Implementation**: Code must respect the design and architecture conventions.
5.  **Validation**: Run tests, review code.
6.  **Archive**: When done, run `openspec archive <change>` and merge.

## 5. Behavioral Rules for AI Agents

- Always check whether a spec already exists before creating a new one.
- Do **not** modify other modules unless the spec explicitly lists them.
- Follow structure, naming, and layering rules in `design-guidelines.md`.
- Confirm cross-module impacts with the human owner before committing.
- Produce concise, readable, and modular code.
- **Testing is mandatory**: For any new feature or bug fix, the AI agent must provide corresponding unit, integration, or end-to-end tests.
- **Dependency Management**: Do not add new dependencies without prior approval. If a new dependency is required, justify its use in the spec.
- **Security**: All code must adhere to security best practices. This includes input validation, parameterized queries to prevent SQL injection, and proper handling of sensitive data.

## 6. Commit & PR Policy

- Each commit must reference its related spec file (e.g., `openspec/spec/changes/add-login.md`).
- Pull requests must include the spec ID in the title or description.
- Cross-module PRs must tag affected folders.
- PRs must include a summary of the changes and a link to the corresponding spec.
- All PRs must pass automated checks (linting, testing, etc.) before they can be merged.

## 7. Communication & Conflict Resolution

- If an AI finds unclear instructions, it must pause and request clarification.
- Humans have final decision authority.
- All discussions leading to a design decision should be summarized in OpenSpec.

## 8. Enforcement

- Failure to follow these rules results in rejection of code during review or automated CI checks.
- Consistency, readability, and adherence to architecture principles are mandatory.

## 9. Auto-Documentation Rule

Every AI agent is responsible for keeping the root `README.md` fully up-to-date. Whenever a new feature, module, or architectural change is introduced, the agent must update the `README.md` automatically to reflect the current project status and explain the changes it has made.

*Remember:*

- Read `design-guidelines.md` and `architecture.md` before every new change.
- Implement *exactly* what the spec defines—nothing more, nothing less.

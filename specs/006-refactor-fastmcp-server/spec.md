# Feature Specification: Refactor fastmcp_server to use @mcp.prompt

**Feature Branch**: `006-refactor-fastmcp-server`  
**Created**: 2025-10-18
**Status**: Draft  
**Input**: User description: "Refactor fastmcp_server to use @mcp.prompt, removing the AGENTS.md dependency."

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a package maintainer, I want to embed the agent's instructions directly into the Python code using `@mcp.prompt` so that end-users do not need to manage a separate `AGENTS.md` context file, simplifying distribution and usage.

### Acceptance Scenarios
1. **Given** the `mcts-gen` package is installed, **When** the `fastmcp_server` is run, **Then** it MUST offer the `mcts_autonomous_search` prompt without requiring an `AGENTS.md` file.
2. **Given** the project source, **When** the package is built, **Then** the `AGENTS.md` file MUST NOT be included in the final distribution.
3. **Given** the documentation, **When** a user reads `README.md` or `docs/quickstart.rst`, **Then** they MUST be informed that prompts are built-in and instructed on how to provide *additional* context if needed.
4. **Given** the project configuration, **When** `pyproject.toml` and `docs/conf.py` are inspected, **Then** the version MUST be `0.0.2`.

### Edge Cases
- **What happens if a user provides their own `AGENTS.md` through a separate configuration?** The server should prioritize its built-in prompts. The documentation should clarify this behavior, stating that user-provided context is for *additional* instructions, not for overriding the core prompts.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The `fastmcp_server.py` MUST be refactored to define the MCTS agent's core workflow and instructions using the `@mcp.prompt` decorator.
- **FR-002**: The `src/mcts_gen/AGENTS.md` file MUST be deleted from the source tree.
- **FR-003**: The `pyproject.toml` file MUST be modified to remove the `package-data` entry for `AGENTS.md`.
- **FR-004**: The `version` in `pyproject.toml` MUST be updated to `0.0.2`.
- **FR-005**: The `version` in `docs/conf.py` MUST be updated to `0.0.2`.
- **FR-006**: `README.md` MUST be updated to explain that core prompts are now built-in and to guide users on how to supply additional, custom context.
- **FR-007**: `docs/quickstart.rst` MUST be updated with the same information as `README.md` regarding the new prompt mechanism.

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous  
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] User scenarios defined
- [ ] Requirements generated
- [ ] Entities identified
- [ ] Review checklist passed

---
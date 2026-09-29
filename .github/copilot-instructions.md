# Copilot Instructions — Recipe Information System

## 1. Project Context

This is a university student project and an MVP.

The project is an Information System for storing recipes and finding
recipes based on available ingredients.

The goal is a useful, understandable, and realistically implementable
student project — NOT an enterprise production system.

## 2. CHILL BRO RULE

"CHILL BRO" means:

Keep the solution useful, simple, realistic, and proportional to a
university MVP.

Prefer:
- simple solutions;
- clear requirements;
- realistic student-level implementation;
- objectively verifiable requirements;
- the minimum necessary complexity.

Do NOT:
- overengineer;
- introduce enterprise-level architecture or infrastructure;
- invent scalability, availability, performance, compliance, or
  security requirements without justification;
- invent arbitrary numerical targets;
- introduce unsupported technologies or platforms;
- add unnecessary abstractions;
- expand the project scope;
- create requirements just to make the specification look
  more sophisticated.

If a proposed idea would normally make sense for a large commercial
system but is unnecessary for this university MVP, flag it instead
of adding it.

"Useful and sufficient" is preferred over
"comprehensive and enterprise-grade."

## 3. Source of Truth

The approved SKED decisions, glossary, Functional Requirements
(REQ-F), and Non-Functional Requirements (REQ-NF) are the current
sources of truth.

Do not:
- introduce functionality that was not approved;
- silently change approved business rules;
- introduce new roles or permissions;
- contradict existing requirements;
- invent missing product decisions when they are not necessary.

When something is genuinely unclear, identify the ambiguity.
When a reasonable assumption is sufficient, prefer the smallest
assumption consistent with the existing project decisions.

## 4. Scope Discipline

The approved roles are exactly:

- Visitor
- Registered user

Do not introduce additional roles.

The MVP currently excludes, among other things:

- admin/moderator roles;
- ratings;
- likes;
- comments;
- follows;
- password recovery;
- profile management;
- username changes;
- recommendation systems;
- unrelated social features.

Do not add excluded functionality unless explicitly approved later.

## 5. Specification Discipline

When creating or reviewing specifications:

- Do not over-fragment requirements.
- Consolidate closely related behavior into logical requirements.
- Keep requirements objectively verifiable where applicable.
- Use stable requirement identifiers.
- Use terminology from the approved glossary consistently.
- Preserve traceability between requirements, acceptance criteria,
  BDD scenarios, tests, implementation, and documentation.
- Do not create multiple requirements that merely restate the same
  behavior from different wording.

## 6. No Unsupported Metrics

Do not invent arbitrary values for:

- response time;
- availability;
- uptime;
- concurrent users;
- database size;
- file size;
- network speed;
- scalability;
- recovery time;
- security strength;
- supported platforms.

Only introduce numerical constraints when they are explicitly
approved or clearly justified by the project.

## 7. Working Style

When asked to generate or review something:

1. Use the existing project decisions.
2. Check for contradictions and scope creep.
3. Prefer the simplest sufficient solution.
4. Do not add functionality while "improving" wording.
5. Do not turn a student MVP into an enterprise system.
6. If asked to propose changes before editing files, show the
   proposal first and do not modify files.

## 8. Quality Check

Before finalizing generated requirements or project artifacts,
check for:

- scope creep;
- duplicated requirements;
- contradictions;
- ambiguous wording;
- untestable requirements;
- unsupported assumptions;
- unnecessary complexity;
- terminology inconsistencies;
- missing traceability.

Keep the project practical and implementable by a student team.
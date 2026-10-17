# Lab 3 Implementation Plan

## Status and Baseline

This is a draft for review. It does not approve the plan or start implementation.

- Approved Lab 2 baseline: `f76729c8c232f817c6f07de8106d959c2f4ffe12`
- PLAN-GATE: Issue #3, currently open
- Ingredient identity Gate: Issue #4, closed
- Issue #4 decision: singular/plural normalization is excluded; matching uses standardized catalog identities; manual ingredient entry remains excluded.

## Responsibilities

### Student

- Decide `GO` or `REVISE` on Issue #3.
- Make scope and requirement decisions.
- Review Feature deliverables and acceptance evidence.
- Approve verification evidence and close Gates.
- Decide whether work is accepted as complete.

### Coding Agent

- Implement only approved Feature Issue scope after Issue #3 is `GO`.
- Use the exact REQ, AC, and BDD references in each Issue.
- Run focused checks and report evidence, failures, and uncertainty.
- Do not decide requirements, scope, Gate outcomes, or human validation.
- Do not add manual ingredient entry, singular/plural normalization, synonym matching, or excluded features.

### Shared

- Review source mappings and dependencies.
- Perform or inspect verification activities.
- Maintain requirement-to-issue traceability after approval.
- Review risks and confirm that evidence supports closure.

## Gate Rules

- No Feature Issue may start implementation before the Student records `GO` on Issue #3.
- `REVISE` on Issue #3 returns the plan for revision; Feature work remains blocked.
- Issue #3 and Issue #4 produce decisions and evidence, not application code or tests.
- Issue #4 is already closed with normalization excluded and therefore does not block Issue #7 anymore.
- Human validation, requirement decisions, and Gate decisions remain with the Student.

## Phases and Estimates

Estimates are planning estimates, not measured effort or requirements.

| Phase | Issues | Estimate | Exit condition |
|---|---|---:|---|
| Plan approval | #3 | 0.5-1 day | Student records `GO` |
| Authentication | #5 | 1-2 days | Student reviews authentication evidence |
| Recipe lifecycle | #6 | 2-3 days | Student reviews recipe evidence |
| Search and matching | #7 | 2-3 days | Matching and search evidence is reviewed |
| Photo management | #9 | 1-2 days | Photo evidence is reviewed |
| Collection and details | #8 | 1-2 days | Browsing/details evidence is reviewed |
| Final verification | #10 | 1-2 days | Student accepts verification evidence |

## Gantt-Style Schedule

This is a dependency-based sequence, not a calendar commitment.

| Work | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Issue #3 PLAN-GATE | Review | GO/REVISE |  |  |  |  |  |  |  |  |
| Issue #5 Authentication |  |  | Work | Work | Review |  |  |  |  |  |
| Issue #6 Recipe lifecycle |  |  |  | Work | Work | Work | Review |  |  |  |
| Issue #7 Search/matching |  |  |  |  |  | Work | Work | Work | Review |  |
| Issue #9 Photos |  |  |  |  |  | Work | Work | Review |  |  |
| Issue #8 Collection/details |  |  |  |  |  |  |  | Work | Review |  |
| Issue #10 Verification |  |  |  |  |  |  |  |  |  | Verify/review |

The schedule starts only after Issue #3 receives `GO`. Actual dates and effort must be recorded separately from these estimates.

## Issue Dependencies

- #3: no dependency; blocks all Feature implementation until Student `GO`.
- #4: closed; normalization decision is complete and does not block remaining work.
- #5: depends on #3 `GO`.
- #6: depends on #3 `GO` and #5.
- #7: depends on #3 `GO`, #6, and the completed decision in #4.
- #9: depends on #3 `GO`, #5, and #6.
- #8: depends on #3 `GO`, #6, #7, and #9.
- #10: depends on #3 `GO` and completed relevant Features #5-#9.

## Critical Path

The main critical path is:

`#3 GO -> #5 -> #6 -> #7 -> #8 -> #10`

Issue #9 can proceed in parallel after #5 and #6, but #8 requires both #7 and #9. Therefore photo work can become part of the effective critical path if it finishes later than search work.

## Human Review Effort

These are estimates, not measured effort:

- Issue #3 plan review: 30-60 minutes.
- Issues #5 and #9 review: about 30 minutes each.
- Issues #6, #7, and #8 review: 45-60 minutes each.
- Issue #10 evidence review: about 60 minutes.

## Definition of Done

A Feature is Done only when:

- its approved scope is implemented;
- exact source IDs remain traceable;
- relevant acceptance criteria are checked;
- explicitly mapped BDD scenarios are verified where applicable;
- applicable NFR verification is completed;
- no excluded functionality is added;
- evidence is available for Student review;
- the Student accepts the result.

Issue #10 is Done only when all relevant Feature evidence is checked, failures are recorded with exact IDs, and the Student accepts the verification result. A Gate is Done only when the Student records its decision.

## Proposed Traceability Update

Do not apply this update yet. After the Student approves the plan, add an Issue column to `spec/traceability.md` using the existing Issue IDs:

| Issue | Source coverage |
|---|---|
| #5 | REQ-F-001-009; REQ-NF-005-007; AC-001-005; BDD: Register and log in as a Registered User; Prompt a Visitor to authenticate before a restricted action |
| #6 | REQ-F-010-022; REQ-NF-002, REQ-NF-003, REQ-NF-006, REQ-NF-008; AC-006-012; BDD: Create a valid recipe; Reject an invalid recipe; Edit and delete a user's own recipe |
| #7 | REQ-F-023-034; REQ-NF-001, REQ-NF-004, REQ-NF-006; AC-013-020; BDD: four ingredient-search scenarios |
| #8 | REQ-F-035-038; REQ-NF-001, REQ-NF-004; AC-021-023; BDD: UNCONFIRMED, no direct scenario |
| #9 | REQ-F-039-045; REQ-NF-002, REQ-NF-003, REQ-NF-006, REQ-NF-008; AC-024-027; BDD: Manage recipe and cooked-dish photos according to permissions |
| #10 | Verification of REQ-F-001-045, REQ-NF-001-012, AC-001-027, and all explicitly mapped BDD scenarios |

Issues #3 and #4 are Gates and should be recorded as approval/decision evidence rather than implementation traceability.

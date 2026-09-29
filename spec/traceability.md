# Requirements Traceability Matrix

This matrix links the approved functional and non-functional requirements to their acceptance criteria and, where applicable, the existing BDD scenarios.

## Functional Requirements

| Requirement ID | Requirement Type | Acceptance Criteria | BDD Scenario | Verification / Notes |
|---|---|---|---|---|
| REQ-F-001 | Functional | AC-001 | — | Covered by role and access-control acceptance testing. |
| REQ-F-002 | Functional | AC-001, AC-015, AC-021 | — | Visitor browsing and search access are covered by acceptance testing; no direct BDD scenario. |
| REQ-F-003 | Functional | AC-001 | — | Covered by role and access-control acceptance testing; no direct BDD scenario. |
| REQ-F-004 | Functional | AC-002, AC-003 | Register and log in as a Registered User | Directly covered by the registration scenario. |
| REQ-F-005 | Functional | AC-003 | Register and log in as a Registered User | Directly covered by the registration and login scenario. |
| REQ-F-006 | Functional | AC-003 | — | Authentication failure behavior has no direct BDD scenario. |
| REQ-F-007 | Functional | AC-004 | Prompt a Visitor to authenticate before a restricted action | Directly covered by the authentication-prompt scenario. |
| REQ-F-008 | Functional | AC-004 | Prompt a Visitor to authenticate before a restricted action | Directly covered by the authentication-prompt scenario. |
| REQ-F-009 | Functional | AC-005 | — | Verified by inspection of excluded account functionality. |
| REQ-F-010 | Functional | AC-006, AC-009 | Create a valid recipe; Reject an invalid recipe | Directly covered by recipe-creation scenarios. |
| REQ-F-011 | Functional | AC-006 | Create a valid recipe | Directly covered at the recipe-creation level. |
| REQ-F-012 | Functional | AC-006 | — | No direct BDD scenario for quantity formats. |
| REQ-F-013 | Functional | AC-006 | — | No direct BDD scenario for the complete unit list. |
| REQ-F-014 | Functional | AC-006 | — | No direct BDD scenario for duplicate catalog ingredients. |
| REQ-F-015 | Functional | AC-007 | Create a valid recipe; Reject an invalid recipe | Directly covered for ordered non-empty preparation steps. |
| REQ-F-016 | Functional | AC-007, AC-009 | Reject an invalid recipe; Edit and delete a user's own recipe | Directly covered for invalid creation and acceptance-tested for editing. |
| REQ-F-017 | Functional | AC-008 | — | No direct BDD scenario for optional metadata. |
| REQ-F-018 | Functional | AC-010 | Edit and delete a user's own recipe | Directly covered by the recipe-management scenario. |
| REQ-F-019 | Functional | AC-010 | Edit and delete a user's own recipe | Directly covered for valid edits and acceptance-tested for invalid edits. |
| REQ-F-020 | Functional | AC-011 | Create a valid recipe; Edit and delete a user's own recipe | Directly covered for newly saved recipes and valid edits. |
| REQ-F-021 | Functional | AC-012 | Edit and delete a user's own recipe | Directly covered by the recipe-deletion scenario. |
| REQ-F-022 | Functional | AC-012 | Edit and delete a user's own recipe | Directly covered by the recipe-deletion scenario. |
| REQ-F-023 | Functional | AC-013 | — | No direct BDD scenario for catalog administration restrictions. |
| REQ-F-024 | Functional | AC-013 | — | Standardized catalog identity consistency is covered by acceptance testing; no direct BDD scenario. |
| REQ-F-025 | Functional | AC-013 | Ignore Basic and Optional ingredients during matching | Directly covered for recipe-specific classification behavior. |
| REQ-F-026 | Functional | AC-014, AC-018 | — | No direct BDD scenario for stored quantities and units not affecting matching. |
| REQ-F-027 | Functional | AC-015, AC-016 | Find a recipe that can be prepared now; Find a recipe that is almost possible to prepare; Exclude recipes missing three or more Essential ingredients; Ignore Basic and Optional ingredients during matching | Directly covered by ingredient-selection scenarios. |
| REQ-F-028 | Functional | AC-015 | — | No direct BDD scenario for the empty-selection message. |
| REQ-F-029 | Functional | AC-016 | Find a recipe that can be prepared now | Directly covered for evaluation against the selected set. |
| REQ-F-030 | Functional | AC-017 | Find a recipe that can be prepared now; Find a recipe that is almost possible to prepare; Exclude recipes missing three or more Essential ingredients | Directly covers all three matching outcomes. |
| REQ-F-031 | Functional | AC-018 | Ignore Basic and Optional ingredients during matching | Directly covered by the matching scenario. |
| REQ-F-032 | Functional | AC-019 | — | No direct BDD scenario for changing selections and explicit rerun. |
| REQ-F-033 | Functional | AC-020 | — | No direct BDD scenario for the empty result state. |
| REQ-F-034 | Functional | AC-020, AC-021 | — | No direct BDD scenario for result ordering. |
| REQ-F-035 | Functional | AC-021 | — | No direct BDD scenario for collection browsing order. |
| REQ-F-036 | Functional | AC-022 | Find a recipe that is almost possible to prepare | Directly covered for Almost can cook result content. |
| REQ-F-037 | Functional | AC-023 | — | No direct BDD scenario for the complete details view. |
| REQ-F-038 | Functional | AC-023 | — | No direct BDD scenario; exclusion is verified by inspection. |
| REQ-F-039 | Functional | AC-024 | Manage recipe and cooked-dish photos according to permissions | Directly covered by the photo-management scenario. |
| REQ-F-040 | Functional | AC-024 | Manage recipe and cooked-dish photos according to permissions | Directly covered for recipe-photo removal and confirmation. |
| REQ-F-041 | Functional | AC-025 | — | No direct BDD scenario for invalid photo uploads. |
| REQ-F-042 | Functional | AC-026 | Manage recipe and cooked-dish photos according to permissions | Directly covered for registered-user contribution. |
| REQ-F-043 | Functional | AC-026 | Manage recipe and cooked-dish photos according to permissions | Directly covered for contributor identity and one active photo. |
| REQ-F-044 | Functional | AC-026 | Manage recipe and cooked-dish photos according to permissions | Directly covered for contributor permissions. |
| REQ-F-045 | Functional | AC-027 | Manage recipe and cooked-dish photos according to permissions | Directly covered for cooked-dish photo removal confirmation. |

## Non-Functional Requirements

| Requirement ID | Requirement Type | Acceptance Criteria | BDD Scenario | Verification / Notes |
|---|---|---|---|---|
| REQ-NF-001 | Non-functional | — | — | Glossary terminology consistency; verification by inspection of requirements and BDD artifacts. |
| REQ-NF-002 | Non-functional | AC-003, AC-006, AC-007, AC-009, AC-010, AC-025 | — | Clear feedback is covered by acceptance testing; no direct BDD scenario. |
| REQ-NF-003 | Non-functional | AC-012, AC-024, AC-027 | Edit and delete a user's own recipe; Manage recipe and cooked-dish photos according to permissions | Confirmation wording is represented by the relevant BDD scenarios. |
| REQ-NF-004 | Non-functional | AC-022, AC-023 | — | Readable and consistent presentation; verification by inspection and demonstration. |
| REQ-NF-005 | Non-functional | — | — | Password storage quality requirement; verification by inspection and analysis. |
| REQ-NF-006 | Non-functional | AC-001, AC-004, AC-010, AC-012, AC-024, AC-026 | Prompt a Visitor to authenticate before a restricted action; Edit and delete a user's own recipe; Manage recipe and cooked-dish photos according to permissions | Cross-cutting permission enforcement; no single BDD scenario covers all operations. |
| REQ-NF-007 | Non-functional | AC-002, AC-023 | Register and log in as a Registered User | Public identity and email exposure are represented in registration/details behavior. |
| REQ-NF-008 | Non-functional | AC-010, AC-012, AC-024, AC-025, AC-026 | Edit and delete a user's own recipe; Manage recipe and cooked-dish photos according to permissions | Persistence integrity across failed updates and photo operations; verified by acceptance testing. |
| REQ-NF-009 | Non-functional | AC-003, AC-025 | — | Technical error-detail handling; no direct BDD scenario. |
| REQ-NF-010 | Non-functional | — | — | Inspection of requirements artifacts confirms unique stable identifiers. |
| REQ-NF-011 | Non-functional | — | — | Inspection of requirements artifacts confirms consistent glossary terms and identifiers. |
| REQ-NF-012 | Non-functional | — | — | Inspection of requirements artifacts confirms unambiguous artifact traceability. |

## Coverage Check

- **Total functional requirements:** 45, from REQ-F-001 through REQ-F-045.
- **Total non-functional requirements:** 12, from REQ-NF-001 through REQ-NF-012.
- **Functional requirements without AC coverage:** None.
- **Non-functional requirements without AC coverage:** REQ-NF-001, REQ-NF-005, REQ-NF-010, REQ-NF-011, and REQ-NF-012. These are verified through inspection or analysis rather than behavior-focused acceptance criteria.
- **Functional requirements without direct BDD coverage:** REQ-F-001, REQ-F-002, REQ-F-003, REQ-F-006, REQ-F-009, REQ-F-012, REQ-F-013, REQ-F-014, REQ-F-017, REQ-F-023, REQ-F-024, REQ-F-026, REQ-F-028, REQ-F-032, REQ-F-033, REQ-F-034, REQ-F-035, REQ-F-037, REQ-F-038, and REQ-F-041. These are covered by the acceptance criteria and are intentionally not forced into the initial 10-scenario BDD specification.
- **Inconsistencies found:** None in the approved IDs or mappings. `spec/srs.tex` was referenced as a source artifact but is not currently present in the repository; no new requirement content was inferred from that missing file.

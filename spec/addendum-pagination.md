# Specification Addendum: Recipe Collection Pagination

## Status and scope

This addendum specifies paginated retrieval of the shared recipe collection through `GET /api/recipes`. It supplements the approved baseline requirement `REQ-F-035` and acceptance criterion `AC-021`; it does not replace either one.

Pagination applies only to collection browsing. Recipes remain in the existing collection order, and the response retains the existing `{ "items": [...] }` structure without pagination metadata. This addendum does not change ingredient matching or introduce other features.

## Additional requirements

| ID | Requirement |
|---|---|
| ADD-F-001 | The system shall support paginated retrieval of the shared recipe collection through `GET /api/recipes`. |
| ADD-F-002 | The optional `page` and `pageSize` query parameters shall default to 1 and 10 respectively; each supplied value shall be an integer greater than or equal to 1. |
| ADD-F-003 | The system shall return only recipes belonging to the requested page, in the existing collection order. A valid page beyond the collection shall return HTTP 200 and an empty `items` array. |

## Additional acceptance criteria

| ID | Acceptance criterion |
|---|---|
| ADD-AC-001 | When both parameters are omitted, the response contains the first page with a page size of 10. |
| ADD-AC-002 | Valid parameters return the corresponding slice of the collection in its existing order. |
| ADD-AC-003 | A valid page beyond the collection returns HTTP 200 with `items: []`. |
| ADD-AC-004 | A `page` or `pageSize` below 1 is rejected with a validation error. |

## Existing implementation and contract at addendum review

Pagination behavior predates this addendum. The `src/main.py` version at commit `c1e1170`, which is an ancestor of the preserved checkpoint `1146a32`, already declares `page=1` and `pageSize=10`, constrains both to values of at least 1, and returns the corresponding slice of `RECIPES`. The pre-existing `docs/openapi.yaml` already declares both optional query parameters with a minimum of 1. This addendum documents and approves that existing behavior; it is not evidence that pagination was newly implemented as part of this addendum.

## SPEC-ADDENDUM-GATE

**Decision: GO.**

The extension is within the established shared-collection browsing scope of `REQ-F-035` and `AC-021`. It makes the already declared query parameters' defaults and behavior explicit, preserves the established order and response structure, and adds no conflicting matching rules or unrelated capabilities. The OpenAPI parameter definitions and existing implementation provide a consistent basis for acceptance verification. The gate approves the requirements above for verification and traceability.

## TDD evidence deviation

A genuine RED/GREEN cycle was not demonstrated. The approved behavior was already implemented in committed code before this addendum was written. Producing a RED result would require intentionally breaking that pre-existing behavior, which would undermine the preserved checkpoint and is not justified. Focused tests were used to verify and characterize the existing behavior; their passing result is not represented as a TDD RED/GREEN cycle. No implementation change was required for this extension.

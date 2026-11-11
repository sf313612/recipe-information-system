# Lab 5 — TDD, Refactoring and Validation Log

## 1. Baseline verification

- Restored the original committed implementation after an unsuccessful broad refactoring attempt.
- Restarted the API server to clear in-memory state.
- Ran the full test suite.
- Result: 36 passed, 1 non-blocking AnyIO warning.

## 2. Controlled refactoring

- Used GitHub Copilot Agent for a planning-only analysis of:
  - src/main.py
  - src/schemas.py
  - tests/api/test_catalog_and_recipes.py
- Approved one isolated refactoring task: extract the ingredient catalog and its two read-only endpoints into src/routers/ingredients.py.
- Preserved the shared INGREDIENTS catalog by importing it into src/main.py.
- Registered the new router using app.include_router().
- No changes to schemas, tests, or OpenAPI contract.

## 3. Verification

- Focused tests: 2 passed, 17 deselected.
- Full regression suite: 36 passed, 1 non-blocking AnyIO warning.
- Reviewed the source diff and new router implementation.
- Confirmed the 404 behavior for unknown ingredient IDs is preserved in the implementation.

## 4. Git checkpoint

- Commit: 1146a32
- Message: refactor: extract ingredient catalog router
- Working tree clean after commit.

## 5. Current status

- Baseline implementation and controlled refactoring completed.
- SPEC Addendum, SPEC-ADDENDUM-GATE, and the extension TDD cycle are pending.

## 6. Pagination addendum and SPEC-ADDENDUM-GATE (2026-11-11)

- Reviewed `spec/srs.tex`; it is present and contains `REQ-F-035` and `AC-021`. Corrected the stale statement in `spec/traceability.md` that claimed the SRS was missing. The SRS itself was not modified.
- Confirmed that the `src/main.py` at ancestor commit `c1e1170` already implemented pagination: `page=1`, `pageSize=10`, minimum values of 1, and ordered collection slicing. The existing OpenAPI contract already declared both optional parameters with a minimum of 1. The implementation and contract therefore predate the addendum and checkpoint `1146a32`.
- Added `spec/addendum-pagination.md` with ADD-F-001--ADD-F-003, ADD-AC-001--ADD-AC-004, provenance, and the TDD deviation.
- SPEC-ADDENDUM-GATE: **GO**, committed before implementation changes as `ee8bdf7` (`docs: approve recipe pagination addendum`). The extension aligns with `REQ-F-035` / `AC-021`, clarifies existing parameter behavior, and preserves the existing response envelope and ordering.

## 7. Pagination verification and TDD deviation (2026-11-11)

- Added focused characterization tests for omitted defaults, requested page slicing and order, a page beyond the collection, validation below 1, and the unchanged `{ "items": [...] }` envelope.
- A genuine TDD RED/GREEN cycle was **not** demonstrated. The desired behavior already existed in committed code; causing RED would have required deliberately breaking it. No RED result is claimed and no pagination implementation code was changed.
- The first focused test attempt failed at collection because the new parameterized test lacked `import pytest`; that test setup error was fixed. The next attempt could not connect because the expected API server was not running. Started the repository's Uvicorn app locally and reran the focused tests: **6 passed, 18 deselected, 1 existing AnyIO deprecation warning**.
- Full regression suite against that running app: **41 passed, 1 existing AnyIO deprecation warning**. Used `-p no:cacheprovider` because this sandbox cannot write the repository's pytest cache.
- Updated `docs/openapi.yaml` after the GO gate to document defaults 1 and 10 and the existing minimums. Parsed the YAML and checked those values against FastAPI's generated OpenAPI schema; both agreed.
- Added the addendum requirement/acceptance/test mapping to `spec/traceability.md`; the original Lab 2 requirement totals remain unchanged.

## 8. Refactoring review and manual validation (2026-11-11)

- Reviewed the existing pagination handler and the ingredient router extraction at checkpoint `1146a32`. The pagination handler is a small direct slice over the ordered collection; no additional structural refactor was needed, and changing it would add risk without improving clarity. No source implementation changes were made for pagination.
- Manual API-level validation against the local Uvicorn app returned HTTP 200 for the ingredient catalog, recipe collection, recipe details, and ingredient search. Pagination returned the first requested item, a valid out-of-range page returned HTTP 200 with `items: []`, and `pageSize=0` returned HTTP 422.
- No separate student UI walkthrough is claimed; the project validation available here is API-level.

## 9. Attribution and final Lab 5 decision (2026-11-11)

- **GitHub Copilot Agent (historical):** Project history records an earlier broad refactoring attempt that failed and was reverted. The retained ingredient-router task is recorded above as having received planning-only Copilot analysis. No pagination implementation work is attributed to Copilot; it predates this addendum.
- **Codex (this continuation):** Authored the pagination addendum and gate, added characterization tests, clarified OpenAPI defaults, corrected and extended traceability, ran focused/full/API contract checks, reviewed the existing implementation, and updated this log.
- **Manual validation:** The API-level smoke checks listed above were run directly against the local app by Codex. The user selected the preserve-existing-behavior path.
- **Final decision: GO.** The approved addendum is implemented in the preserved pre-existing behavior; focused checks, full regression, contract consistency, traceability, and API-level validation passed. The documented limitation is that RED/GREEN TDD evidence cannot honestly be produced for behavior that was already committed; no implementation refactor was needed.
- **Checkpoints:** Preserved `1146a32`. Additional commits: `ee8bdf7` (addendum and gate), `acde63d` (pagination characterization tests), and `403a27b` (OpenAPI and traceability).

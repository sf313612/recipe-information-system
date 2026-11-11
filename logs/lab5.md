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

## 9. Attribution and pagination-stage decision (2026-11-11)

- **GitHub Copilot Agent (historical):** Project history records an earlier broad refactoring attempt that failed and was reverted. The retained ingredient-router task is recorded above as having received planning-only Copilot analysis. No pagination implementation work is attributed to Copilot; it predates this addendum.
- **Codex (this continuation):** Authored the pagination addendum and gate, added characterization tests, clarified OpenAPI defaults, corrected and extended traceability, ran focused/full/API contract checks, reviewed the existing implementation, and updated this log.
- **Manual validation:** The API-level smoke checks listed above were run directly against the local app by Codex. The user selected the preserve-existing-behavior path.
- **Pagination-stage decision: GO.** The approved pagination addendum documents preserved pre-existing behavior; its focused checks, full regression, contract consistency, traceability, and recorded API-level validation passed. The documented limitation is that RED/GREEN TDD evidence cannot honestly be produced for behavior that was already committed; no implementation refactor was needed. This section's GO is the pagination-stage decision, not the final overall Lab 5 decision after the category-filter addendum.
- **Checkpoints:** Preserved `1146a32`. Additional commits: `ee8bdf7` (addendum and gate), `acde63d` (pagination characterization tests), and `403a27b` (OpenAPI and traceability).

## 10. Category-filter specification gate (2026-11-11)

- Updated `spec/addendum-recipe-category-filter.md` with the explicit query boundary: an empty `category` value is invalid; `Dessert` is valid; and a URL-encoded single space (`%20`) is valid as a literal value and is not trimmed or normalized.
- Strengthened the category-browsing BDD scenario to state that Soup recipes and recipes without category metadata are excluded from a Dessert-filtered response.
- The Student approved the addendum in principle and requested these clarifications. **SPEC-ADDENDUM-GATE decision: GO**, approved by the Student on 2026-11-11. Rationale: the filter uses existing optional recipe-category metadata, fits shared collection browsing, preserves current order and pagination, and does not alter ingredient matching or excluded MVP scope.
- Updated the category-filter traceability entry from pending gate recommendation to approved gate / implementation pending.
- This step changed specification and log documents only. Implementation, tests, and OpenAPI were not modified; no tests were run and no RED/GREEN evidence is claimed. The implementation phase remains pending.

## 11. Category-filter TEST-GATE proposal (2026-11-11)

- Added category-filter API tests only; no tests have been run yet.
- Planned coverage: ADD-AC-005 (category omitted preserves unfiltered results); ADD-AC-006 (exact case-sensitive match, excluding another category and uncategorized recipes, preserving order); ADD-AC-007 (filter before pagination); ADD-AC-008 (no match returns HTTP 200 and empty `items`); ADD-AC-009 (empty category returns HTTP 422). The encoded-space case explicitly checks that `%20` is treated as a literal category value.
- Expected RED: the current `list_recipes` accepts only `page` and `pageSize` and slices the full collection. FastAPI ignores the undeclared `category` query parameter, so category requests currently return unfiltered results; `?category=` is not validated as empty. The literal Dessert filter, exact-category filter, empty-result, empty-value, and encoded-space tests should therefore fail against this unchanged implementation. The separate no-category test should pass.
- TEST-GATE status: **GO — test set is ready for RED execution** after tightening the Dessert test to use a unique category and assert the exact returned ID list. Tests have not been run; no RED result is claimed. Implementation and test execution remain pending the next authorized phase.

## 12. Category-filter RED attempt (2026-11-11)

- Command: `pytest -p no:cacheprovider tests/api/test_catalog_and_recipes.py::test_browse_recipes_without_category_keeps_categorized_and_uncategorized_items tests/api/test_catalog_and_recipes.py::test_browse_recipes_accepts_dessert_category tests/api/test_catalog_and_recipes.py::test_browse_recipes_filters_exact_category_before_pagination tests/api/test_catalog_and_recipes.py::test_browse_recipes_rejects_empty_category tests/api/test_catalog_and_recipes.py::test_browse_recipes_treats_encoded_space_as_literal_category`
- Pytest collected exactly five selected tests. Result: **0 passed, 1 failed, 4 errors, 1 warning** in 22.65s.
- Errors: the four tests using `bearer_headers` errored during fixture setup when its registration request tried to connect to the API. The connection was refused (`httpx.ConnectError`, Windows `WinError 10061`) at `127.0.0.1:8000`.
- Failure: `test_browse_recipes_rejects_empty_category` failed on its API request with the same refused connection (`httpx.ConnectError`, Windows `WinError 10061`) at `127.0.0.1:8000`.
- Warning: the existing AnyIO plugin emitted `PytestRemovedIn10Warning` for `CallSpec2`.
- This run did **not** reach category-filter assertions. The outcome is an infrastructure block, not the expected RED caused by missing category filtering or empty-value validation. No functional RED result is claimed. The API server was not started or modified; implementation and tests remain unchanged.

## 13. Category-filter RED rerun (2026-11-11)

- Confirmed before execution that `git diff -- src/` was empty and selected only the five new category-filter test node IDs.
- Command: `pytest -p no:cacheprovider tests/api/test_catalog_and_recipes.py::test_browse_recipes_without_category_keeps_categorized_and_uncategorized_items tests/api/test_catalog_and_recipes.py::test_browse_recipes_accepts_dessert_category tests/api/test_catalog_and_recipes.py::test_browse_recipes_filters_exact_category_before_pagination tests/api/test_catalog_and_recipes.py::test_browse_recipes_rejects_empty_category tests/api/test_catalog_and_recipes.py::test_browse_recipes_treats_encoded_space_as_literal_category`
- Pytest collected five tests and reached feature assertions: **1 passed, 4 failed, 0 errors, 1 warning** in 9.35s.
- Passed: `test_browse_recipes_without_category_keeps_categorized_and_uncategorized_items`; the unfiltered collection retained both records.
- Failed: `test_browse_recipes_accepts_dessert_category`; the response included the existing recipes (`recipe-1` through `recipe-5`) as well as the newly created Dessert recipe instead of the exact one-ID list. This confirms the `category` query parameter is ignored and filtering is absent.
- Failed: `test_browse_recipes_filters_exact_category_before_pagination`; the response contained the unfiltered collection rather than the three exact-category recipe IDs. The test stopped at this assertion, so its subsequent page-slicing and no-match assertions were not reached.
- Failed: `test_browse_recipes_rejects_empty_category`; `?category=` returned HTTP 200 instead of the required validation error (HTTP 422), confirming empty-value validation is absent.
- Failed: `test_browse_recipes_treats_encoded_space_as_literal_category`; the response included `recipe-1` despite requesting the literal-space category. This confirms the filter is absent; this test run does not independently evaluate trimming behavior because the implementation does not filter at all.
- Warning: the existing AnyIO plugin emitted `PytestRemovedIn10Warning` for `CallSpec2`.
- **RED assessment:** The expected RED is confirmed for absent category filtering and empty-category validation. Pagination-after-filtering assertions remain unverified in this run because the combined test stopped at its earlier result assertion. No implementation change or test fix was made; do not proceed to GREEN without separate authorization.

## 14. Category-filter GREEN (2026-11-11)

- Implemented the optional `category` query parameter in `GET /api/recipes` with a non-empty constraint. When supplied, recipes are filtered by exact, case-sensitive `metadata.category` equality before the existing pagination slice; recipe order is retained. Category values are not trimmed. When omitted, the existing collection list and slice are used unchanged.
- Updated `docs/openapi.yaml` with the optional `category` query parameter (`minLength: 1`), exact-match and filter-before-pagination semantics, literal whitespace behavior, and a 422 validation response. No historical Lab 4 decision, baseline requirement, or pagination addendum was changed.
- The first five-test run against `127.0.0.1:8000` after the source edit returned 1 passed and 4 failed. Inspection of `GET /openapi.json` on that server showed only `page` and `pageSize`, confirming it was serving a stale app process that had not loaded the changed source. The process on port 8000 was left untouched.
- Started a separate local Uvicorn process on port 8001 from the current source and ran only the five category-filter tests with `API_BASE_URL` set to that app.
- Command: `$env:API_BASE_URL='http://127.0.0.1:8001/api'; pytest -p no:cacheprovider tests/api/test_catalog_and_recipes.py::test_browse_recipes_without_category_keeps_categorized_and_uncategorized_items tests/api/test_catalog_and_recipes.py::test_browse_recipes_accepts_dessert_category tests/api/test_catalog_and_recipes.py::test_browse_recipes_filters_exact_category_before_pagination tests/api/test_catalog_and_recipes.py::test_browse_recipes_rejects_empty_category tests/api/test_catalog_and_recipes.py::test_browse_recipes_treats_encoded_space_as_literal_category`
- Result: **5 passed, 1 warning** in 6.22s. The warning is the existing AnyIO `PytestRemovedIn10Warning` for `CallSpec2`.
- Parsed `docs/openapi.yaml` and checked the category parameter, non-empty constraint, 422 ValidationError reference, exact/case-sensitive and whitespace description, filter-before-pagination wording, and runtime FastAPI parameter schema; the contract check passed.
- **RED → GREEN:** The prior RED run against the unchanged implementation had 1 pass and 4 assertion failures for unfiltered category results, missing empty-value validation, and encoded-space category filtering. Against the current implementation, all five selected category-filter tests pass. The full regression suite was not run; no refactoring was performed.

## 15. Full regression after category-filter GREEN (2026-11-11)

- Restarted Uvicorn on `127.0.0.1:8001` from the current source, giving the full suite a fresh in-memory application state. The stale server on port 8000 was not used.
- Confirmed `tests/api/conftest.py` reads `API_BASE_URL` (not `API_BASE`) and set it to `http://127.0.0.1:8001/api` for pytest.
- Command: `$env:API_BASE_URL='http://127.0.0.1:8001/api'; pytest -p no:cacheprovider`
- Pytest collected 46 tests across authentication, catalog/recipe, photo, and search API tests. Result: **46 passed, 0 failed, 0 errors, 1 warning** in 55.92s.
- Warning: the existing AnyIO plugin emitted `PytestRemovedIn10Warning` for `CallSpec2`.
- Regression conclusion: no regressions were observed in the full suite, including the new category-filter tests. `git diff --check` passed. No code, test, OpenAPI, or specification changes were made during this regression-verification step; only this log entry was added.

## 16. Category-filter REFACTOR review (2026-11-11)

- Reviewed `list_recipes` and nearby handler style. The category predicate is a short, readable list comprehension directly before the existing pagination slice. Extracting it into a private helper would add indirection without improving reuse or clarity, so no source refactor was made. The GREEN implementation and behavior remain unchanged.
- Focused command: `$env:API_BASE_URL='http://127.0.0.1:8001/api'; pytest -p no:cacheprovider tests/api/test_catalog_and_recipes.py::test_browse_recipes_without_category_keeps_categorized_and_uncategorized_items tests/api/test_catalog_and_recipes.py::test_browse_recipes_accepts_dessert_category tests/api/test_catalog_and_recipes.py::test_browse_recipes_filters_exact_category_before_pagination tests/api/test_catalog_and_recipes.py::test_browse_recipes_rejects_empty_category tests/api/test_catalog_and_recipes.py::test_browse_recipes_treats_encoded_space_as_literal_category`
- Focused result: **5 passed, 1 warning** in 12.72s.
- Restarted Uvicorn on port 8001 before the full regression run so it used current code and a fresh in-memory state. Full command: `$env:API_BASE_URL='http://127.0.0.1:8001/api'; pytest -p no:cacheprovider`
- Full regression result: **46 passed, 0 failed, 0 errors, 1 warning** in 102.20s.
- Both runs emitted the existing AnyIO `PytestRemovedIn10Warning` for `CallSpec2`. `git diff --check` passed.
- REFACTOR conclusion: the implementation remains as written after review; no code, tests, OpenAPI, or specification files were changed in this stage. Only this log entry was added.

## 17. Documentary alignment and final checkpoint status (2026-11-11)

- Updated `spec/traceability.md` to mark `ADD-F-004` / `ADD-F-005` and `ADD-AC-005` through `ADD-AC-009` implemented and verified, identify the specific API tests and recorded outcomes, and map the category BDD scenario only to `ADD-AC-006`, which it directly demonstrates.
- Updated `spec/addendum-recipe-category-filter.md` to state the actual implementation and OpenAPI status, retain all approved requirement wording, and correct its BDD traceability. Added the Lab 4 chronology clarification in `docs/lab4-api-design.md` without changing the historical decision.
- Documentary status: **complete** for these audit findings. The recorded category-focused runs passed 5 tests; the recorded full regression runs passed 46 tests with 0 failures and 0 errors. Each final run reported one existing AnyIO deprecation warning; it was not a test failure. The pagination TDD deviation remains explicitly documented: pagination behavior predated RED, and no RED is claimed.
- **Status at the time of this entry:** Human validation and the final Lab 5 checkpoint were still outstanding. No human validation was claimed in this documentary update. No commit hash or clean-working-tree status is asserted here.

## 18. HUMAN VALIDATION — manual API verification (2026-11-11)

- `GET /openapi.json`: **200**. Confirmed the `GET /api/recipes` operation documents `page`, `pageSize`, and `category` query parameters.
- Registration: the first request displayed a PowerShell security warning. The retry returned `User already exists`; no HTTP 201 registration response is claimed. The subsequent successful login confirms that the account exists.
- Login: **200**.
- Recipe setup: all four recipe creation requests returned **201**.
- Category filter: **200**. The category query returned the two expected recipes. Verified that filtering is applied before pagination, matching is case-sensitive, a nonexistent category returns an empty list, and an empty category parameter returns **422**.
- Recipe details: **200**. Recipe update: **200**; verified the updated name, ingredient quantity, and preparation step. Recipe deletion: **204**; a subsequent GET returned **404**.
- Recipe photo: PUT returned **200** and the photo metadata appeared in recipe details; DELETE returned **204** and `recipePhoto` was empty afterward.
- Cooked-dish photo: POST returned **201**; duplicate POST returned **409**; PUT `/me` returned **200**; DELETE `/me` returned **204**. `cookedDishPhotos` was empty afterward.
- Ingredient search: **200**. `recipe-1` returned `Can cook now`. `recipe-2` returned `Almost can cook`, with `tomato` (`ingredient-3`) listed in the missing ingredients.
- Photo verification covered API metadata and returned URLs only. Actual image-file storage and serving were not verified.
- No tests were run as part of this manual validation log update.
- **Status update:** Human API validation is complete. The final Lab 5 checkpoint and overall final decision remain outstanding. No commit hash or clean-working-tree status is asserted.

## 19. Photo byte storage and retrieval (2026-11-12)

- Added local filesystem storage for uploaded photos through `src/photo_storage.py`, configurable with `PHOTO_STORAGE_DIR` and defaulting to the ignored `photo_uploads/` directory. Added a public `GET /api/photos/{photoId}` route and absolute URLs in photo metadata. Existing upload authentication, ownership, contributor, and duplicate-photo checks remain in place.
- Uploads are staged to a temporary file, rejected with HTTP 422 if empty or Pillow cannot verify them, then published with `os.replace`. Metadata changes only after the new bytes are stored, preserving an existing valid photo after rejected replacements. No custom format allowlist, MIME-type check, or file-size limit was added. Pillow supplies the response media type.
- Updated OpenAPI for image retrieval and invalid-upload responses. The OpenAPI validator passed. `git diff --check` passed.
- The first focused-test command ran from an incorrect working directory and collected no tests because the requested test path was unavailable there. Reran from the repository against a fresh Uvicorn process on port 8002. Command: `$env:API_BASE_URL='http://127.0.0.1:8002/api'; pytest -p no:cacheprovider tests/api/test_photos.py`. Result: **3 passed, 1 AnyIO deprecation warning** in 7.76s.
- The earlier full regression result was **46 passed**. The later run below was **43 passed** after consolidating six photo tests into three; the difference is the three fewer test functions, not a regression failure.
- Restarted Uvicorn on port 8002 for a clean in-memory state and ran `$env:API_BASE_URL='http://127.0.0.1:8002/api'; pytest -p no:cacheprovider`. Result: **43 passed, 0 failed, 0 errors, 1 AnyIO deprecation warning** in 85.61s. The photo tests were consolidated from six tests into three lifecycle tests; they retain upload, duplicate, replacement, deletion, and permission assertions while adding byte retrieval and invalid-upload coverage.
- No pre-implementation RED run was performed for this photo work; no RED is claimed. The prior HUMAN VALIDATION entry checked photo metadata and URLs only; actual image-byte retrieval is verified by the new API tests, not by a new manual validation run.
- Removal confirmation and cancellation for recipe and cooked-dish photos (REQ-F-040 / AC-024 and REQ-F-045 / AC-027) are client-side responsibilities outside this API-only implementation scope. The API exposes the removal operations; no UI confirmation or cancellation behavior is claimed as implemented or tested.

## 20. Final photo audit follow-up (2026-11-12)

- Pillow's standard image MIME mapping is used when available. Accepted Pillow formats without an image MIME entry now receive a format-specific `image/x-pillow-<format>` media type rather than `application/octet-stream`; no format allowlist, MIME restriction, or file-size limit was introduced.
- Added API coverage for BMP and PPM retrieval media types, a recipe-search result's retrievable photo URL and bytes, recipe deletion removing both recipe-photo and cooked-dish photo files, and exact cooked-photo contributor usernames.
- The first focused run failed during collection because the test imported `src.photo_storage`, which is not importable under this API test path setup. The test was adjusted to locate the configured storage directory without importing application code. Corrected command: `$env:API_BASE_URL='http://127.0.0.1:8003/api'; pytest -p no:cacheprovider tests/api/test_photos.py`. Result: **7 passed, 0 failed, 0 errors, 1 AnyIO deprecation warning** in 11.54s.
- A first full-suite invocation used an incorrectly typed working-directory path and collected zero tests. The corrected command against a freshly restarted Uvicorn app was `$env:API_BASE_URL='http://127.0.0.1:8003/api'; pytest -p no:cacheprovider`. Result: **47 passed, 0 failed, 0 errors, 1 AnyIO deprecation warning** in 55.79s.
- Validation: `python -m openapi_spec_validator docs/openapi.yaml` reported `docs/openapi.yaml: OK`; `git diff --check` and the staged diff check passed. Git displayed only LF-to-CRLF working-copy notices.

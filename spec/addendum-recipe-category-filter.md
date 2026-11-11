# Specification Addendum: Recipe Collection Category Filter

## Review status

**Status: SPEC-ADDENDUM-GATE GO, approved by the Student (2026-11-11); implementation and contract update completed.** The focused and full test outcomes and the REFACTOR review are recorded in `logs/lab5.md`.

## Purpose and scope

This addendum specifies the optional category filter implemented for `GET /api/recipes`. It supplements `REQ-F-017` / `AC-008` for optional recipe category metadata and `REQ-F-035` / `AC-021` for shared collection browsing. It does not modify the baseline SRS or the separately approved pagination addendum.

When both a category and pagination parameters are supplied, category filtering is applied first; the existing page and page-size behavior is then applied to the filtered collection. The response keeps its existing `{ "items": [...] }` envelope and collection order. A recipe without category metadata is not included when a category filter is supplied. Category comparison is exact and case-sensitive. `?category=` is invalid and returns a validation error. `?category=Dessert` is valid. `?category=%20` is also valid: after URL decoding, the single space is treated as a literal category value. The system does not trim or normalize whitespace in the query value.

The filter is for browsing recipe metadata only. It does not affect ingredient matching, recipe storage, or the fixed ingredient catalog.

## Additional requirements

| ID | Requirement |
|---|---|
| ADD-F-004 | `GET /api/recipes` shall accept an optional, non-empty `category` query parameter. When supplied, the result shall include only recipes whose `metadata.category` exactly and case-sensitively equals that value. Recipes without category metadata shall be excluded. |
| ADD-F-005 | When `category` is supplied, the system shall preserve the relative order of matching recipes and apply the existing `page` and `pageSize` pagination to that filtered collection. When `category` is omitted, collection behavior shall remain unchanged. |

## Additional acceptance criteria

| ID | Acceptance criterion |
|---|---|
| ADD-AC-005 | Given the category parameter is omitted, when the shared collection is requested, then the existing unfiltered pagination behavior and response structure are preserved. |
| ADD-AC-006 | Given recipes with matching, different, and absent categories, when a category is supplied, then only exact, case-sensitive matches are returned, in their existing relative collection order. |
| ADD-AC-007 | Given more matching recipes than fit on one page, when category and pagination parameters are supplied, then pagination selects the requested page from the ordered, filtered results. |
| ADD-AC-008 | Given no recipe has the requested category, when the collection is requested, then the system returns HTTP 200 with `items: []`. |
| ADD-AC-009 | Given an empty `category` query value, when the collection is requested, then the system returns a validation error and does not treat the empty value as an omitted filter. |

Boundary clarification: `?category=Dessert` is a valid non-empty value. `?category=%20` is valid and is matched literally as one space; it is not trimmed or normalized. Only an empty value such as `?category=` is rejected.

## BDD scenario

### Scenario: Browse recipes in a selected category

Given the shared collection contains recipes categorized as Dessert and Soup, as well as a recipe with no category\
When a Visitor requests `GET /api/recipes?category=Dessert`\
Then only recipes whose category exactly equals Dessert are returned\
And Soup recipes are excluded from the response\
And recipes without category metadata are excluded from the response\
And those recipes remain in their existing collection order\
And the existing pagination is applied to the filtered results\
And the response contains the existing `items` field without additional pagination metadata

**Traceability:** This scenario demonstrates `REQ-F-017`, `REQ-F-035`, and `ADD-F-004` through exact category matching and exclusion of other and uncategorized recipes. Its directly demonstrated addendum acceptance criterion is `ADD-AC-006`. It does not demonstrate omitted-category behavior, a no-match response, empty-value validation, or a filtered pagination boundary (`ADD-AC-005`, `ADD-AC-007` through `ADD-AC-009`).

## Proposed ticket (local draft; not created in an external tracker)

**Ticket key:** `LAB5-FEATURE-CATEGORY-FILTER`\
**Title:** Filter the shared recipe collection by category

**Description:** As a Visitor or Registered User browsing the shared recipe collection, I want to request recipes in a selected category so that I can narrow the collection while retaining its established order and pagination behavior.

**Acceptance scope and result:** `ADD-F-004` and `ADD-F-005` are implemented for `GET /api/recipes`; `ADD-AC-005` through `ADD-AC-009` are covered by the API tests listed in `spec/traceability.md` and recorded in `logs/lab5.md`. Category storage, recipe matching, the ingredient catalog, and unrelated routes were not changed for this feature.

**Dependencies:** Student approval of this addendum and SPEC-ADDENDUM-GATE. No dependency on changing or replaying the pagination work.

**Definition of done and result:** The category-filter tests produced a functional RED against the prior implementation and passed after the implementation change and REFACTOR review. The full regression suite and OpenAPI contract checks passed, and actual results are recorded in traceability and `logs/lab5.md`. See the log for the pagination TDD deviation; no RED is claimed for pagination, whose behavior predated that addendum.

## Impact analysis

- **Existing requirements:** Uses existing optional `metadata.category` (`REQ-F-017` / `AC-008`) and shared collection browsing (`REQ-F-035` / `AC-021`). It introduces no additional user role or change to the meaning of recipe metadata.
- **Existing API:** Extends `GET /api/recipes`, which already accepts pagination. `docs/openapi.yaml` now declares the optional `category` query parameter, its non-empty constraint, exact-match and filter-before-pagination behavior, and the 422 validation response. The recipe and collection response schemas require no new fields.
- **Implementation surface:** The change is implemented in `src/main.py`, covered in `tests/api/test_catalog_and_recipes.py`, and reflected in OpenAPI and traceability. No schema or persistence change was needed; existing recipe metadata stores category values.
- **Behavioral interaction:** Filtering before slicing means page boundaries are calculated over matching recipes. Omitting the category preserves the current pagination behavior. No special ranking is added.
- **Scope exclusions:** No ingredient normalization, synonyms, ingredient matching changes, manual ingredient entry, social features, or pagination metadata are introduced.
- **Test design:** Positive cases cover exact category matches and preservation of relative order. Negative cases cover different categories, uncategorized recipes, and a category with no matches. Boundary cases cover omitted category, empty category validation, and category combined with page boundaries.
- **Risk:** Low. The change is an optional predicate on one existing collection route. The main behavioral risk is applying pagination before filtering; `ADD-AC-007` explicitly prevents that ordering mistake. Exact case-sensitive comparison avoids introducing implicit category normalization.
- **Documentation status:** `docs/lab4-api-design.md` retains the original Lab 4 decision and now records that pagination was subsequently approved in a separate addendum with GO.

## SPEC-ADDENDUM-GATE decision

**Decision: GO — approved by the Student (2026-11-11).**

The Student approved the category-filter addendum in principle and requested explicit handling of empty and whitespace query values and explicit exclusion of Soup and uncategorized recipes in the BDD scenario. Those clarifications are included above. The feature is consistent with the SRS's existing optional recipe category and collection-browsing capabilities. It adds a narrowly scoped browse filter, leaves the default collection behavior intact, preserves order and the approved pagination contract, and does not cross the documented ingredient-matching or social-feature exclusions. The acceptance criteria define the interaction with pagination and exact-match behavior sufficiently for focused API tests and OpenAPI verification. The implementation surface is small enough for a controlled TDD cycle.

This GO approved the specification before implementation. The category filter has since been implemented and verified; its actual RED/GREEN results and REFACTOR review are recorded in `logs/lab5.md`. The earlier pagination gate and its documented TDD deviation remain approved and unchanged.

# Lab 4 API Design

This document describes the proposed REST contract in `docs/openapi.yaml`. It is an API-first design artifact, not server implementation.

## Resource and Operation Table

| Resource | Method and URI | Purpose | Requirements |
|---|---|---|---|
| Authentication | `POST /api/auth/register` | Register with unique username/email/password | REQ-F-004 |
| Authentication | `POST /api/auth/login` | Login with email/password | REQ-F-005, REQ-F-006 |
| Authentication | `POST /api/auth/logout` | End authenticated session | REQ-F-005 |
| Ingredient catalog | `GET /api/ingredients` | Read fixed catalog | REQ-F-023, REQ-F-024, REQ-F-027 |
| Ingredient catalog | `GET /api/ingredients/{ingredientId}` | Read one catalog ingredient | REQ-F-023, REQ-F-024 |
| Recipes | `GET /api/recipes` | Browse shared collection | REQ-F-002, REQ-F-035 |
| Recipes | `POST /api/recipes` | Create valid recipe | REQ-F-003, REQ-F-010--REQ-F-017 |
| Recipes | `GET /api/recipes/{recipeId}` | View recipe details | REQ-F-002, REQ-F-026, REQ-F-037 |
| Recipes | `PUT /api/recipes/{recipeId}` | Update own recipe | REQ-F-003, REQ-F-018, REQ-F-019 |
| Recipes | `DELETE /api/recipes/{recipeId}` | Delete own recipe | REQ-F-003, REQ-F-021, REQ-F-022 |
| Search | `POST /api/recipes/search` | Match recipes by catalog ingredient IDs | REQ-F-027--REQ-F-034 |
| Recipe photo | `PUT /api/recipes/{recipeId}/photo` | Add or replace creator's recipe photo | REQ-F-039, REQ-F-041 |
| Recipe photo | `DELETE /api/recipes/{recipeId}/photo` | Remove creator's recipe photo | REQ-F-040, REQ-F-041 |
| Cooked-dish photos | `POST /api/recipes/{recipeId}/cooked-dish-photos` | Add one contributor photo | REQ-F-042, REQ-F-043, REQ-F-041 |
| Cooked-dish photos | `PUT /api/recipes/{recipeId}/cooked-dish-photos/me` | Replace own contributor photo | REQ-F-044, REQ-F-041 |
| Cooked-dish photos | `DELETE /api/recipes/{recipeId}/cooked-dish-photos/me` | Remove own contributor photo | REQ-F-044, REQ-F-045 |

Ingredient entries and preparation steps are nested inside recipe request and response schemas. No separate endpoints are proposed for them.

## Requirement Mapping

| Requirement group | API operation(s) |
|---|---|
| REQ-F-001--REQ-F-003 | Authentication, recipe mutations, photo mutations, and authorization on protected operations |
| REQ-F-004--REQ-F-008 | Authentication operations; REQ-F-007 and REQ-F-008 also include client-side prompt/return behavior |
| REQ-F-009 | No API operation; excluded functionality |
| REQ-F-010--REQ-F-022 | Recipe create, update, details, and delete operations |
| REQ-F-023--REQ-F-026 | Catalog reads, recipe schemas, recipe details, and search |
| REQ-F-027--REQ-F-034 | `POST /api/recipes/search` |
| REQ-F-035--REQ-F-038 | Collection, recipe details, and search-result operations; REQ-F-038 is an exclusion |
| REQ-F-039--REQ-F-041 | Recipe-photo operations and upload error responses |
| REQ-F-042--REQ-F-045 | Cooked-dish-photo operations; confirmations remain client-side |

The detailed operation descriptions in `openapi.yaml` contain the exact REQ-F IDs.

## Key Design Decisions

- The contract uses `/api` as a proposed base path.
- `POST /api/recipes/search` is used for a structured set of selected ingredient IDs; this is a design choice, not an SRS requirement.
- Authentication uses a proposed HTTP bearer security scheme. The SRS does not define token or session format.
- Photo uploads use proposed `multipart/form-data` bodies with a binary `photo` part.
- Recipe ingredient entries and preparation steps remain nested recipe data.
- Delete confirmations are client-side. No confirmation endpoint is added.
- Error responses use `{code, message, details}` consistently.
- Recipe and search matching use standardized catalog identities only. Manual ingredient entry, singular/plural normalization, synonym matching, quantity-based matching, and social features are not added.
- Pagination query parameters are optional design choices for collection browsing; pagination is not an approved product requirement.

## Unresolved Assumptions

- Exact authentication session/token behavior is not specified by the SRS.
- Exact HTTP error-code vocabulary and validation-detail conventions are API design choices.
- Exact media handling and returned photo metadata are not specified by the SRS.
- The SRS requires a consistent collection order but does not define the ordering algorithm.
- Client state preservation after authentication and confirmation dialogs are client-side behaviors, not separate API operations.
- The API contract is not an approval of implementation technology or server architecture.

## Lab 4 Contract Validation

### Tooling check

- At inspection time, C: had 2.52 GB free and the repository drive had 156.68 GB free. The earlier zero-free-space observation was no longer current.
- Node v24.11.0 and npm 11.10.1 were available. Python had no installed YAML/OpenAPI validator. Docker was installed, but its daemon was unavailable.
- Prism was not globally installed. It was run with `npm exec` using a cache under the system temp directory; no project dependency or lockfile was added.
- Prism loaded `docs/openapi.yaml`, listed all 16 operations, and started successfully. Its route output used root paths such as `/recipes` even though the document declares `servers.url: /api`; the Prism mock did not mount that server URL path component. A temporary local forwarding proxy mapped the planned `/api/...` requests to Prism's root operation routes during the scenarios below. This verifies the operation paths behind that adapter, not direct `/api` routing by Prism or a production deployment.

### Static contract checks

The previously recorded structural and editor checks reported:

- OpenAPI version: `3.0.3`
- Paths: 11; HTTP operations: 16; `$ref` occurrences: 95
- Security schemes and `multipart/form-data` photo uploads: present
- Nullable optional recipe-photo fields: 2
- Editor diagnostics: no errors

The prior structural/editor observations above are not an automatic OpenAPI validation result. No dedicated OpenAPI validator command, version, or successful validation output is evidenced in these artifacts. Prism loading the document without a parser error establishes that it could start a mock from it; that alone does not establish a complete OpenAPI conformance check. Prism did validate the individual requests in the HTTP scenarios below.

### Mock-server scenarios

The six planned HTTP scenarios were sent to the temporary local `/api` prefix adapter backed by Prism. These are contract-mock results, not application/backend tests; successful responses contain Prism-generated sample data.

| Scenario | Actual result | Observation |
|---|---:|---|
| `GET /api/recipes` | 200 | Request passed Prism validation; sample collection returned. |
| `GET /api/recipes/recipe-1` | 200 | Request passed Prism validation; sample recipe returned. |
| `POST /api/recipes/search` with `{"ingredientIds":["ingredient-1"]}` | 200 | Request passed Prism validation; generated sample search response returned. |
| `POST /api/recipes/search` with `{"ingredientIds":[]}` | 422 | Prism reported the `minItems` violation for `ingredientIds`. |
| Unauthenticated `POST /api/recipes` with a structurally valid recipe body | 401 | Prism reported the missing/invalid bearer security scheme. |
| `PUT /api/recipes/recipe-1/photo` with multipart `photo` and `Authorization: Bearer mock-token` | 200 | Multipart request passed Prism validation and a sample photo response returned. The mock token does not test real authentication. |

Prism validates request shape and selects declared mock responses. It does not implement recipe persistence, search matching, ownership rules, or real authentication, so those behaviors remain unverified against an application server.

### API-GATE decision

**REVISE**

Reasons and required corrections:

- **Automatic OpenAPI validation is not evidenced.** Run a dedicated OpenAPI validator and record its name/version, command, and result. Do not use Prism mock startup as a substitute.
- **The `/api` prefix is not directly served by the Prism mock.** Prism mounted the operations at root paths, so the scenarios used a temporary prefix adapter. Configure or verify the intended deployment routing for `/api`, then exercise the routes through that routing without the adapter.
- **The detailed API-GATE rubric is not included in the inspected artifacts.** Record the rubric criteria and their evidence in this API design document before making a GO decision.

The existing mock responses do not test backend persistence, real authentication, ownership enforcement, or search matching. No backend behavior is claimed as tested.

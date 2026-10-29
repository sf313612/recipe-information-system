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
- Authentication uses the selected Bearer access-token design described below; this is an API-design refinement, not an SRS requirement.
- Photo uploads use proposed `multipart/form-data` bodies with a binary `photo` part.
- Recipe ingredient entries and preparation steps remain nested recipe data.
- Delete confirmations are client-side. No confirmation endpoint is added.
- Error responses use `{code, message, details}` consistently.
- Recipe and search matching use standardized catalog identities only. Manual ingredient entry, singular/plural normalization, synonym matching, quantity-based matching, and social features are not added.
- Pagination query parameters are optional design choices for collection browsing; pagination is not an approved product requirement.

### Unresolved Assumptions

- Exact HTTP error-code vocabulary and validation-detail conventions are API design choices.
- Exact media handling and returned photo metadata are not specified by the SRS.
- The SRS requires a consistent collection order but does not define the ordering algorithm.
- Client state preservation after authentication and confirmation dialogs are client-side behaviors, not separate API operations.
- The API contract is not an approval of implementation technology or server architecture.

### Authentication Decision (Lab 4 API Design Refinement)

The SRS requires login and logout (`REQ-F-005`) and authenticated access to Registered User actions (`REQ-F-001--REQ-F-003`), but does not prescribe Bearer tokens, cookies, or another transport mechanism. For this API contract, Bearer access tokens are the selected design decision; this clarifies the API without adding or changing a REQ-ID.

A successful `POST /api/auth/login` returns the user and a non-empty `accessToken`. The client sends that value on protected operations as `Authorization: Bearer <accessToken>`. `POST /api/auth/logout` retains its existing method, `204` response, and no response body; its design semantics are to end the current authenticated session and invalidate the token used for that request.

The Prism mock can check the declared response shape and Bearer security requirement, but it does not implement stateful login, token storage, or token invalidation. A mock `204` for logout therefore does not prove that a real token was invalidated; that behavior requires backend verification in Lab 5.

## Lab 4 Contract Validation

### Tooling check

- At inspection time, C: had 2.52 GB free and the repository drive had 156.68 GB free. The earlier zero-free-space observation was no longer current.
- Node v24.11.0 and npm 11.10.1 were available. Python's `openapi_spec_validator` module is available. Docker was installed, but its daemon was unavailable.
- Prism was not globally installed. It was run from the existing temp npm cache; no project dependency or lockfile was added. The cached CLI version is `5.14.2`.
- `prism mock --help` lists host, port, CORS, process, error, logging, and example-generation options; it has no base-path or path-prefix option. Prism loaded `docs/openapi.yaml` and listed the operations at root paths such as `/recipes`, despite `servers.url: /api`. The official [Prism FAQ](https://github.com/stoplightio/prism#why-am-i-getting-404-errors-when-i-include-my-basepath) explains that Prism does not prepend the OpenAPI server URL path to mounted operation paths. The earlier six `/api/...` scenarios therefore used a temporary local forwarding proxy to map the contract prefix to Prism's root routes; they were not direct requests to Prism at the contract URIs.

### Static contract checks

The previously recorded structural and editor checks reported:

- OpenAPI version: `3.0.3`
- Paths: 11; HTTP operations: 16; `$ref` occurrences: 95
- Security schemes and `multipart/form-data` photo uploads: present
- Nullable optional recipe-photo fields: 2
- Editor diagnostics: no errors

The structural/editor observations above are separate from the automatic validation result. The dedicated OpenAPI validation command completed successfully:

```text
python -m openapi_spec_validator docs/openapi.yaml
docs/openapi.yaml: OK
exit code: 0
```

Prism loading the document is not used as proof of this validation. Prism did separately validate the individual requests in the HTTP scenarios below.

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

### Direct Prism URI verification

The cached CLI was inspected and run without installing packages:

```powershell
$root = Join-Path (Join-Path $env:TEMP 'lab4-npm-cache') '_npx\bafec163626a88fa\node_modules'
$cli = Join-Path $root '@stoplight\prism-cli\dist\index.js'
node $cli --version
node $cli mock --help
node $cli mock docs/openapi.yaml --host 127.0.0.1 --port 4010
```

The version command returned `5.14.2`. The help output has no option to mount routes under `/api`. With Prism listening at `http://127.0.0.1:4010`, these direct contract-URI requests returned:

| Direct request to Prism | Status | Actual result |
|---|---:|---|
| `GET http://127.0.0.1:4010/api/recipes` | 404 | `NO_PATH_MATCHED_ERROR`; no response body. |
| `GET http://127.0.0.1:4010/api/recipes/recipe-1` | 404 | `NO_PATH_MATCHED_ERROR`; no response body. |
| `POST http://127.0.0.1:4010/api/recipes/search` with `{"ingredientIds":[]}` | 404 | `NO_PATH_MATCHED_ERROR`; Prism did not reach request-schema validation. |
| Unauthenticated `POST http://127.0.0.1:4010/api/recipes` with a structurally valid recipe body | 404 | `NO_PATH_MATCHED_ERROR`; Prism did not reach security validation. |

The least disruptive solution is to keep `servers.url: /api` and the existing operation paths unchanged, and use a prefix-aware local reverse proxy or deployment gateway to forward `/api/*` to Prism's root-mounted routes. Prism 5.14.2 cannot serve those prefixed routes directly. Do not treat a direct Prism request returning 404 as a contract validation result.

### Contract URI scenarios through a temporary prefix-aware proxy

In a separate run, Prism 5.14.2 listened on `127.0.0.1:4010` and a temporary Node.js core `http` proxy listened on `127.0.0.1:4011`. The proxy was used only to check the contract's `/api/...` URIs: it removed `/api` before forwarding each request to Prism's matching root route. It forwarded the HTTP method, request headers (setting `Host` to the Prism upstream), and request stream; it returned Prism's status, response headers, and response stream to the caller. This did not test an application gateway or backend.

| Request through `http://127.0.0.1:4011/api` | Expected | Actual | Prism result |
|---|---:|---:|---|
| `GET /recipes` | 200 | 200 | Mock collection returned. |
| `GET /recipes/recipe-1` | 200 | 200 | Mock recipe returned. |
| `POST /recipes/search` with `{"ingredientIds":[]}` | 422 | 422 | `minItems` violation for `ingredientIds` was returned in `sl-violations`. |
| Unauthenticated `POST /recipes` with a structurally valid recipe body | 401 | 401 | Missing/invalid bearer scheme was returned in `sl-violations`. |

The proxy logs showed request bytes equal to `Content-Length` for both POSTs (20/20 and 169/169 bytes), and response bytes equal to `Content-Length` for all four responses (168/168, 508/508, 86/86, and 86/86 bytes). The client received the JSON content type and Prism's `sl-violations` headers. These results validate the contract URIs through this temporary path-prefix mapping only; they do not establish production routing or backend behavior.

### Bearer login and logout mock checks

After selecting Bearer access tokens as an API-design refinement, Prism 5.14.2 was started from `docs/openapi.yaml` on `127.0.0.1:4010`; the temporary prefix-aware Node.js core `http` proxy forwarded `/api/*` from `127.0.0.1:4011`. No packages were installed. The following requests used the login response's example token, `mock-access-token`:

| Request through proxy | Actual status | Result and limitation |
|---|---:|---|
| `POST /api/auth/login` with a structurally valid `LoginRequest` | 200 | Response included `user.username` and non-empty `accessToken: "mock-access-token"` from the OpenAPI example. Credentials were not authenticated by Prism. |
| `POST /api/recipes` with a valid recipe body and no `Authorization` | 401 | Protected operation rejected the request without Bearer credentials. |
| `POST /api/recipes` with `Authorization: Bearer mock-access-token` and the same body | 201 | Prism accepted the Bearer header and returned a mock recipe. This tests header/security-scheme conformance only. |
| `POST /api/auth/logout` without `Authorization` | 401 | Protected logout rejected the request without Bearer credentials. |
| `POST /api/auth/logout` with `Authorization: Bearer mock-access-token` | 204 | Declared no-content success response returned. |
| Repeated the protected recipe POST with the same token after the mock logout | 201 | Prism still accepted the token. Its mock has no session state or revocation behavior, so token invalidation was not verified. |

The login response example and security checks confirm the contract's token shape and Bearer-header requirement. They do not prove real token issuance, persistence, authentication, or invalidation. Logout invalidation remains an implementation behavior for Lab 5 verification.

### API-GATE decision

**GO — Lab 4 API contract design**

The contract has an explicit Bearer access-token decision, the login response schema requires a non-empty `accessToken`, protected and public operations use the security scheme consistently, the automatic OpenAPI validator passes, and the recorded mock checks cover success and unauthorized requests through the contract-URI proxy. API operation groups remain linked to their existing `REQ-F` IDs in `spec/traceability.md`; no requirement IDs were added or changed.

This GO is limited to the API design contract and mock conformance. The documented positive and negative mock scenarios returned their recorded expected results; the post-logout `201` when reusing the same token is a probe showing that Prism cannot verify invalidation, not a successful invalidation check. Prism itself mounts routes without `/api`, so the full contract URIs were exercised through the documented temporary prefix-aware proxy; production gateway routing was not tested. Real authentication, token invalidation, persistence, ownership enforcement, and search matching remain Lab 5 verification. These limitations do not require backend implementation in Lab 4 or block completion of its API contract.

# Initial BDD Specification

## Feature: Ingredient-Based Search

### Scenario: Find a recipe that can be prepared now

Given the user selects chicken and pasta
And a recipe requires chicken and pasta as Essential ingredients
When the user performs an ingredient-based search
Then the recipe is classified as "Can cook now"
And the recipe appears in the search results

# Traceability: REQ-F-027, REQ-F-029, REQ-F-030; AC-016, AC-017

### Scenario: Find a recipe that is almost possible to prepare

Given the user selects chicken
And a recipe requires chicken, pasta, and cream as Essential ingredients
When the user performs an ingredient-based search
Then the recipe is classified as "Almost can cook"
And pasta and cream are shown as missing Essential ingredients

# Traceability: REQ-F-027, REQ-F-030, REQ-F-036; AC-016, AC-017, AC-022

### Scenario: Exclude recipes missing three or more Essential ingredients

Given the user selects chicken
And a recipe requires chicken, pasta, cream, and tomatoes as Essential ingredients
When the user performs an ingredient-based search
Then the recipe is not included in the search results

# Traceability: REQ-F-030; AC-017

### Scenario: Ignore Basic and Optional ingredients during matching

Given the user selects chicken and pasta
And a recipe requires chicken and pasta as Essential ingredients
And the recipe also contains salt as Basic and cheese as Optional
When the user performs an ingredient-based search
Then the recipe is classified as "Can cook now"
And salt and cheese do not count as missing Essential ingredients

# Traceability: REQ-F-031; AC-018

## Feature: Authentication

### Scenario: Register and log in as a Registered User

Given a Visitor provides a unique username, unique email address, and password
When the Visitor registers and then logs in with the email address and password
Then the system creates the Registered User account
And the user is logged in
And the user can log out

# Traceability: REQ-F-004, REQ-F-005; AC-002, AC-003

### Scenario: Prompt a Visitor to authenticate before a restricted action

Given a Visitor is viewing a recipe
When the Visitor selects an action that requires a Registered User, such as adding a cooked-dish photo
Then the system displays a prompt explaining that authentication is required
And the prompt offers login and registration
When the Visitor successfully authenticates
Then the system returns the user to the recipe page where possible
And the restricted action is not performed automatically

# Traceability: REQ-F-007, REQ-F-008; AC-004

## Feature: Recipe Management

### Scenario: Create a valid recipe

Given a Registered User enters a non-empty recipe name
And adds a catalog ingredient with a positive quantity, predefined unit, and classification
And adds at least one non-empty preparation step
When the user saves the recipe
Then the system saves the valid recipe
And the recipe becomes immediately visible and searchable in the shared collection

# Traceability: REQ-F-010, REQ-F-011, REQ-F-015, REQ-F-020; AC-006, AC-007, AC-011

### Scenario: Reject an invalid recipe

Given a Registered User is creating a recipe
When the user attempts to save a recipe with invalid required information, such as an empty preparation step
Then the system displays validation feedback
And the invalid recipe is not saved

# Traceability: REQ-F-016; AC-007, AC-009

### Scenario: Edit and delete a user's own recipe

Given a Registered User has created a valid recipe
When the creator edits the recipe with valid changes
Then the changes are saved and become immediately visible and searchable
When the creator chooses to delete the recipe and confirms the permanent-deletion warning
Then the recipe is removed from the shared collection and search results
And its associated photos are removed from user-facing views

# Traceability: REQ-F-018, REQ-F-019, REQ-F-020, REQ-F-021, REQ-F-022; AC-010, AC-011, AC-012

## Feature: Photos

### Scenario: Manage recipe and cooked-dish photos according to permissions

Given a Registered User has created a recipe
And another Registered User is viewing that recipe
When the creator adds, replaces, or removes the optional recipe photo
Then the creator must confirm removal
And removing the recipe photo does not affect the recipe
When the other user adds a cooked-dish photo to the recipe
Then the contributor's username is displayed with the photo
And the contributor can replace their own photo without separate confirmation or remove their own photo after confirming removal
And the creator cannot modify or remove the other user's cooked-dish photo

# Traceability: REQ-F-039, REQ-F-040, REQ-F-042, REQ-F-043, REQ-F-044, REQ-F-045; AC-024, AC-026, AC-027

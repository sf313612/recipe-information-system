# Information System Glossary

This glossary defines the key terms used in the Recipe Information System and keeps their meanings consistent across the project.

| Term | Definition |
|---|---|
| **Available ingredient** | An ingredient selected by the user as currently available for an ingredient-based search. It is selected from the predefined ingredient catalog. |
| **Basic ingredient** | A recipe-specific ingredient classification for common ingredients such as salt, pepper, oil, and common spices. Basic ingredients are assumed to be available and do not count as missing during matching. |
| **Can cook now** | A search-result classification for a recipe with zero missing Essential ingredients. |
| **Cooked-dish photo** | An optional photo contributed by a registered user to show how a dish prepared from a recipe turned out. Each registered user may have at most one active cooked-dish photo per recipe. |
| **Creator** | The creator is the registered user who created the recipe and has permission to edit or delete the recipe and manage its recipe photo. |
| **Essential ingredient** | A recipe-specific ingredient classification for an ingredient necessary to prepare a recipe. Missing Essential ingredients determine the recipe's search-match classification. |
| **Ingredient catalog** | The fixed, system-controlled set of standardized ingredients available for recipes and ingredient-based searches. Users cannot add, edit, or remove catalog entries. |
| **Ingredient-based search** | The core system function that compares a user's selected available ingredients with recipe ingredients to determine what the user can cook. At least one ingredient must be selected. |
| **Ingredient classification** | The classification assigned to an ingredient within a particular recipe: Essential, Basic, or Optional. The classification belongs to the recipe use of the ingredient, not permanently to the catalog ingredient. |
| **Login** | The account action through which a registered user authenticates using an email address and password. |
| **Logout** | The account action through which a logged-in registered user ends the current authenticated session. |
| **Almost can cook** | A search-result classification for a recipe with exactly 1 or 2 missing Essential ingredients. The missing ingredients are shown in the search result. |
| **Missing Essential ingredient** | An Essential ingredient in a recipe that is not included among the user's selected available ingredients. Quantities are not considered when determining whether it is missing. |
| **Optional ingredient** | A recipe-specific ingredient classification for an ingredient that is not necessary to prepare the recipe. Optional ingredients do not prevent a recipe from being considered fully matchable. |
| **Predefined measurement unit** | One of the fixed units available for recipe ingredients: `g`, `kg`, `ml`, `l`, `tsp`, `tbsp`, `cup`, or `pcs`. Free-text units are not allowed. |
| **Preparation step** | One separate, non-empty text entry describing part of the recipe preparation process. Preparation steps have a defined order that must be preserved when displayed. |
| **Recipe** | A shared collection item containing a name, at least one catalog ingredient, ingredient quantities and classifications, and at least one valid preparation step. It may also contain optional metadata and one optional recipe photo. |
| **Recipe ingredient entry** | The occurrence of a catalog ingredient within a specific recipe, including its quantity, predefined measurement unit, and exactly one ingredient classification. |
| **Recipe details** | The view displaying a recipe's name, creator username, complete ingredients, quantities, units, classifications, ordered preparation steps, optional metadata when provided, recipe photo when available, and contributed cooked-dish photos when available. |
| **Recipe photo** | One optional photo representing a recipe. It may be managed only by the recipe creator and is separate from cooked-dish photos. |
| **Registered user** | A user with an account identified by a unique username and unique email address. Registered users can create recipes and contribute cooked-dish photos. |
| **Search result** | A recipe returned by ingredient-based search because it is classified as either Can cook now or Almost can cook. Recipes missing 3 or more Essential ingredients are excluded. |
| **Shared recipe collection** | The collection of valid recipes visible and searchable by all users. Newly saved valid recipes become part of it immediately. |
| **User** | A person interacting with the system as either a Visitor or a Registered user. |
| **Valid recipe** | A recipe that satisfies all required recipe rules and can be saved, displayed, and included in the shared recipe collection. |
| **Visitor** | An unregistered user who can browse and search recipes and view recipe details, but cannot create, edit, delete, or contribute cooked-dish photos. |

## Terms with Explicitly Different Meanings

- A **catalog ingredient** is the standardized ingredient from the fixed ingredient catalog. A **recipe ingredient entry** is that catalog ingredient together with its recipe-specific quantity, measurement unit, and classification.
- **Photo** is not a single interchangeable concept. A **recipe photo** represents the recipe, while a **cooked-dish photo** represents a registered user's result from preparing it.
- **Classification** is not a permanent property of a catalog ingredient. It is assigned separately each time that ingredient is used in a recipe.
- **Available** means that the user selected the ingredient for the current search. It does not describe an exact quantity or an inventory amount.
- **Recipe creator** and **cooked-dish photo contributor** may be different registered users. The creator has permission to edit or delete the recipe and manage its recipe photo; each contributor controls only their own cooked-dish photo.

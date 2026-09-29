# SKED Dialogue Summary

## 1. Initial idea

The project is an information system for storing and organizing cooking recipes and helping users answer: "What can I cook with the ingredients I currently have?" Users can browse recipes, view ingredients and preparation steps, and search for suitable dishes using available ingredients. Registered users can create and manage their own recipes and contribute photos.

## 2. Main uncertainties identified

The specification process had to clarify:

- which user roles exist and what each role may do;
- whether recipes and ingredients use a fixed catalog;
- how Essential, Basic, and Optional ingredient classifications affect matching;
- whether quantities affect matching and which measurement units are allowed;
- the required recipe fields, preparation-step rules, validation, editing, and deletion behavior;
- the difference between a recipe photo and a cooked-dish photo;
- who may add, replace, or remove each type of photo;
- how registration, login, logout, authentication prompts, and failed authentication behave;
- how ingredient search behaves with one or multiple ingredients, empty selections, partial matches, and changed selections;
- which functionality is inside the university MVP and which functionality is excluded.

The repository does not preserve the complete question-by-question SKED dialogue, so this summary records only decisions supported by the approved specification artifacts.

## 3. Human decisions

The approved baseline contains exactly two roles: Visitor and Registered User. Visitors may browse, search, and view recipes and photos. Registered Users may additionally create recipes, edit and delete only recipes they created, manage their own recipe photo, and contribute one active cooked-dish photo per recipe.

Ingredient matching uses a fixed, system-controlled catalog. Recipe ingredients and search selections use the same standardized catalog identities. Each recipe ingredient entry has one quantity, one predefined unit, and one recipe-specific classification: Essential, Basic, or Optional. Matching is availability-based rather than quantity-based:

- zero missing Essential ingredients means "Can cook now";
- one or two missing Essential ingredients means "Almost can cook";
- three or more missing Essential ingredients excludes the recipe.

Basic and Optional ingredients do not count as missing Essential ingredients. Search requires at least one selected ingredient, supports updating the selection followed by an explicit new search, and orders results by match classification.

A valid recipe requires a non-empty name, at least one ingredient entry, and at least one ordered non-empty preparation step. Valid saved recipes become immediately visible and searchable. Invalid recipes and invalid edits are not saved. Recipe deletion, recipe-photo removal, and cooked-dish-photo removal require confirmation.

The MVP distinguishes one optional recipe photo from user-contributed cooked-dish photos. The recipe creator manages the recipe photo. Any Registered User may contribute one cooked-dish photo per recipe and may replace or remove only their own contribution. Usernames may be displayed publicly, but email addresses are not.

Registration requires a unique username, unique email address, and password. Login uses email and password, and logout is supported. Visitors receive a choice to log in or register before restricted actions; after successful authentication they return to the original page where possible, but the restricted action is not executed automatically.

## 4. Model assumptions corrected or rejected

The following are documented scope decisions. The repository does not preserve every original proposal, so they are stated as scope outcomes rather than as claims about exact undocumented dialogue:

- Manual ingredient entry was excluded in favor of a fixed system-controlled ingredient catalog.
- Quantity-based inventory matching was excluded in favor of availability-based matching; recipe quantities are stored and displayed but do not affect search matching.
- Administrator, moderator, and other additional roles were excluded in favor of exactly Visitor and Registered User.
- Enterprise-level performance, scalability, availability, backup, uptime, and infrastructure requirements were excluded because the project is a university MVP.
- Ratings, comments, likes, follows, recommendations, and other social features were excluded.
- Draft, unpublished, pending, publishing, archived, and recoverable recipe workflows were excluded; valid saved recipes become immediately visible and searchable.

## 5. Resulting specification baseline

The resulting project artifacts are:

- `spec/glossary.md` -- approved terminology and distinctions between related concepts;
- `spec/srs.tex` -- the baseline Software Requirements Specification with REQ-F, REQ-NF, interface requirements, and acceptance criteria;
- `spec/bdd.md` -- the initial ten-scenario BDD specification;
- `spec/traceability.md` -- mappings between requirements, acceptance criteria, BDD scenarios, and verification notes.

The baseline was independently checked for requirement-ID completeness, duplicate or missing identifiers, terminology consistency, BDD and traceability consistency, and scope alignment with the approved MVP decisions.

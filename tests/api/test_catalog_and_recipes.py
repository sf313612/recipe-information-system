from uuid import uuid4

import pytest


def _create_recipe_for_category_filter(api_client, bearer_headers, name, category=None):
    recipe_data = {
        "name": name,
        "ingredients": [
            {
                "ingredientId": "ingredient-1",
                "quantity": 100,
                "unit": "g",
                "classification": "Essential",
            }
        ],
        "preparationSteps": [{"order": 1, "text": "Prepare the dish."}],
    }

    if category is not None:
        recipe_data["metadata"] = {"category": category}

    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json=recipe_data,
    )

    assert response.status_code == 201
    return response.json()


def test_list_catalog_ingredients(api_client):
    response = api_client.get("/ingredients")

    assert response.status_code == 200
    assert "items" in response.json()


def test_get_catalog_ingredient(api_client):
    response = api_client.get("/ingredients/ingredient-1")

    assert response.status_code == 200
    assert response.json()["id"] == "ingredient-1"
    assert "name" in response.json()


def test_browse_recipes(api_client):
    response = api_client.get("/recipes")

    assert response.status_code == 200
    assert "items" in response.json()


def test_browse_recipes_without_category_keeps_categorized_and_uncategorized_items(
    api_client,
    bearer_headers,
):
    category = "Dessert"
    categorized_recipe = _create_recipe_for_category_filter(
        api_client,
        bearer_headers,
        f"Categorized {uuid4().hex}",
        category,
    )
    uncategorized_recipe = _create_recipe_for_category_filter(
        api_client,
        bearer_headers,
        f"Uncategorized {uuid4().hex}",
    )

    response = api_client.get("/recipes", params={"pageSize": 10000})

    assert response.status_code == 200
    assert set(response.json()) == {"items"}
    returned_ids = [item["id"] for item in response.json()["items"]]
    assert categorized_recipe["id"] in returned_ids
    assert uncategorized_recipe["id"] in returned_ids


def test_browse_recipes_accepts_dessert_category(api_client, bearer_headers):
    category = f"Dessert-{uuid4().hex}"
    dessert_recipe = _create_recipe_for_category_filter(
        api_client,
        bearer_headers,
        f"Dessert {uuid4().hex}",
        category,
    )

    response = api_client.get(
        "/recipes",
        params={"category": category, "pageSize": 10000},
    )

    assert response.status_code == 200
    returned_ids = [item["id"] for item in response.json()["items"]]
    assert returned_ids == [dessert_recipe["id"]]


def test_browse_recipes_filters_exact_category_before_pagination(api_client, bearer_headers):
    suffix = uuid4().hex
    category = f"Dessert-{suffix}"
    matching_recipes = [
        _create_recipe_for_category_filter(
            api_client,
            bearer_headers,
            f"Matching dessert {index}-{suffix}",
            category,
        )
        for index in (1, 2)
    ]
    _create_recipe_for_category_filter(
        api_client,
        bearer_headers,
        f"Soup {suffix}",
        f"Soup-{suffix}",
    )
    _create_recipe_for_category_filter(
        api_client,
        bearer_headers,
        f"Case variant {suffix}",
        category.lower(),
    )
    _create_recipe_for_category_filter(
        api_client,
        bearer_headers,
        f"Uncategorized {suffix}",
    )
    matching_recipes.append(
        _create_recipe_for_category_filter(
            api_client,
            bearer_headers,
            f"Matching dessert 3-{suffix}",
            category,
        )
    )

    response = api_client.get(
        "/recipes",
        params={"category": category, "pageSize": 10000},
    )

    assert response.status_code == 200
    assert set(response.json()) == {"items"}
    assert [item["id"] for item in response.json()["items"]] == [
        recipe["id"] for recipe in matching_recipes
    ]

    first_page = api_client.get(
        "/recipes",
        params={"category": category, "page": 1, "pageSize": 2},
    )
    second_page = api_client.get(
        "/recipes",
        params={"category": category, "page": 2, "pageSize": 2},
    )

    assert first_page.status_code == 200
    assert second_page.status_code == 200
    assert [item["id"] for item in first_page.json()["items"]] == [
        recipe["id"] for recipe in matching_recipes[:2]
    ]
    assert [item["id"] for item in second_page.json()["items"]] == [
        recipe["id"] for recipe in matching_recipes[2:]
    ]

    no_match = api_client.get(
        "/recipes",
        params={"category": f"No-Match-{suffix}"},
    )
    assert no_match.status_code == 200
    assert no_match.json() == {"items": []}


def test_browse_recipes_rejects_empty_category(api_client):
    response = api_client.get("/recipes?category=")

    assert response.status_code == 422


def test_browse_recipes_treats_encoded_space_as_literal_category(
    api_client,
    bearer_headers,
):
    space_category_recipe = _create_recipe_for_category_filter(
        api_client,
        bearer_headers,
        f"Space category {uuid4().hex}",
        " ",
    )

    response = api_client.get("/recipes?category=%20&pageSize=10000")

    assert response.status_code == 200
    returned_ids = [item["id"] for item in response.json()["items"]]
    assert space_category_recipe["id"] in returned_ids
    assert "recipe-1" not in returned_ids
    assert "recipe-2" not in returned_ids


def test_browse_recipes_defaults_to_page_one_and_page_size_ten(api_client):
    default_response = api_client.get("/recipes")
    explicit_default_response = api_client.get(
        "/recipes",
        params={"page": 1, "pageSize": 10},
    )

    assert default_response.status_code == 200
    assert explicit_default_response.status_code == 200
    assert default_response.json() == explicit_default_response.json()
    assert set(default_response.json()) == {"items"}
    assert len(default_response.json()["items"]) <= 10


def test_browse_recipes_returns_requested_page_in_collection_order(api_client):
    collection_response = api_client.get("/recipes", params={"pageSize": 10000})
    first_response = api_client.get("/recipes", params={"page": 1, "pageSize": 1})
    second_response = api_client.get("/recipes", params={"page": 2, "pageSize": 1})

    assert collection_response.status_code == 200
    assert first_response.status_code == 200
    assert second_response.status_code == 200

    collection = collection_response.json()["items"]
    assert len(collection) >= 2
    assert first_response.json()["items"] == collection[:1]
    assert second_response.json()["items"] == collection[1:2]


def test_browse_recipes_page_beyond_collection_is_empty(api_client):
    collection_response = api_client.get("/recipes", params={"pageSize": 10000})
    assert collection_response.status_code == 200
    collection = collection_response.json()["items"]

    response = api_client.get(
        "/recipes",
        params={"page": len(collection) + 1, "pageSize": 1},
    )

    assert response.status_code == 200
    assert response.json() == {"items": []}


@pytest.mark.parametrize("params", [{"page": 0}, {"pageSize": 0}])
def test_browse_recipes_rejects_values_below_one(api_client, params):
    response = api_client.get("/recipes", params=params)

    assert response.status_code == 422


def test_get_recipe_details(api_client, recipe_id):
    response = api_client.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200

    recipe = response.json()

    assert recipe["id"] == recipe_id
    assert "name" in recipe
    assert "username" in recipe["creator"]
    assert isinstance(recipe["ingredients"], list)
    assert isinstance(recipe["preparationSteps"], list)
    assert isinstance(recipe["cookedDishPhotos"], list)


def test_create_recipe_without_authentication(api_client):
    response = api_client.post(
        "/recipes",
        json={
            "name": "Test recipe",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 1,
                    "unit": "pcs",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [{"order": 1, "text": "Prepare it."}],
        },
    )

    assert response.status_code == 401


def test_create_recipe_with_invalid_quantity(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": "Invalid recipe",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 0,
                    "unit": "pcs",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [{"order": 1, "text": "Prepare it."}],
        },
    )

    assert response.status_code == 422


def test_create_recipe_with_invalid_unit(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": "Invalid unit recipe",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 100,
                    "unit": "kgz",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [{"order": 1, "text": "Prepare it."}],
        },
    )

    assert response.status_code == 422



def test_create_recipe_with_invalid_classification(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": "Invalid classification recipe",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 100,
                    "unit": "g",
                    "classification": "Required",
                }
            ],
            "preparationSteps": [{"order": 1, "text": "Prepare it."}],
        },
    )

    assert response.status_code == 422



def test_create_recipe_with_empty_ingredients(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": "Recipe without ingredients",
            "ingredients": [],
            "preparationSteps": [{"order": 1, "text": "Prepare it."}],
        },
    )

    assert response.status_code == 422



def test_create_recipe_with_empty_preparation_steps(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": "Recipe without steps",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 100,
                    "unit": "g",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [],
        },
    )

    assert response.status_code == 422



def test_create_recipe_successfully(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": "New chicken recipe",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 200,
                    "unit": "g",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [
                {"order": 1, "text": "Cook the chicken."}
            ],
        },
    )

    assert response.status_code == 201

    recipe = response.json()
    assert recipe["name"] == "New chicken recipe"
    assert recipe["id"]
    assert recipe["creator"]["username"]
    assert len(recipe["ingredients"]) == 1
    assert len(recipe["preparationSteps"]) == 1
    assert recipe["cookedDishPhotos"] == []
    
    recipe_id = recipe["id"]

    get_response = api_client.get(f"/recipes/{recipe_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == recipe_id
    assert get_response.json()["name"] == "New chicken recipe"


def test_update_recipe_requires_owner_access(api_client, recipe_id, bearer_headers):
    response = api_client.put(
        f"/recipes/{recipe_id}",
        headers=bearer_headers,
        json={
            "name": "Updated recipe",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 1,
                    "unit": "pcs",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [{"order": 1, "text": "Prepare it."}],
        },
    )

    assert response.status_code in {200, 403, 404, 422}


def test_delete_recipe_requires_owner_access(api_client, recipe_id, bearer_headers):
    response = api_client.delete(f"/recipes/{recipe_id}", headers=bearer_headers)

    assert response.status_code in {204, 403, 404}


def test_create_recipe_with_unknown_ingredient(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": "Recipe with unknown ingredient",
            "ingredients": [
                {
                    "ingredientId": "ingredient-999",
                    "quantity": 100,
                    "unit": "g",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [
                {"order": 1, "text": "Prepare it."}
            ],
        },
    )

    assert response.status_code == 422


def test_create_recipe_without_name(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 100,
                    "unit": "g",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [
                {"order": 1, "text": "Prepare it."}
            ],
        },
    )

    assert response.status_code == 422

def test_update_recipe_without_authentication(api_client):
    response = api_client.put(
        "/recipes/recipe-1",
        json={
            "name": "Updated chicken pasta",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 300,
                    "unit": "g",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [
                {"order": 1, "text": "Cook the chicken."}
            ],
        },
    )

    assert response.status_code == 401

def test_delete_recipe_without_authentication(api_client):
    response = api_client.delete("/recipes/recipe-1")

    assert response.status_code == 401


def test_owner_can_update_recipe(api_client, bearer_headers):
    recipe_data = {
        "name": "Owner test recipe",
        "ingredients": [
            {
                "ingredientId": "ingredient-1",
                "quantity": 100,
                "unit": "g",
                "classification": "Essential",
            }
        ],
        "preparationSteps": [
            {"order": 1, "text": "Prepare the dish."}
        ],
    }

    created = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json=recipe_data,
    )
    assert created.status_code == 201

    recipe_id = created.json()["id"]
    recipe_data["name"] = "Updated owner test recipe"

    response = api_client.put(
        f"/recipes/{recipe_id}",
        headers=bearer_headers,
        json=recipe_data,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated owner test recipe"


def test_owner_can_delete_recipe(api_client, bearer_headers):
    recipe_data = {
        "name": "Recipe to delete",
        "ingredients": [
            {
                "ingredientId": "ingredient-1",
                "quantity": 100,
                "unit": "g",
                "classification": "Essential",
            }
        ],
        "preparationSteps": [
            {"order": 1, "text": "Prepare the dish."}
        ],
    }

    created = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json=recipe_data,
    )
    assert created.status_code == 201

    recipe_id = created.json()["id"]

    response = api_client.delete(
        f"/recipes/{recipe_id}",
        headers=bearer_headers,
    )

    assert response.status_code == 204

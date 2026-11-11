def test_search_with_non_empty_ingredients(api_client):
    response = api_client.post(
        "/recipes/search",
        json={"ingredientIds": ["ingredient-1"]},
    )

    assert response.status_code == 200
    assert isinstance(response.json()["items"], list)


def test_search_with_empty_ingredients(api_client):
    response = api_client.post(
        "/recipes/search",
        json={"ingredientIds": []},
    )

    assert response.status_code == 422


def test_search_with_missing_ingredient_ids(api_client):
    response = api_client.post("/recipes/search", json={})

    assert response.status_code == 422




def test_search_returns_matching_recipe(api_client):
    response = api_client.post(
        "/recipes/search",
        json={"ingredientIds": ["ingredient-1"]},
    )

    assert response.status_code == 200

    items = response.json()["items"]

    chicken_recipe = next(
        item for item in items
        if item["recipeId"] == "recipe-1"
    )

    tomato_recipe = next(
        item for item in items
        if item["recipeId"] == "recipe-2"
    )

    assert chicken_recipe["classification"] == "Can cook now"
    assert chicken_recipe["missingEssentialIngredients"] == []

    assert tomato_recipe["classification"] == "Almost can cook"
    assert tomato_recipe["missingEssentialIngredients"] == [
        {"id": "ingredient-3", "name": "tomato"}
    ]



def test_search_with_unknown_ingredient(api_client):
    response = api_client.post(
        "/recipes/search",
        json={"ingredientIds": ["ingredient-999"]},
    )

    assert response.status_code == 404


def test_search_ignores_basic_and_optional_ingredients(api_client, bearer_headers):
    recipe_data = {
        "name": "Search classification test",
        "ingredients": [
            {
                "ingredientId": "ingredient-1",
                "quantity": 100,
                "unit": "g",
                "classification": "Essential",
            },
            {
                "ingredientId": "ingredient-2",
                "quantity": 100,
                "unit": "g",
                "classification": "Basic",
            },
            {
                "ingredientId": "ingredient-3",
                "quantity": 100,
                "unit": "g",
                "classification": "Optional",
            },
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

    response = api_client.post(
        "/recipes/search",
        json={"ingredientIds": ["ingredient-1"]},
    )

    assert response.status_code == 200

    result = next(
        item for item in response.json()["items"]
        if item["recipeId"] == recipe_id
    )

    assert result["classification"] == "Can cook now"
    assert result["missingEssentialIngredients"] == []

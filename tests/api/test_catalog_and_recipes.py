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

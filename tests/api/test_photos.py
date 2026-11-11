
def test_upload_recipe_photo(api_client, bearer_headers, recipe_id):
    response = api_client.put(
        f"/recipes/{recipe_id}/photo",
        headers=bearer_headers,
        files={"photo": ("recipe.jpg", b"test-image", "image/jpeg")},
    )

    assert response.status_code == 403


def test_delete_recipe_photo(api_client, bearer_headers, recipe_id):
    response = api_client.delete(
        f"/recipes/{recipe_id}/photo",
        headers=bearer_headers,
    )

    assert response.status_code == 403


def test_upload_cooked_dish_photo(api_client, bearer_headers, recipe_id):
    response = api_client.post(
        f"/recipes/{recipe_id}/cooked-dish-photos",
        headers=bearer_headers,
        files={"photo": ("dish.jpg", b"test-image", "image/jpeg")},
    )

    assert response.status_code == 201


def test_upload_duplicate_cooked_dish_photo(api_client, bearer_headers, recipe_id):
    response = api_client.post(
        f"/recipes/{recipe_id}/cooked-dish-photos",
        headers=bearer_headers,
        files={"photo": ("dish.jpg", b"test-image", "image/jpeg")},
    )

    assert response.status_code == 409



def test_replace_my_cooked_dish_photo(api_client, bearer_headers):
    recipe_id = "recipe-2"

    upload = api_client.post(
        f"/recipes/{recipe_id}/cooked-dish-photos",
        headers=bearer_headers,
        files={"photo": ("dish.jpg", b"test-image", "image/jpeg")},
    )

    assert upload.status_code == 201

    response = api_client.put(
        f"/recipes/{recipe_id}/cooked-dish-photos/me",
        headers=bearer_headers,
        files={"photo": ("new-dish.jpg", b"new-image", "image/jpeg")},
    )

    assert response.status_code == 200



def test_delete_my_cooked_dish_photo(api_client, bearer_headers):
    recipe_data = {
        "name": "Temporary photo test recipe",
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

    upload = api_client.post(
        f"/recipes/{recipe_id}/cooked-dish-photos",
        headers=bearer_headers,
        files={"photo": ("dish.jpg", b"test-image", "image/jpeg")},
    )

    assert upload.status_code == 201

    response = api_client.delete(
        f"/recipes/{recipe_id}/cooked-dish-photos/me",
        headers=bearer_headers,
    )

    assert response.status_code == 204

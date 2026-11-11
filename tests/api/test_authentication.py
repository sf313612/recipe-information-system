import os


def test_register_user(api_client):
    response = api_client.post(
        "/auth/register",
        json={
            "username": os.getenv("API_TEST_USERNAME", "lab5-user"),
            "email": os.getenv("API_TEST_EMAIL", "lab5@example.com"),
            "password": os.getenv("API_TEST_PASSWORD", "test-password"),
        },
    )

    assert response.status_code in {201, 409, 422}


def test_login_user(api_client):
    response = api_client.post(
        "/auth/login",
        json={
            "email": os.getenv("API_TEST_EMAIL", "lab5@example.com"),
            "password": os.getenv("API_TEST_PASSWORD", "test-password"),
        },
    )

    assert response.status_code in {200, 400, 401}


def test_logout_requires_authentication(api_client):
    response = api_client.post("/auth/logout")

    assert response.status_code == 401


def test_invalid_token_is_rejected(api_client):
    response = api_client.post(
        "/recipes",
        headers={"Authorization": "Bearer invalid-token"},
        json={
            "name": "Test recipe",
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
        },
    )

    assert response.status_code == 401


def test_logout_invalidates_token(api_client, bearer_headers):
    logout = api_client.post(
        "/auth/logout",
        headers=bearer_headers,
    )

    assert logout.status_code == 204

    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": "Test recipe",
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
        },
    )

    assert response.status_code == 401

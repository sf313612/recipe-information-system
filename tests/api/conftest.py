import os

import httpx
import pytest


@pytest.fixture
def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")


@pytest.fixture
def api_client(api_base_url: str):
    with httpx.Client(base_url=api_base_url) as client:
        yield client


@pytest.fixture
def bearer_headers(api_client):
    username = os.getenv("API_TEST_USERNAME", "lab5-user")
    email = os.getenv("API_TEST_EMAIL", "lab5@example.com")
    password = os.getenv("API_TEST_PASSWORD", "test-password")

    registration = api_client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert registration.status_code in {201, 409}

    login = api_client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert login.status_code == 200
    token = login.json()["accessToken"]

    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def recipe_id() -> str:
    return os.getenv("API_TEST_RECIPE_ID", "recipe-1")

from io import BytesIO
import os
from pathlib import Path
from uuid import uuid4

from PIL import Image
import pytest

PHOTO_STORAGE_DIR = Path(
    os.environ.get(
        "PHOTO_STORAGE_DIR",
        Path(__file__).resolve().parents[2] / "photo_uploads",
    )
)


def _valid_image_bytes(color=(20, 80, 140), image_format="PNG"):
    image_buffer = BytesIO()
    Image.new("RGB", (2, 2), color=color).save(image_buffer, format=image_format)
    return image_buffer.getvalue()


def _expected_test_username():
    return os.getenv("API_TEST_USERNAME", "lab5-user")


def _create_recipe(api_client, bearer_headers):
    response = api_client.post(
        "/recipes",
        headers=bearer_headers,
        json={
            "name": f"Photo test {uuid4().hex}",
            "ingredients": [
                {
                    "ingredientId": "ingredient-1",
                    "quantity": 100,
                    "unit": "g",
                    "classification": "Essential",
                }
            ],
            "preparationSteps": [{"order": 1, "text": "Prepare the dish."}],
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def _register_another_user(api_client):
    suffix = uuid4().hex
    credentials = {
        "username": f"photo-user-{suffix}",
        "email": f"photo-user-{suffix}@example.test",
        "password": "test-password",
    }
    registration = api_client.post("/auth/register", json=credentials)
    assert registration.status_code == 201

    login = api_client.post(
        "/auth/login",
        json={"email": credentials["email"], "password": credentials["password"]},
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['accessToken']}"}


def _upload_recipe_photo(api_client, recipe_id, headers, content):
    return api_client.put(
        f"/recipes/{recipe_id}/photo",
        headers=headers,
        files={"photo": ("recipe.png", content, "image/png")},
    )


def _upload_cooked_photo(api_client, recipe_id, headers, content):
    return api_client.post(
        f"/recipes/{recipe_id}/cooked-dish-photos",
        headers=headers,
        files={"photo": ("dish.png", content, "image/png")},
    )


def test_recipe_photo_upload_retry_replacement_and_retrieval(
    api_client,
    bearer_headers,
):
    recipe_id = _create_recipe(api_client, bearer_headers)

    for invalid_content in (b"", b"not an image"):
        invalid_upload = _upload_recipe_photo(
            api_client,
            recipe_id,
            bearer_headers,
            invalid_content,
        )
        assert invalid_upload.status_code == 422
        recipe = api_client.get(f"/recipes/{recipe_id}").json()
        assert recipe["recipePhoto"] is None

    first_image = _valid_image_bytes()
    upload = _upload_recipe_photo(api_client, recipe_id, bearer_headers, first_image)
    assert upload.status_code == 200
    first_photo = upload.json()
    assert first_photo["url"].startswith("http://") or first_photo["url"].startswith(
        "https://"
    )

    retrieved = api_client.get(first_photo["url"])
    assert retrieved.status_code == 200
    assert retrieved.content == first_image
    assert retrieved.headers["content-type"] == "image/png"

    original_metadata = api_client.get(f"/recipes/{recipe_id}").json()["recipePhoto"]
    assert original_metadata == first_photo

    for invalid_content in (b"", b"not an image"):
        invalid_replacement = _upload_recipe_photo(
            api_client,
            recipe_id,
            bearer_headers,
            invalid_content,
        )
        assert invalid_replacement.status_code == 422
        current_recipe = api_client.get(f"/recipes/{recipe_id}").json()
        assert current_recipe["recipePhoto"] == original_metadata
        still_available = api_client.get(first_photo["url"])
        assert still_available.status_code == 200
        assert still_available.content == first_image

    replacement_image = _valid_image_bytes(color=(180, 40, 70))
    replacement = _upload_recipe_photo(
        api_client,
        recipe_id,
        bearer_headers,
        replacement_image,
    )
    assert replacement.status_code == 200
    assert replacement.json()["id"] == first_photo["id"]
    assert replacement.json()["url"] == first_photo["url"]
    replaced_image = api_client.get(first_photo["url"])
    assert replaced_image.status_code == 200
    assert replaced_image.content == replacement_image

    delete = api_client.delete(
        f"/recipes/{recipe_id}/photo",
        headers=bearer_headers,
    )
    assert delete.status_code == 204
    assert api_client.get(first_photo["url"]).status_code == 404
    assert api_client.get(f"/recipes/{recipe_id}").json()["recipePhoto"] is None


def test_recipe_search_returns_a_retrievable_photo_url(api_client, bearer_headers):
    recipe_id = _create_recipe(api_client, bearer_headers)
    image_bytes = _valid_image_bytes()
    upload = _upload_recipe_photo(api_client, recipe_id, bearer_headers, image_bytes)
    assert upload.status_code == 200

    search = api_client.post(
        "/recipes/search",
        json={"ingredientIds": ["ingredient-1"]},
    )

    assert search.status_code == 200
    result = next(
        item for item in search.json()["items"] if item["recipeId"] == recipe_id
    )
    assert result["recipePhoto"] == upload.json()

    retrieved = api_client.get(result["recipePhoto"]["url"])
    assert retrieved.status_code == 200
    assert retrieved.content == image_bytes
    assert retrieved.headers["content-type"] == "image/png"


def test_deleting_recipe_removes_associated_photo_files(api_client, bearer_headers):
    recipe_id = _create_recipe(api_client, bearer_headers)
    recipe_photo = _upload_recipe_photo(
        api_client, recipe_id, bearer_headers, _valid_image_bytes()
    )
    assert recipe_photo.status_code == 200
    cooked_photo = _upload_cooked_photo(
        api_client, recipe_id, bearer_headers, _valid_image_bytes(color=(80, 20, 140))
    )
    assert cooked_photo.status_code == 201

    stored_paths = [
        PHOTO_STORAGE_DIR / f"{photo['id']}.image"
        for photo in (recipe_photo.json(), cooked_photo.json())
    ]
    assert all(path.is_file() for path in stored_paths)

    deleted = api_client.delete(f"/recipes/{recipe_id}", headers=bearer_headers)

    assert deleted.status_code == 204
    assert all(not path.exists() for path in stored_paths)
    assert api_client.get(recipe_photo.json()["url"]).status_code == 404
    assert api_client.get(cooked_photo.json()["url"]).status_code == 404


@pytest.mark.parametrize("image_format", ["BMP", "PPM"])
def test_photo_retrieval_uses_image_media_type_without_pillow_mapping(
    api_client,
    bearer_headers,
    image_format,
):
    image_bytes = _valid_image_bytes(image_format=image_format)
    recipe_id = _create_recipe(api_client, bearer_headers)
    upload = _upload_recipe_photo(api_client, recipe_id, bearer_headers, image_bytes)
    assert upload.status_code == 200

    retrieved = api_client.get(upload.json()["url"])

    assert retrieved.status_code == 200
    assert retrieved.content == image_bytes
    assert retrieved.headers["content-type"].startswith("image/")
    assert retrieved.headers["content-type"] != "application/octet-stream"


def test_cooked_dish_photo_upload_retry_duplicate_replacement_and_retrieval(
    api_client,
    bearer_headers,
):
    recipe_id = "recipe-2"

    for invalid_content in (b"", b"not an image"):
        invalid_upload = _upload_cooked_photo(
            api_client,
            recipe_id,
            bearer_headers,
            invalid_content,
        )
        assert invalid_upload.status_code == 422
        recipe = api_client.get(f"/recipes/{recipe_id}").json()
        assert recipe["cookedDishPhotos"] == []

    first_image = _valid_image_bytes()
    upload = _upload_cooked_photo(api_client, recipe_id, bearer_headers, first_image)
    assert upload.status_code == 201
    first_photo = upload.json()

    retrieved = api_client.get(first_photo["url"])
    assert retrieved.status_code == 200
    assert retrieved.content == first_image
    assert retrieved.headers["content-type"] == "image/png"
    assert first_photo["contributor"]["username"] == _expected_test_username()
    recipe_details = api_client.get(f"/recipes/{recipe_id}").json()
    assert (
        recipe_details["cookedDishPhotos"][0]["contributor"]["username"]
        == _expected_test_username()
    )

    duplicate = _upload_cooked_photo(
        api_client,
        recipe_id,
        bearer_headers,
        _valid_image_bytes(color=(10, 200, 90)),
    )
    assert duplicate.status_code == 409

    original_metadata = api_client.get(f"/recipes/{recipe_id}").json()[
        "cookedDishPhotos"
    ][0]
    for invalid_content in (b"", b"not an image"):
        invalid_replacement = api_client.put(
            f"/recipes/{recipe_id}/cooked-dish-photos/me",
            headers=bearer_headers,
            files={"photo": ("dish.png", invalid_content, "image/png")},
        )
        assert invalid_replacement.status_code == 422
        current_recipe = api_client.get(f"/recipes/{recipe_id}").json()
        assert current_recipe["cookedDishPhotos"] == [original_metadata]
        still_available = api_client.get(first_photo["url"])
        assert still_available.status_code == 200
        assert still_available.content == first_image

    replacement_image = _valid_image_bytes(color=(180, 40, 70))
    replacement = api_client.put(
        f"/recipes/{recipe_id}/cooked-dish-photos/me",
        headers=bearer_headers,
        files={"photo": ("new-dish.png", replacement_image, "image/png")},
    )
    assert replacement.status_code == 200
    assert replacement.json()["id"] == first_photo["id"]
    assert replacement.json()["contributor"]["username"] == _expected_test_username()
    replaced_image = api_client.get(first_photo["url"])
    assert replaced_image.status_code == 200
    assert replaced_image.content == replacement_image

    delete = api_client.delete(
        f"/recipes/{recipe_id}/cooked-dish-photos/me",
        headers=bearer_headers,
    )
    assert delete.status_code == 204
    assert api_client.get(first_photo["url"]).status_code == 404
    assert api_client.get(f"/recipes/{recipe_id}").json()["cookedDishPhotos"] == []


def test_photo_permissions_and_contributor_ownership(api_client, bearer_headers):
    recipe_id = _create_recipe(api_client, bearer_headers)
    other_user_headers = _register_another_user(api_client)
    image = _valid_image_bytes()

    owner_upload = _upload_recipe_photo(
        api_client,
        recipe_id,
        bearer_headers,
        image,
    )
    assert owner_upload.status_code == 200
    forbidden_upload = _upload_recipe_photo(
        api_client,
        recipe_id,
        other_user_headers,
        _valid_image_bytes(color=(120, 120, 30)),
    )
    assert forbidden_upload.status_code == 403
    forbidden_delete = api_client.delete(
        f"/recipes/{recipe_id}/photo",
        headers=other_user_headers,
    )
    assert forbidden_delete.status_code == 403

    cooked_upload = _upload_cooked_photo(
        api_client,
        recipe_id,
        bearer_headers,
        image,
    )
    assert cooked_upload.status_code == 201
    other_user_replace = api_client.put(
        f"/recipes/{recipe_id}/cooked-dish-photos/me",
        headers=other_user_headers,
        files={"photo": ("other.png", image, "image/png")},
    )
    assert other_user_replace.status_code == 404
    other_user_delete = api_client.delete(
        f"/recipes/{recipe_id}/cooked-dish-photos/me",
        headers=other_user_headers,
    )
    assert other_user_delete.status_code == 404

    assert api_client.get(owner_upload.json()["url"]).content == image
    assert api_client.get(cooked_upload.json()["url"]).content == image
    assert api_client.delete(
        f"/recipes/{recipe_id}/photo",
        headers=bearer_headers,
    ).status_code == 204
    assert api_client.delete(
        f"/recipes/{recipe_id}/cooked-dish-photos/me",
        headers=bearer_headers,
    ).status_code == 204

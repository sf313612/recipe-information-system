
import logging
import secrets
import hashlib
import time

from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    Header,
    UploadFile,
    File,
    Request,
)

from src.schemas import (
    RecipeWriteRequest,
    SearchRequest,
    RegisterRequest,
    LoginRequest,
)

app = FastAPI(title="Recipe Information System API")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("recipe_api")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration = (time.perf_counter() - start_time) * 1000

        logger.info(
            "%s %s | Status: %s | Duration: %.2f ms",
            request.method,
            request.url.path,
            status_code,
            duration,
        )

INGREDIENTS = [
    {"id": "ingredient-1", "name": "chicken"},
    {"id": "ingredient-2", "name": "pasta"},
    {"id": "ingredient-3", "name": "tomato"},
]

RECIPES = [
    {
        "id": "recipe-1",
        "name": "Chicken pasta",
        "creator": {"username": "recipe-author"},
        "ingredients": [
            {
                "ingredientId": "ingredient-1",
                "quantity": 200,
                "unit": "g",
                "classification": "Essential",
                "name": "chicken",
            }
        ],
        "preparationSteps": [
            {"order": 1, "text": "Cook the chicken."}
        ],
        "recipePhoto": None,
        "cookedDishPhotos": [],
    },
    {
        "id": "recipe-2",
        "name": "Tomato pasta",
        "creator": {"username": "recipe-author"},
        "ingredients": [
            {
                "ingredientId": "ingredient-3",
                "quantity": 150,
                "unit": "g",
                "classification": "Essential",
                "name": "tomato",
            }
        ],
        "preparationSteps": [
            {"order": 1, "text": "Prepare the tomatoes."}
        ],
        "recipePhoto": None,
        "cookedDishPhotos": [],
    },
]

USERS = []
TOKENS = {}

def get_current_username(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")

    token = authorization.removeprefix("Bearer ")
    username = TOKENS.get(token)

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return username

@app.post("/api/auth/register", status_code=201)
def register_user(user: RegisterRequest):
    if any(
        item["username"] == user.username or item["email"] == user.email
        for item in USERS
    ):
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashlib.sha256(user.password.encode()).hexdigest(),
    }

    USERS.append(new_user)

    logger.info("User registered successfully")

    return {"user": {"username": new_user["username"]}}


@app.post("/api/auth/login")
def login_user(user: LoginRequest):
    password_hash = hashlib.sha256(user.password.encode()).hexdigest()

    account = next(
        (
            item for item in USERS
            if item["email"] == user.email
            and item["password"] == password_hash
        ),
        None,
    )

    if account is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_urlsafe(32)
    TOKENS[token] = account["username"]

    logger.info("User logged in successfully")

    return {
        "user": {"username": account["username"]},
        "accessToken": token,
    }


@app.post("/api/auth/logout", status_code=204)
def logout_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")

    token = authorization.removeprefix("Bearer ")

    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")

    del TOKENS[token]

    logger.info("User logged out successfully")


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/ingredients")
def list_ingredients() -> dict[str, list[dict[str, str]]]:
    return {"items": INGREDIENTS}


@app.get("/api/ingredients/{ingredient_id}")
def get_ingredient(ingredient_id: str) -> dict[str, str]:
    for ingredient in INGREDIENTS:
        if ingredient["id"] == ingredient_id:
            return ingredient

    raise HTTPException(status_code=404, detail="Ingredient not found")


@app.get("/api/recipes")
def list_recipes(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, alias="pageSize", ge=1),
) -> dict[str, list[dict[str, object]]]:
    start = (page - 1) * page_size
    end = start + page_size
    return {"items": RECIPES[start:end]}

@app.get("/api/recipes/{recipe_id}")
def get_recipe(recipe_id: str) -> dict[str, object]:
    for recipe in RECIPES:
        if recipe["id"] == recipe_id:
            return recipe

    raise HTTPException(status_code=404, detail="Recipe not found")


@app.post("/api/recipes/search")
def search_recipes(request: SearchRequest) -> dict[str, list[dict[str, object]]]:
    selected_ids = set(request.ingredient_ids)

    for ingredient_id in selected_ids:
        if not any(item["id"] == ingredient_id for item in INGREDIENTS):
            raise HTTPException(status_code=404, detail="Ingredient not found")

    results = []

    for recipe in RECIPES:
        missing_essential = [
            ingredient
            for ingredient in recipe["ingredients"]
            if ingredient["classification"] == "Essential"
            and ingredient["ingredientId"] not in selected_ids
        ]

        if len(missing_essential) >= 3:
            continue

        classification = (
            "Can cook now"
            if len(missing_essential) == 0
            else "Almost can cook"
        )

        missing_ingredients = [
            {
                "id": ingredient["ingredientId"],
                "name": ingredient["name"],
            }
            for ingredient in missing_essential
        ]

        results.append({
            "recipeId": recipe["id"],
            "name": recipe["name"],
            "classification": classification,
            "missingEssentialIngredients": missing_ingredients,
            "recipePhoto": recipe.get("recipePhoto"),
        })

    results.sort(
        key=lambda item: 0 if item["classification"] == "Can cook now" else 1
    )

    return {"items": results}


@app.post("/api/recipes", status_code=201)
def create_recipe(
    recipe: RecipeWriteRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, object]:
    username = get_current_username(authorization)

    recipe_data = recipe.model_dump(by_alias=True, exclude_none=True)

    for ingredient in recipe_data["ingredients"]:
        catalog_ingredient = next(
            (
                item
                for item in INGREDIENTS
                if item["id"] == ingredient["ingredientId"]
            ),
            None,
        )

        if catalog_ingredient is None:
            raise HTTPException(status_code=422, detail="Unknown ingredient")

        ingredient["name"] = catalog_ingredient["name"]

    new_recipe = {
        "id": f"recipe-{len(RECIPES) + 1}",
        "name": recipe_data["name"],
        "creator": {"username": username},
        "ingredients": recipe_data["ingredients"],
        "preparationSteps": recipe_data["preparationSteps"],
        "recipePhoto": None,
        "cookedDishPhotos": [],
    }

    if "metadata" in recipe_data:
        new_recipe["metadata"] = recipe_data["metadata"]

    RECIPES.append(new_recipe)

    logger.info("Recipe created: %s", new_recipe["id"])

    return new_recipe


@app.put("/api/recipes/{recipe_id}")
def update_recipe(
    recipe_id: str,
    recipe: RecipeWriteRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, object]:
    username = get_current_username(authorization)

    existing_recipe = next(
        (item for item in RECIPES if item["id"] == recipe_id),
        None,
    )

    if existing_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if existing_recipe["creator"]["username"] != username:
        raise HTTPException(status_code=403, detail="Not the recipe owner")

    recipe_data = recipe.model_dump(by_alias=True, exclude_none=True)

    for ingredient in recipe_data["ingredients"]:
        catalog_ingredient = next(
            (item for item in INGREDIENTS if item["id"] == ingredient["ingredientId"]),
            None,
        )

        if catalog_ingredient is None:
            raise HTTPException(status_code=422, detail="Unknown ingredient")

        ingredient["name"] = catalog_ingredient["name"]

    existing_recipe.update({
        "name": recipe_data["name"],
        "ingredients": recipe_data["ingredients"],
        "preparationSteps": recipe_data["preparationSteps"],
    })

    if "metadata" in recipe_data:
        existing_recipe["metadata"] = recipe_data["metadata"]

    logger.info("Recipe updated: %s", recipe_id)
    
    return existing_recipe


@app.delete("/api/recipes/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: str,
    authorization: str | None = Header(default=None),
) -> None:
    username = get_current_username(authorization)

    recipe = next(
    (item for item in RECIPES if item["id"] == recipe_id),
        None,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe["creator"]["username"] != username:
        raise HTTPException(status_code=403, detail="Not the recipe owner")

    RECIPES.remove(recipe)

    logger.info("Recipe deleted: %s", recipe_id)



@app.put("/api/recipes/{recipe_id}/photo")
def upload_recipe_photo(
    recipe_id: str,
    photo: UploadFile = File(...),
    authorization: str | None = Header(default=None),
) -> dict[str, object]:
    username = get_current_username(authorization)

    recipe = next(
        (item for item in RECIPES if item["id"] == recipe_id),
        None,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe["creator"]["username"] != username:
        raise HTTPException(status_code=403, detail="Not the recipe owner")

    photo_data = {
        "id": f"photo-{recipe_id}",
        "url": f"/uploads/{photo.filename}",
        "contributor": {"username": username},
    }

    recipe["recipePhoto"] = photo_data

    logger.info("Recipe photo uploaded: %s", recipe_id)

    return photo_data


@app.delete("/api/recipes/{recipe_id}/photo", status_code=204)
def delete_recipe_photo(
    recipe_id: str,
    authorization: str | None = Header(default=None),
) -> None:
    username = get_current_username(authorization)

    recipe = next(
        (item for item in RECIPES if item["id"] == recipe_id),
        None,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe["creator"]["username"] != username:
        raise HTTPException(status_code=403, detail="Not the recipe owner")

    if recipe["recipePhoto"] is None:
        raise HTTPException(status_code=404, detail="Recipe photo not found")

    recipe["recipePhoto"] = None

    logger.info("Recipe photo deleted: %s", recipe_id)


@app.post("/api/recipes/{recipe_id}/cooked-dish-photos", status_code=201)
def upload_cooked_dish_photo(
    recipe_id: str,
    photo: UploadFile = File(...),
    authorization: str | None = Header(default=None),
) -> dict[str, object]:
    username = get_current_username(authorization)

    recipe = next(
        (item for item in RECIPES if item["id"] == recipe_id),
        None,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if any(
        item["contributor"]["username"] == username
        for item in recipe["cookedDishPhotos"]
    ):
        raise HTTPException(
            status_code=409,
            detail="You already have a cooked dish photo for this recipe",
        )

    photo_data = {
        "id": f"cooked-photo-{recipe_id}-{secrets.token_hex(4)}",
        "url": f"/uploads/{photo.filename}",
        "contributor": {"username": username},
    }

    recipe["cookedDishPhotos"].append(photo_data)

    logger.info("Cooked dish photo uploaded: %s", recipe_id)

    return photo_data


@app.put("/api/recipes/{recipe_id}/cooked-dish-photos/me")
def replace_my_cooked_dish_photo(
    recipe_id: str,
    photo: UploadFile = File(...),
    authorization: str | None = Header(default=None),
) -> dict[str, object]:
    username = get_current_username(authorization)

    recipe = next(
        (item for item in RECIPES if item["id"] == recipe_id),
        None,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    existing_photo = next(
        (
            item for item in recipe["cookedDishPhotos"]
            if item["contributor"]["username"] == username
        ),
        None,
    )

    if existing_photo is None:
        raise HTTPException(status_code=404, detail="Your cooked dish photo not found")

    photo_data = {
        "id": existing_photo["id"],
        "url": f"/uploads/{photo.filename}",
        "contributor": {"username": username},
    }

    photo_index = recipe["cookedDishPhotos"].index(existing_photo)
    recipe["cookedDishPhotos"][photo_index] = photo_data

    logger.info("Cooked dish photo replaced: %s", recipe_id)

    return photo_data


@app.delete(
    "/api/recipes/{recipe_id}/cooked-dish-photos/me",
    status_code=204,
)
def delete_my_cooked_dish_photo(
    recipe_id: str,
    authorization: str | None = Header(default=None),
) -> None:
    username = get_current_username(authorization)

    recipe = next(
        (item for item in RECIPES if item["id"] == recipe_id),
        None,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    photo_index = next(
        (
            index for index, item in enumerate(recipe["cookedDishPhotos"])
            if item["contributor"]["username"] == username
        ),
        None,
    )

    if photo_index is None:
        raise HTTPException(status_code=404, detail="Your cooked dish photo not found")

    recipe["cookedDishPhotos"].pop(photo_index)

    logger.info("Cooked dish photo deleted: %s", recipe_id)

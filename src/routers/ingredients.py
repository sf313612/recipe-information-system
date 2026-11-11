from fastapi import APIRouter, HTTPException


INGREDIENTS = [
    {"id": "ingredient-1", "name": "chicken"},
    {"id": "ingredient-2", "name": "pasta"},
    {"id": "ingredient-3", "name": "tomato"},
]

router = APIRouter()


@router.get("/api/ingredients")
def list_ingredients() -> dict[str, list[dict[str, str]]]:
    return {"items": INGREDIENTS}


@router.get("/api/ingredients/{ingredient_id}")
def get_ingredient(ingredient_id: str) -> dict[str, str]:
    for ingredient in INGREDIENTS:
        if ingredient["id"] == ingredient_id:
            return ingredient

    raise HTTPException(status_code=404, detail="Ingredient not found")

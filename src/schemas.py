
from typing import Literal

from pydantic import BaseModel, Field


class IngredientEntryRequest(BaseModel):
    ingredient_id: str = Field(alias="ingredientId")
    quantity: float = Field(gt=0)
    unit: Literal["g", "kg", "ml", "l", "tsp", "tbsp", "cup", "pcs"]
    classification: Literal["Essential", "Basic", "Optional"]


class PreparationStepRequest(BaseModel):
    order: int = Field(ge=1)
    text: str


class RecipeWriteRequest(BaseModel):
    name: str
    ingredients: list[IngredientEntryRequest] = Field(min_length=1)
    preparation_steps: list[PreparationStepRequest] = Field(
        alias="preparationSteps",
        min_length=1,
    )
    metadata: dict[str, object] | None = None

class SearchRequest(BaseModel):
    ingredient_ids: list[str] = Field(
        alias="ingredientIds",
        min_length=1,
    )

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str
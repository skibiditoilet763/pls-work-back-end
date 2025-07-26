from fastapi import APIRouter
from schemas.ingredient_schema import IngredientCreate, IngredientUpdate, IngredientOut
from typing import List
from routes.utils.ingredient import create_ingredient_db, get_ingredients_db, update_ingredient_db, delete_ingredient_db

router = APIRouter()

@router.post("/", response_model=IngredientOut)
def create_ingredient(ingredient: IngredientCreate):
    return create_ingredient_db(ingredient)

@router.get("/", response_model=List[IngredientOut])
def get_ingredients(query: str = ""):
    return get_ingredients_db(query)

@router.put("/{ingredient_id}", response_model=IngredientOut)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate):
    return update_ingredient_db(ingredient_id, ingredient)

@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int):
    return delete_ingredient_db(ingredient_id)
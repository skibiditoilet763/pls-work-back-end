from schemas.ingredient_schema import IngredientCreate, IngredientUpdate, IngredientOut
from db import get_connection
from fastapi import HTTPException

def create_ingredient_db(ingredient: IngredientCreate) -> IngredientOut:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tbl_Ingredients (IngredientName) VALUES (?)",
        (ingredient.IngredientName,),
    )
    conn.commit()
    cursor.execute("SELECT @@IDENTITY")
    ingredient_id = cursor.fetchone()[0]
    cursor.execute(
        "SELECT IngredientId, IngredientName FROM tbl_Ingredients WHERE IngredientId = ?",
        (ingredient_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return IngredientOut(IngredientId=row[0], IngredientName=row[1])

def get_ingredients_db(query: str = "") -> list[IngredientOut]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT IngredientId, IngredientName FROM tbl_Ingredients WHERE IngredientName LIKE ?",
        (f"%{query}%",),
    )
    rows = cursor.fetchall()
    conn.close()
    return [IngredientOut(IngredientId=row[0], IngredientName=row[1]) for row in rows]

def update_ingredient_db(ingredient_id: int, ingredient: IngredientUpdate) -> IngredientOut:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbl_Ingredients SET IngredientName = ? WHERE IngredientId = ?",
        (ingredient.IngredientName, ingredient_id),
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Ingredient not found")
    conn.commit()
    cursor.execute(
        "SELECT IngredientId, IngredientName FROM tbl_Ingredients WHERE IngredientId = ?",
        (ingredient_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return IngredientOut(IngredientId=row[0], IngredientName=row[1])

def delete_ingredient_db(ingredient_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tbl_Ingredients WHERE IngredientId = ?",
        (ingredient_id,),
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Ingredient not found")
    conn.commit()
    conn.close()
    return {"message": "Ingredient deleted successfully"}
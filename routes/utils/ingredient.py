from db import conn
from schemas.ingredient_schema import IngredientCreate, IngredientUpdate

def create_ingredient_db(ingredient: IngredientCreate):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tbl_Ingredients (IngredientName) OUTPUT INSERTED.IngredientId VALUES (?)",
        ingredient.IngredientName,
    )
    inserted_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {**ingredient.dict(), "IngredientId": inserted_id}

def get_ingredients_db(query: str):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT IngredientId, IngredientName FROM tbl_Ingredients WHERE IngredientName LIKE ?",
        f"%{query}%",
    )
    rows = cursor.fetchall()
    cursor.close()
    return [{"IngredientId": row[0], "IngredientName": row[1]} for row in rows]

def update_ingredient_db(ingredient_id: int, ingredient: IngredientUpdate):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tbl_Ingredients SET IngredientName = ? WHERE IngredientId = ?",
        ingredient.IngredientName, ingredient_id,
    )
    conn.commit()
    cursor.close()
    return {**ingredient.dict(), "IngredientId": ingredient_id}

def delete_ingredient_db(ingredient_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_Ingredients WHERE IngredientId = ?", ingredient_id)
    conn.commit()
    cursor.close()
    return {"message": "Ingredient deleted successfully"}

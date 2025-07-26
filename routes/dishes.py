from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from datetime import datetime
import pyodbc
import os

router = APIRouter(tags=["Dishes"])  # Prefix set in main.py

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=DESKTOP-648G0K0\\SQLEXPRESS01;'
        'DATABASE=food;'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )

@router.get("/")
def get_all_dishes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_Dishes")
    columns = [column[0] for column in cursor.description]
    dishes = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return dishes

@router.get("/{dish_id}")
def get_dish(dish_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_Dishes WHERE DishId = ?", (dish_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Dish not found")
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

@router.post("/dishes")
def create_dish(
    name: str = Form(...),
    description: str = Form(""),  # Default to empty string if not provided
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None),
    image_url: str = Form(None)
):
    image_url_to_use = image_url if image_url else None
    if image:
        os.makedirs("static/images", exist_ok=True)
        path = f"static/images/{image.filename}"
        with open(path, "wb") as f:
            f.write(image.file.read())
        image_url_to_use = f"http://localhost:8000/{path.replace(os.sep, '/')}"

    now = datetime.now()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tbl_Dishes (
            DishName, DishImageUrl, DishDescription,
            DishPrice, CategoryId, DishCreatedAt, DishUpdatedAt
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, image_url_to_use, description, price, category_id, now, now))
    conn.commit()

    cursor.execute("SELECT @@IDENTITY")
    dish_id = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM tbl_Dishes WHERE DishId = ?", (dish_id,))
    row = cursor.fetchone()
    conn.close()

    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

@router.put("/dishes/{dish_id}")
def update_dish(
    dish_id: int,
    name: str = Form(...),
    description: str = Form(""),  # Default to empty string if not provided
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None),
    image_url: str = Form(None)
):
    image_url_to_use = image_url if image_url else None
    if image:
        os.makedirs("static/images", exist_ok=True)
        path = f"static/images/{image.filename}"
        with open(path, "wb") as f:
            f.write(image.file.read())
        image_url_to_use = f"http://localhost:8000/{path.replace(os.sep, '/')}"

    conn = get_connection()
    cursor = conn.cursor()

    # Always check for existing image URL if none provided
    if not image_url_to_use and not image:
        cursor.execute("SELECT DishImageUrl FROM tbl_Dishes WHERE DishId = ?", (dish_id,))
        row = cursor.fetchone()
        if row:
            image_url_to_use = row[0]

    cursor.execute("""
        UPDATE tbl_Dishes SET
            DishName = ?,
            DishImageUrl = ?,
            DishDescription = ?,
            DishPrice = ?,
            CategoryId = ?,
            DishUpdatedAt = ?
        WHERE DishId = ?
    """, (name, image_url_to_use, description, price, category_id, datetime.now(), dish_id))
    conn.commit()
    conn.close()

    return {"message": "Dish updated successfully", "image_url": image_url_to_use}

@router.delete("/dishes/{dish_id}")
def delete_dish(dish_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_Dishes WHERE DishId = ?", (dish_id,))
    conn.commit()
    conn.close()
    return {"message": "Dish deleted successfully"}
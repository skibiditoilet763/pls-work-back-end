from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from datetime import datetime
import pyodbc
import os

router = APIRouter(prefix="/dishes", tags=["Dishes"])

def get_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost\\SQLEXPRESS;"
        "Database=food;"
        "Trusted_Connection=yes;"
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

@router.post("/")
def create_dish(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...)
):
    # Lưu ảnh vào thư mục static/images
    os.makedirs("static/images", exist_ok=True)
    path = f"static/images/{image.filename}"
    with open(path, "wb") as f:
        f.write(image.file.read())

    image_url = f"http://localhost:8000/{path.replace(os.sep, '/')}"
    now = datetime.now()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tbl_Dishes (
            DishName, DishImageUrl, DishDescription,
            DishPrice, CategoryId, DishCreatedAt, DishUpdatedAt
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, image_url, description, price, category_id, now, now))
    conn.commit()
    conn.close()

    return {"message": "Dish created successfully", "image_url": image_url}

@router.put("/{dish_id}")
def update_dish(
    dish_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None)
):
    # Nếu có ảnh mới thì lưu lại
    if image:
        os.makedirs("static/images", exist_ok=True)
        path = f"static/images/{image.filename}"
        with open(path, "wb") as f:
            f.write(image.file.read())
        image_url = f"http://localhost:8000/{path.replace(os.sep, '/')}"
    else:
        image_url = None

    conn = get_connection()
    cursor = conn.cursor()

    # Nếu không có ảnh mới thì lấy ảnh cũ
    if not image_url:
        cursor.execute("SELECT DishImageUrl FROM tbl_Dishes WHERE DishId = ?", (dish_id,))
        row = cursor.fetchone()
        if row:
            image_url = row[0]

    cursor.execute("""
        UPDATE tbl_Dishes SET
            DishName = ?,
            DishImageUrl = ?,
            DishDescription = ?,
            DishPrice = ?,
            CategoryId = ?,
            DishUpdatedAt = ?
        WHERE DishId = ?
    """, (name, image_url, description, price, category_id, datetime.now(), dish_id))
    conn.commit()
    conn.close()

    return {"message": "Dish updated successfully", "image_url": image_url}

@router.delete("/{dish_id}")
def delete_dish(dish_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_Dishes WHERE DishId = ?", (dish_id,))
    conn.commit()
    conn.close()
    return {"message": "Dish deleted successfully"}

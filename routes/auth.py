from fastapi import APIRouter, HTTPException
from schemas.account_schema import AccountCreate, AccountLogin
import pyodbc

router = APIRouter(tags=["Auth"])

# Hàm kết nối SQL Server bằng pyodbc (Windows Authentication)
def get_connection():
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost\\SQLEXPRESS;"
        "Database=food;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

@router.post("/register")
def register(data: AccountCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tbl_Accounts WHERE AccountUsername = ?", (data.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    cursor.execute("""
        INSERT INTO tbl_Accounts (AccountUsername, AccountPassword, AccountRole)
        VALUES (?, ?, ?)
    """, (data.username, data.password, data.role))
    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}

@router.post("/login")
def login(data: AccountLogin):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AccountId, AccountUsername, AccountRole
        FROM tbl_Accounts
        WHERE AccountUsername = ? AND AccountPassword = ?
    """, (data.username, data.password))

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "id": user[0],
        "username": user[1],
        "role": user[2],
        "message": "Login successful"
    }

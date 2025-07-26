from fastapi import APIRouter, HTTPException
from schemas.account_schema import AccountCreate, AccountLogin, AccountResponse, AccountUpdate
from routes.utils.auth import hash_password
import pyodbc

router = APIRouter(tags=["Auth"])

def get_connection():
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DESKTOP-648G0K0\\SQLEXPRESS01;"
        "Database=food;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

@router.post("/register", response_model=AccountResponse)
def register(data: AccountCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tbl_Accounts WHERE AccountUsername = ?", (data.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(data.password)
    cursor.execute(
        """
        INSERT INTO tbl_Accounts (AccountUsername, AccountPassword, AccountRole, Name, Address, PhoneNumber)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (data.username, hashed_password, data.role, data.name, data.address, data.phoneNumber)
    )
    conn.commit()

    cursor.execute("SELECT @@IDENTITY")
    account_id = cursor.fetchone()[0]
    cursor.execute(
        """
        SELECT AccountId, AccountUsername, AccountRole, Name, Address, PhoneNumber
        FROM tbl_Accounts
        WHERE AccountId = ?
        """,
        (account_id,)
    )
    user = cursor.fetchone()
    conn.close()

    return AccountResponse(
        id=user[0],
        username=user[1],
        role=user[2],
        name=user[3],
        address=user[4],
        phoneNumber=user[5]
    )

@router.post("/login", response_model=AccountResponse)
def login(data: AccountLogin):
    hashed_password = hash_password(data.password)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AccountId, AccountUsername, AccountRole, Name, Address, PhoneNumber
        FROM tbl_Accounts
        WHERE AccountUsername = ? AND AccountPassword = ?
        """,
        (data.username, hashed_password)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return AccountResponse(
        id=user[0],
        username=user[1],
        role=user[2],
        name=user[3],
        address=user[4],
        phoneNumber=user[5]
    )

@router.get("/profile/{account_id}", response_model=AccountResponse)
def get_profile(account_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AccountId, AccountUsername, AccountRole, Name, Address, PhoneNumber
        FROM tbl_Accounts
        WHERE AccountId = ?
        """,
        (account_id,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return AccountResponse(
        id=user[0],
        username=user[1],
        role=user[2],
        name=user[3],
        address=user[4],
        phoneNumber=user[5]
    )

@router.put("/profile/{account_id}", response_model=AccountResponse)
def update_profile(account_id: int, data: AccountUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(data.password)

    cursor.execute(
        """
        UPDATE tbl_Accounts
        SET Name = ?, AccountPassword = ?, Address = ?, PhoneNumber = ?
        WHERE AccountId = ?
        """,
        (data.name, hashed_password, data.address, data.phoneNumber, account_id)
    )
    conn.commit()

    cursor.execute(
        """
        SELECT AccountId, AccountUsername, AccountRole, Name, Address, PhoneNumber
        FROM tbl_Accounts
        WHERE AccountId = ?
        """,
        (account_id,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return AccountResponse(
        id=user[0],
        username=user[1],
        role=user[2],
        name=user[3],
        address=user[4],
        phoneNumber=user[5]
    )

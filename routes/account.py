
from fastapi import APIRouter, HTTPException
from schemas.account_schema import AccountCreate, AccountUpdate, AccountResponse
from routes.utils.account import update_account
from passlib.hash import bcrypt
from db import conn

router = APIRouter()

@router.post("/")
def create_user(data: AccountCreate):
    cursor = conn.cursor()
    try:
        hashed_password = bcrypt.hash(data.AccountPassword)
        cursor.execute(
            """
            INSERT INTO tbl_Accounts ([AccountUsername], [AccountPassword], [AccountRole], [PhoneNumber], [Address])
            VALUES (?, ?, ?, ?, ?)
            """,
            (data.AccountUsername, hashed_password, data.AccountRole, data.PhoneNumber, data.Address)
        )
        conn.commit()
        cursor.execute("SELECT @@IDENTITY AS id")
        account_id = cursor.fetchone()[0]
        cursor.execute(
            "SELECT [AccountId], [AccountUsername], [AccountRole], [PhoneNumber], [Address] FROM tbl_Accounts WHERE [AccountId] = ?",
            (account_id,)
        )
        row = cursor.fetchone()
        if row:
            # Explicitly cast PhoneNumber to string to match schema
            return {"AccountId": row[0], "AccountUsername": row[1], "AccountRole": row[2], "PhoneNumber": str(row[3]) if row[3] is not None else None, "Address": row[4]}
        else:
            raise HTTPException(status_code=500, detail="Insert succeeded but data not found in table")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
    finally:
        cursor.close()

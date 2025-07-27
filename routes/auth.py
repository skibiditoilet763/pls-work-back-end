
from fastapi import APIRouter, HTTPException
from schemas.account_schema import AccountCreate, AccountLogin, AccountResponse, AccountUpdate
from routes.utils.account import update_account
from passlib.hash import bcrypt
from db import conn

router = APIRouter()

@router.post("/register", response_model=AccountResponse)
def register(data: AccountCreate):
    cursor = conn.cursor()
    try:
        hashed_password = bcrypt.hash(data.AccountPassword)
        cursor.execute(
            """
            INSERT INTO tbl_Accounts (AccountUsername, AccountPassword, AccountRole, PhoneNumber, Address)
            VALUES (?, ?, ?, ?, ?)
            """,
            (data.AccountUsername, hashed_password, data.AccountRole, data.PhoneNumber, data.Address)
        )
        conn.commit()
        cursor.execute("SELECT @@IDENTITY AS id")
        account_id = cursor.fetchone()[0]
        cursor.execute(
            "SELECT AccountId, AccountUsername, AccountRole, PhoneNumber, Address FROM tbl_Accounts WHERE AccountId = ?",
            (account_id,)
        )
        row = cursor.fetchone()
        if row:
            # Explicitly cast PhoneNumber to string to match schema
            return {
                "AccountId": row[0],
                "AccountUsername": row[1],
                "AccountRole": row[2],
                "PhoneNumber": str(row[3]) if row[3] is not None else None,
                "Address": row[4]
            }
        raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
    finally:
        cursor.close()

@router.post("/login")
def login(data: AccountLogin):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT AccountPassword FROM tbl_Accounts WHERE AccountUsername = ?",
            (data.AccountUsername,)
        )
        row = cursor.fetchone()
        if row and bcrypt.verify(data.AccountPassword, row[0]):
            cursor.execute(
                "SELECT AccountId, AccountUsername, AccountRole, PhoneNumber, Address FROM tbl_Accounts WHERE AccountUsername = ?",
                (data.AccountUsername,)
            )
            user_row = cursor.fetchone()
            if user_row:
                # Explicitly cast PhoneNumber to string to match schema
                return {
                    "AccountId": user_row[0],
                    "AccountUsername": user_row[1],
                    "AccountRole": user_row[2],
                    "PhoneNumber": str(user_row[3]) if user_row[3] is not None else None,
                    "Address": user_row[4]
                }
        raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        cursor.close()
@router.get("/profile/{account_id}", response_model=AccountResponse)
def get_profile(account_id: int):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT AccountId, AccountUsername, AccountRole, PhoneNumber, Address FROM tbl_Accounts WHERE AccountId = ?",
            (account_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "AccountId": row[0],
                "AccountUsername": row[1],
                "AccountRole": row[2],
                "PhoneNumber": str(row[3]) if row[3] is not None else None,
                "Address": row[4]
            }
        raise HTTPException(status_code=404, detail="User not found")
    finally:
        cursor.close()
        
        
        
@router.put("/update/{account_id}")
def update_user(account_id: int, data: AccountUpdate):
    try:
        updated_data = update_account(account_id, data)
        if updated_data is None:
            raise HTTPException(status_code=404, detail="User not found or no updates applied")
        # Ensure PhoneNumber is a string to match AccountResponse schema
        updated_data["PhoneNumber"] = str(updated_data["PhoneNumber"]) if updated_data["PhoneNumber"] is not None else None
        return updated_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")




@router.delete("/delete")
def delete_user(account_id: int):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tbl_Accounts WHERE AccountId = ?", (account_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
    finally:
        cursor.close()
        
        
        
#admin shit:
from typing import List

@router.get("/users", response_model=List[AccountResponse])
def get_users():
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT AccountId, AccountUsername, AccountRole, PhoneNumber, Address FROM tbl_Accounts"
        )
        rows = cursor.fetchall()
        return [
            {
                "AccountId": row[0],
                "AccountUsername": row[1],
                "AccountRole": row[2],
                "PhoneNumber": str(row[3]) if row[3] is not None else None,
                "Address": row[4]
            }
            for row in rows
        ]
    finally:
        cursor.close()
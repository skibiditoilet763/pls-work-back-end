from db import conn
from schemas.account_schema import AccountUpdate
from passlib.hash import bcrypt

def update_account(account_id: int, data: AccountUpdate):
    hashed_password = bcrypt.hash(data.AccountPassword)

    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE tbl_Accounts
        SET AccountUsername = ?, AccountPassword = ?
        WHERE AccountId = ?
        """,
        data.AccountUsername, hashed_password, account_id
    )
    conn.commit()
    cursor.execute(
        "SELECT AccountId, AccountUsername FROM tbl_Accounts WHERE AccountId = ?",
        account_id,
    )
    row = cursor.fetchone()
    cursor.close()
    if row:
        return {"AccountId": row[0], "AccountUsername": row[1]}
    return None

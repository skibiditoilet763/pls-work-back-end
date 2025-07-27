
from db import conn
from schemas.account_schema import AccountUpdate
from passlib.hash import bcrypt

def update_account(account_id: int, data: AccountUpdate):
    cursor = conn.cursor()
    try:
        update_parts = []
        update_values = []

        if data.AccountUsername is not None:
            update_parts.append("[AccountUsername] = ?")
            update_values.append(data.AccountUsername)
        if data.AccountPassword is not None:
            hashed_password = bcrypt.hash(data.AccountPassword)
            update_parts.append("[AccountPassword] = ?")
            update_values.append(hashed_password)
        if data.AccountRole is not None:
            update_parts.append("[AccountRole] = ?")
            update_values.append(data.AccountRole)
        if data.PhoneNumber is not None:
            update_parts.append("[PhoneNumber] = ?")
            update_values.append(data.PhoneNumber)
        if data.Address is not None:
            update_parts.append("[Address] = ?")
            update_values.append(data.Address)

        if not update_parts:
            return None

        update_query = f"""
        UPDATE tbl_Accounts
        SET {', '.join(update_parts)}
        WHERE [AccountId] = ?
        """
        update_values.append(account_id)
        cursor.execute(update_query, update_values)
        conn.commit()

        cursor.execute(
            "SELECT [AccountId], [AccountUsername], [AccountRole], [PhoneNumber], [Address] FROM tbl_Accounts WHERE [AccountId] = ?",
            (account_id,)
        )
        row = cursor.fetchone()
        if row:
            # Explicitly cast PhoneNumber to string to match schema
            return {"AccountId": row[0], "AccountUsername": row[1], "AccountRole": row[2], "PhoneNumber": str(row[3]) if row[3] is not None else None, "Address": row[4]}
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
    return None

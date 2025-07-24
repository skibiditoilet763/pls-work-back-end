from fastapi import APIRouter, HTTPException
from schemas.account_schema import AccountUpdate, AccountOut
from utils.account import update_account

router = APIRouter()

@router.put("/{account_id}", response_model=AccountOut)
def update_user(account_id: int, data: AccountUpdate):
    result = update_account(account_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

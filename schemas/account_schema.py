from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    AccountUsername: str
    AccountPassword: str
    AccountRole: str  # Required to match your intent
    PhoneNumber: Optional[str] = None
    Address: Optional[str] = None

class AccountLogin(BaseModel):
    AccountUsername: str
    AccountPassword: str

class AccountUpdate(BaseModel):
    AccountUsername: Optional[str] = None
    AccountPassword: Optional[str] = None
    AccountRole: Optional[str] = None
    PhoneNumber: Optional[str] = None
    Address: Optional[str] = None

class AccountResponse(BaseModel):
    AccountId: int
    AccountUsername: str
    AccountRole: str
    PhoneNumber: Optional[str] = None
    Address: Optional[str] = None

    class Config:
        orm_mode = True
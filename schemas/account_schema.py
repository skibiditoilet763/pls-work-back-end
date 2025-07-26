from pydantic import BaseModel
from typing import Optional


class AccountCreate(BaseModel):
    username: str
    password: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None


class AccountLogin(BaseModel):
    username: str
    password: str


class AccountUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class AccountResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True

from pydantic import BaseModel

# Dùng cho tạo tài khoản (đăng ký)
class AccountCreate(BaseModel):
    username: str
    password: str
    role: str  # nếu có role, không có thì có thể bỏ đi

# Dùng cho đăng nhập
class AccountLogin(BaseModel):
    username: str
    password: str

# Dùng cho phản hồi ra bên ngoài (nếu cần)
class AccountOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

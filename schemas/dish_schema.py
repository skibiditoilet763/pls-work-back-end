from pydantic import BaseModel
from typing import Optional

class DishCreate(BaseModel):
    name: str
    image_url: Optional[str]
    description: Optional[str]
    price: float
    category_id: int

class DishUpdate(DishCreate):
    pass

class DishOut(BaseModel):
    id: int
    name: str
    image_url: Optional[str]
    description: Optional[str]
    price: float
    category_id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel

class IngredientCreate(BaseModel):
    IngredientName: str

    class Config:
        from_attributes = True  # Replaced orm_mode
        json_schema_extra = {
            "example": {"IngredientName": "Tomato"}
        }

class IngredientUpdate(BaseModel):
    IngredientName: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {"IngredientName": "Red Tomato"}
        }

class IngredientOut(BaseModel):
    IngredientId: int | None = None
    IngredientName: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {"IngredientId": 1, "IngredientName": "Tomato"}
        }
from typing import Optional, Any, Dict
from pydantic import BaseModel

class RecipeOut(BaseModel):
    id: int
    cuisine: Optional[str] = None
    title: Optional[str] = None
    rating: Optional[float] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    description: Optional[str] = None
    nutrients: Optional[Dict[str, Any]] = None
    serves: Optional[str] = None

    class Config:
        orm_mode = True

class PaginatedRecipes(BaseModel):
    page: int
    limit: int
    total: int
    data: list[RecipeOut]

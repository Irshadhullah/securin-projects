from fastapi import FastAPI, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from .db import get_db, engine, Base
from . import models, crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipes API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/recipes", response_model=schemas.PaginatedRecipes)
def list_recipes(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    total, rows = crud.get_recipes(db, page=page, limit=limit)
    return {"page": page, "limit": limit, "total": total, "data": rows}

@app.get("/api/recipes/search", response_model=schemas.PaginatedRecipes)
def search_recipes(title: Optional[str] = None, cuisine: Optional[str] = None, rating: Optional[str] = None, total_time: Optional[str] = None, calories: Optional[str] = None, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), sort_by: str = Query("rating", regex="^(rating|title|total_time)$"), order: str = Query("desc", regex="^(asc|desc)$"), db: Session = Depends(get_db)):
    total, rows = crud.search_recipes(db=db, page=page, limit=limit, title=title, cuisine=cuisine, rating=rating, total_time=total_time, calories=calories, sort_by=sort_by, order=order)
    return {"page": page, "limit": limit, "total": total, "data": rows}

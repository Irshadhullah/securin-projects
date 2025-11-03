import re
from typing import Optional, Tuple, Dict, Any
from sqlalchemy import select, func, text, desc, asc, and_
from sqlalchemy.orm import Session
from .models import Recipe

COMPARATOR_RE = re.compile(r"^(?P<op>>=|<=|=|>|<)?(?P<val>-?\d+(\.\d+)?)$")

def parse_comparator(s: str) -> Optional[Tuple[str, float]]:
    if s is None:
        return None
    s = s.strip()
    m = COMPARATOR_RE.match(s)
    if not m:
        return None
    op = m.group("op") or "="
    val = float(m.group("val"))
    return op, val

def to_int_or_null(v) -> Optional[int]:
    try:
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip().lower()
            if s in ("", "nan", "null"):
                return None
        return int(float(v))
    except Exception:
        return None

def create_recipe(db: Session, recipe_data: Dict[str, Any]) -> Recipe:
    r = Recipe(**recipe_data)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

def get_recipes(db: Session, page: int = 1, limit: int = 10):
    limit = min(limit, 100)
    offset = (page - 1) * limit
    stmt = select(Recipe).order_by(desc(Recipe.rating).nulls_last(), asc(Recipe.title)).limit(limit).offset(offset)
    total = db.execute(select(func.count()).select_from(Recipe)).scalar_one()
    rows = db.execute(stmt).scalars().all()
    return total, rows

def build_filters(title=None, cuisine=None, rating=None, total_time=None, calories=None):
    filters = []
    if title:
        filters.append(Recipe.title.ilike(f"%{{title}}%"))
    if cuisine:
        filters.append(Recipe.cuisine.ilike(f"%{{cuisine}}%"))
    if rating:
        parsed = parse_comparator(rating)
        if parsed:
            op, val = parsed
            if op == "=":
                filters.append(Recipe.rating == val)
            elif op == ">=":
                filters.append(Recipe.rating >= val)
            elif op == "<=":
                filters.append(Recipe.rating <= val)
            elif op == ">":
                filters.append(Recipe.rating > val)
            elif op == "<":
                filters.append(Recipe.rating < val)
    if total_time:
        parsed = parse_comparator(total_time)
        if parsed:
            op, val = parsed
            if op == "=":
                filters.append(Recipe.total_time == int(val))
            elif op == ">=":
                filters.append(Recipe.total_time >= int(val))
            elif op == "<=":
                filters.append(Recipe.total_time <= int(val))
            elif op == ">":
                filters.append(Recipe.total_time > int(val))
            elif op == "<":
                filters.append(Recipe.total_time < int(val))
    if calories:
        parsed = parse_comparator(calories)
        if parsed:
            op, val = parsed
            cal_expr = text("(NULLIF(regexp_replace((recipes.nutrients->>'calories')::text, '[^0-9]', '', 'g'), '')::int)")
            if op == "=":
                filters.append(cal_expr == int(val))
            elif op == ">=":
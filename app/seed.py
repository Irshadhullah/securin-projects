import json
import os
import re
from dotenv import load_dotenv
from .db import SessionLocal, engine, Base
from .models import Recipe
from .crud import to_int_or_null

load_dotenv()

Base.metadata.create_all(bind=engine)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "recipes.json")

def to_float_or_none(v):
    try:
        if v is None:
            return None
        if isinstance(v, str) and v.strip().lower() in ("", "nan", "null"):
            return None
        return float(v)
    except Exception:
        return None

def parse_calories(cal):
    if cal is None:
        return None
    if isinstance(cal, (int, float)):
        return int(cal)
    s = str(cal)
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

def sanitize_recipe(raw):
    title = raw.get("title") or raw.get("name") or None
    cuisine = raw.get("cuisine")
    rating = to_float_or_none(raw.get("rating"))
    prep_time = to_int_or_null(raw.get("prep_time") or raw.get("prepTime") or raw.get("prep"))
    cook_time = to_int_or_null(raw.get("cook_time") or raw.get("cookTime") or raw.get("cook"))
    total_time = to_int_or_null(raw.get("total_time") or raw.get("totalTime") or raw.get("total"))
    description = raw.get("description") or raw.get("instructions") or None
    serves = raw.get("serves") or raw.get("yield") or None
    nutrients = raw.get("nutrients") or raw.get("nutrition") or {}
    if not isinstance(nutrients, dict):
        nutrients = {"raw": nutrients}
    cal_raw = nutrients.get("calories") or nutrients.get("energy") or None
    cal_num = parse_calories(cal_raw) if cal_raw is not None else None
    if cal_raw is not None:
        nutrients["calories_raw"] = cal_raw
    if cal_num is not None:
        nutrients["calories_numeric"] = cal_num
    return {
        "title": title,
        "cuisine": cuisine,
        "rating": rating,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "total_time": total_time,
        "description": description,
        "nutrients": nutrients,
        "serves": serves,
    }

def load_data():
    if not os.path.exists(DATA_PATH):
        print("Data file not found:", DATA_PATH)
        return
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    records = raw if isinstance(raw, list) else raw.get("recipes", [])
    db = SessionLocal()
    inserted = 0
    for r in records:
        try:
            item = sanitize_recipe(r)
            rec = Recipe(**item)
            db.add(rec)
            db.commit()
            inserted += 1
        except Exception as e:
            db.rollback()
            print("Error:", e)
    db.close()
    print("Inserted", inserted)

if __name__ == "__main__":
    load_data()

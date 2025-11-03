from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from .db import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    cuisine = Column(String, index=True)
    title = Column(String, index=True)
    rating = Column(Float, index=True, nullable=True)
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=True)
    description = Column(Text)
    nutrients = Column(JSONB)
    serves = Column(String)
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())

from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Category

def get_categories(site_id, skip: int = 0, limit: int = 10):
    db = SessionLocal()
    return db.query(Category).filter(Category.site_id == site_id, Category.parent_code.isnot(None)).all()
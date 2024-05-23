from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Site

def get_sites(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    return db.query(Site).offset(skip).limit(limit).all()
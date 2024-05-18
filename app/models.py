from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(Integer)
    url = Column(String, unique=True, index=True)
    origin_url = Column(String)
    headline = Column(String)
    summary = Column(String)
    author = Column(String)
    body = Column(String)
    img_url = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    collected_at = Column(DateTime, default=datetime.now)

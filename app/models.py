from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()

article_category = Table(
    'article_category', Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)

class Site(Base):
    __tablename__ = "site"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="id")
    name = Column(String(50), nullable=False, comment="site 명")
    host = Column(String(50), nullable=False, comment="site host")
    base_url = Column(String(500), nullable=False, comment="scrap할 base url")
    
    categories = relationship("Category", back_populates="site")

class Category(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="id")
    code = Column(String(20), nullable=False, comment="코드")
    name = Column(String(100), nullable=False, comment="코드명")
    parent_code = Column(String(20), nullable=True, comment="상위 코드")
    site_id = Column(Integer, ForeignKey("site.id"), nullable=True, comment="site id")
    created_at = Column(DateTime, default=datetime.utcnow, comment="등록일")
    updated_at = Column(DateTime, nullable=True, comment="수정일")
    
    site = relationship("Site", back_populates="categories")
    articles = relationship("Article", secondary=article_category, back_populates="categories")

class Article(Base):
    __tablename__ = "article"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="id")
    url = Column(String(255), nullable=False, comment="기사 url")
    redirected_url = Column(String(255), nullable=False, comment="기사 redirect url")
    origin_url = Column(String(255), nullable=True, comment="기사 원본 url")
    headline = Column(String(500), nullable=False, comment="기사 제목")
    body = Column(String, nullable=False, comment="기사 본문")
    img_url = Column(String(500), nullable=True, comment="이미지 url")
    summary = Column(String(1000), nullable=True, comment="요약")
    author = Column(String(255), nullable=True, comment="기사 작성자")
    article_created_at = Column(String(255), nullable=True, comment="기사 생성일")
    article_updated_at = Column(String(255), nullable=True, comment="기사 수정일")
    collected_at = Column(DateTime, default=datetime.utcnow, comment="데이터 수집일")
    
    categories = relationship("Category", secondary=article_category, back_populates="articles")

    # def __str__(s):
    #     return "id: " + s.id + ", category_id: " + str(s.category_id) + ", url: " + s.url + ", origin_url: " + s.origin_url + ", headline: " + s.headline + ", body: " + s.body + ", img_url: " + s.img_url + ", summary: " + s.summary + ", author: " + s.author + ", article_created_at: " + s.article_created_at + ", article_updated_at: " + s.article_updated_at


class Channel(Base):
    __tablename__ = 'youtube_channels'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    channel_id = Column(String(50), unique=True, nullable=False)
    channel_title = Column(String(255), nullable=False)
    description = Column(String(1000))
    published_at = Column(DateTime)

    videos = relationship("ShortsVideo", back_populates="channel")

# Shorts 비디오 모델
class ShortsVideo(Base):
    __tablename__ = 'shorts_video'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    video_id = Column(String(50), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    published_at = Column(DateTime)
    view_count = Column(Integer)
    like_count = Column(Integer)
    comment_count = Column(Integer)
    thumbnail_url = Column(String(1000))
    tags = Column(String(5000))
    channel_id = Column(String(50), ForeignKey('youtube_channels.channel_id'), nullable=False)
    

    channel = relationship("Channel", back_populates="videos")
from sqlalchemy.orm import Session
from .models import Channel, ShortsVideo

def create_channel(db: Session, channel_id: str, channel_title: str):
    db_channel = Channel(channel_id=channel_id, channel_title=channel_title)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def create_shorts_video(db: Session, video_id: str, title: str, description: str, published_at: str,
                        view_count: int, like_count: int, comment_count: int, thumbnail_url: str, channel_id: str,
                        tags: str
                        ):
    db_video = ShortsVideo(
        video_id=video_id,
        title=title,
        description=description,
        published_at=published_at,
        view_count=view_count,
        like_count=like_count,
        comment_count=comment_count,
        thumbnail_url=thumbnail_url,
        channel_id=channel_id,
        tags=tags
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

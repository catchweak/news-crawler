-- https://commentpicker.com/youtube-channel-id.php
create table if not exists catch_weak.youtube_channels
(
    id            bigint auto_increment primary key comment 'id',
    channel_id    VARCHAR(50) UNIQUE NOT NULL comment '유튜브 채널 ID',
    channel_title VARCHAR(255)       NOT NULL comment '채널 이름',
    description   TEXT comment '채널 설명',
    published_at  TIMESTAMP comment '채널 생성 날짜'
);

CREATE TABLE if not exists catch_weak.shorts_video
(
    id            bigint auto_increment primary key comment 'id',
    video_id      VARCHAR(50)  NOT NULL COMMENT 'YouTube 비디오 ID',
    title         VARCHAR(255) NOT NULL COMMENT '비디오 제목',
    description   TEXT COMMENT '비디오 설명',
    published_at  DATETIME COMMENT '비디오 게시 날짜',
    view_count    INT COMMENT '조회수',
    like_count    INT COMMENT '좋아요 수',
    comment_count INT COMMENT '댓글 수',
    thumbnail_url TEXT COMMENT '썸네일 URL',
    channel_id    VARCHAR(50)  NOT NULL,
    tags          varchar(255) comment '태그',
    scraped_at datetime(6) default now() comment '데이터 수집일',
    FOREIGN KEY (channel_id) REFERENCES catch_weak.youtube_channels (channel_id)
);

-- ALTER TABLE catch_weak.shorts_video
-- ADD COLUMN tags TEXT COMMENT '비디오 태그';

-- CREATE TABLE IF NOT EXISTS catch_weak.tags (
--     id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Tag ID',
--     tag_name VARCHAR(255) UNIQUE NOT NULL COMMENT 'Tag Name'
-- );

-- CREATE TABLE IF NOT EXISTS catch_weak.video_tags (
--     video_id BIGINT NOT NULL COMMENT 'Video ID',
--     tag_id BIGINT NOT NULL COMMENT 'Tag ID',
--     PRIMARY KEY (video_id, tag_id),
--     FOREIGN KEY (video_id) REFERENCES catch_weak.shorts_video (id),
--     FOREIGN KEY (tag_id) REFERENCES catch_weak.tags (id)
-- );
create database if not exists catch_weak;

create table if not exists catch_weak.site
(
    id       bigint auto_increment primary key comment 'id',
    name     varchar(50) comment 'site 명',
    host     varchar(50) comment 'site host',
    base_url varchar(500) comment 'scrap할 base url'
);

insert into catch_weak.site(name, host, base_url) values('네이버', 'news.naver.com', 'https://news.naver.com/breakingnews/section');

create table if not exists catch_weak.category
(
    id          bigint auto_increment primary key comment 'id',
    code        varchar(20) not null comment '코드',
    name        varchar(100) comment '코드명',
    parent_code varchar(20) null comment '상위 코드',
    site_id     bigint comment 'site id',
    created_at  datetime(6) default now() comment '등록일',
    updated_at  datetime(6) comment '수정일',
    FOREIGN KEY (site_id) REFERENCES catch_weak.site (id)
);

insert into catch_weak.category(code, name, parent_code, site_id) values('100', '정치', null, 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('101', '경제', null, 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('102', '사회', null, 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('103', '생활/문화', null, 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('104', '세계', null, 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('105', 'IT/과학', null, 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('264', '대통령실', '100', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('265', '국회/정당', '100', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('266', '행정', '100', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('267', '국방/외교', '100', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('268', '북한', '100', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('269', '정치일반', '100', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('259', '금융', '101', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('258', '증권', '101', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('261', '산업/재계', '101', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('771', '중기/벤처', '101', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('260', '부동산', '101', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('262', '글로벌 경제', '101', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('310', '생활경제', '101', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('263', '경제 일반', '101', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('249', '사건사고', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('250', '교육', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('251', '노동', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('254', '언론', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('252', '환경', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('59b', '인권/복지', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('255', '식품/의료', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('256', '지역', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('276', '인물', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('257', '사회 일반', '102', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('241', '건강정보', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('239', '자동차/시승기', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('240', '도로/교통', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('237', '여행/레저', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('238', '음식/맛집', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('376', '패션/뷰티', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('242', '공연/전시', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('243', '책', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('244', '종교', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('248', '날씨', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('245', '생활문화 일반', '103', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('231', '아시아/호주', '104', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('232', '미국/중남미', '104', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('233', '유럽', '104', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('234', '중동/아프리카', '104', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('322', '세계 일반', '104', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('731', '모바일', '105', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('226', '인터넷/SNS', '105', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('227', '통신/뉴미디어', '105', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('230', 'IT 일반', '105', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('732', '보안/해킹', '105', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('283', '컴퓨터', '105', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('229', '게임/리뷰', '105', 1);
insert into catch_weak.category(code, name, parent_code, site_id) values('228', '과학 일반', '105', 1);


create table if not exists catch_weak.article
(
    id                 bigint auto_increment primary key comment 'id',
    category_id        bigint comment '카테고리 id',
    url                varchar(255) comment '기사 url',
    origin_url         varchar(255)  null comment '기사 원본 url',
    headline           varchar(500) comment '기사 제목',
    body               text comment '기사 본문',
    img_url            varchar(500)  null comment '이미지 url',
    summary            varchar(1000) null comment '요약',
    author             varchar(255)  null comment '기사 작성자',
    article_created_at varchar(255)  null comment '기사 생성일',
    article_updated_at varchar(255)  null comment '기사 수정일',
    collected_at       datetime(6) default now() comment '데이터 수집일',
    FOREIGN KEY (category_id) REFERENCES catch_weak.category (id)
);
create dabase if not exists catch_weak;

create table if not exists catch_weak.article
(
    id           bigint auto_increment primary key,
    category     int,
    url          varchar(255),
    origin_url   varchar(255)  null,
    headline     varchar(500),
    body         text,
    img_url      varchar(500),
    summary      varchar(1000) null,
    author       varchar(255)  null,
    created_at   varchar(255)  null,
    updated_at   varchar(255)  null,
    collected_at datetime(6) default now()
);

create table if not exists category
(
    id          bigint auto_increment primary key,
    code        int,
    name        varchar(100),
    parent_code int,
    created_at  datetime(6) default now(),
    updated_at  datetime(6)
);
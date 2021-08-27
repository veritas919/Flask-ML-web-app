create table publications
(
    id          int auto_increment
        primary key,
    type        varchar(20)               not null,
    title       varchar(400) charset utf8 null,
    abstract    text                      null,
    booktitle   varchar(400) charset utf8 null,
    pages       varchar(400) charset utf8 null,
    year        int                       null,
    address     varchar(400) charset utf8 null,
    journal     varchar(400) charset utf8 null,
    volume      int                       null,
    number      int                       null,
    month       varchar(16) charset utf8  null,
    url         varchar(400) charset utf8 null,
    ee          varchar(120) charset utf8 null,
    cdrom       varchar(40) charset utf8  null,
    cite        varchar(200) charset utf8 null,
    publisher   varchar(100) charset utf8 null,
    note        varchar(40) charset utf8  null,
    crossref    varchar(100) charset utf8 null,
    isbn        varchar(20) charset utf8  null,
    series      varchar(40) charset utf8  null,
    school      varchar(100) charset utf8 null,
    chapter     int                       null,
    publnr      varchar(100) charset utf8 null,
    series_href varchar(40) charset utf8  null,
    mdate       date                      null,
    `key`       varchar(40) charset utf8  null,
    ee_type     varchar(20)               null
);

create table authors
(
    id             int auto_increment
        primary key,
    publication_id int                      not null,
    name           varchar(40) charset utf8 null,
    orcid          varchar(40) charset utf8 null,
    constraint authors_ibfk_1
        foreign key (publication_id) references publications (id)
);

create index publication_id
    on authors (publication_id);

create table topics
(
    id              int auto_increment
        primary key,
    publication_id  int   not null,
    topic1          float null,
    topic2          float null,
    topic3          float null,
    topic4          float null,
    topic5          float null,
    topic6          float null,
    topic7          float null,
    topic8          float null,
    topic9          float null,
    topic10         float null,
    predicted_topic int   null,
    constraint topics_ibfk_1
        foreign key (publication_id) references publications (id)
);

create index publication_id
    on topics (publication_id);


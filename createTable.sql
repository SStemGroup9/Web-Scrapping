DROP TABLE IF EXISTS fb_page;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS author;

CREATE TABLE fb_page (
    page_id varchar(20) NOT NULL,
    name varchar(30) NOT NULL,
    fans INTEGER NOT NULL,
    shares INTEGER NOT NULL,
    url varchar(255) NOT NULL,
    PRIMARY KEY(page_id)
    );

CREATE TABLE posts(
    page_id varchar(255) NOT NULL,
    post_id varchar(255) NOT NULL,
    post_date varchar(255) NOT NULL,
    message varchar(255) NOT NULL,
    num_comments int(10) NOT NULL,
    num_likes int(255) NOT NULL,
    num_shares int(255) NOT NULL,
    FOREIGN KEY(page_id) REFERENCES fb_page(page_id)
    );

CREATE TABLE comments(
    post_id varchar(20) NOT NULL,
    comment_id varchar(2) NOT NULL,
    author_id int(10) NOT NULL,
    com_date varchar(20) NOT NULL,
    message varchar(255) NOT NULL,
    num_likes int(10) NOT NULL,
    PRIMARY KEY(comment_id),
    FOREIGN KEY(post_id) REFERENCES posts(post_id)
    );

CREATE TABLE author(
    author_id varchar(20) NOT NULL,
    fName varchar(100) NOT NULL,
    lName varchar(100) NOT NULL,
    gender varchar(20) NOT NULL,
    location varchar(20) NOT NULL,
    FOREIGN KEY(author_id) REFERENCES comments(comment_id)
    );

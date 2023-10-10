CREATE DATABASE youtube;

USE youtube;

CREATE TABLE Channel (
channel_id VARCHAR(255),
channel_name VARCHAR(255),
channel_views INT,
channel_description TEXT,
channel_status VARCHAR(255),
primary key (channel_id)
);

CREATE TABLE Playlist(
playlist_id VARCHAR(255),
channel_id VARCHAR(255),
playlist_name VARCHAR(255),
primary key (playlist_id),
FOREIGN KEY (channel_id) REFERENCES Channel(channel_id)
);

CREATE TABLE Video(
video_id VARCHAR(255),
playlist_id VARCHAR(255),
video_name VARCHAR(255),
video_description TEXT,
published_date VARCHAR(255),
view_count INT,
like_count INT,
dislike_count INT,
favorite_count INT,
comment_count INT,
duration INT,
thumbnail VARCHAR(255),
caption_status VARCHAR(255),
channel_name VARCHAR(255),
primary key (video_id),
FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id)
);

CREATE TABLE Comment(
comment_id VARCHAR(255),
video_id VARCHAR(255),
comment_text TEXT,
comment_author VARCHAR(255),
comment_published_date VARCHAR(255),
primary key (comment_id),
FOREIGN KEY (video_id) REFERENCES Video(video_id)
);

DESC channel;

CREATE DATABASE IF NOT EXISTS strokes;

USE strokes;

CREATE TABLE IF NOT EXISTS users (
  user_id INT NOT NULL AUTO_INCREMENT,
  user_name varchar(128) NOT NULL DEFAULT '',
  user_role varchar(128) NOT NULL DEFAULT '',
  user_password BLOB NOT NULL,
  PRIMARY KEY (user_id)
);

INSERT INTO users(user_name, user_role, user_password) VALUES('admin', 'admin', AES_ENCRYPT('4dm1N', 'strokes'));
INSERT INTO users(user_name, user_role, user_password) VALUES('alice', 'user', AES_ENCRYPT('wonderland', 'strokes'));
INSERT INTO users(user_name, user_role, user_password) VALUES('bob', 'user', AES_ENCRYPT('builder', 'strokes'));
INSERT INTO users(user_name, user_role, user_password) VALUES('clementine', 'user', AES_ENCRYPT('mandarine', 'strokes'));
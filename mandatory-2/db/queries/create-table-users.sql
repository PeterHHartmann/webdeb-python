DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id     TEXT UNIQUE NOT NULL,
    user_name   TEXT UNIQUE NOT NULL,
    user_email  TEXT UNIQUE NOT NULL,
    user_pwd    TEXT NOT NULL,
    PRIMARY KEY(user_id)
) without ROWID;

INSERT INTO users(user_id, user_name, user_email, user_pwd) 
VALUES('308e0166-6676-4185-9422-20a09abc22c1', 'Tom', 'test@email.com', '$2b$12$r1XwsYlYdoqf7GC3i256aOajRcJ3AbWlUOPUJuERhJVUExKzH9Hq6');

SELECT * FROM users;
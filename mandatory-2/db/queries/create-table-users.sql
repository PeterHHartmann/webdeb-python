DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id     INTEGER NOT NULL,
    user_name   TEXT UNIQUE NOT NULL,
    user_email  TEXT UNIQUE NOT NULL,
    user_pwd    TEXT NOT NULL,
    PRIMARY KEY(user_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS email_validations;
CREATE TABLE email_validations (
	validation_id	        INTEGER NOT NULL,
	user_email	            TEXT UNIQUE NOT NULL,
    validation_url          TEXT UNIQUE NOT NULL,
	validation_code	        INTEGER NOT NULL,
	CONSTRAINT fk_user_email FOREIGN KEY (user_email) REFERENCES users(user_email),
	PRIMARY KEY (validation_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS user_settings;
CREATE TABLE user_settings (
    settings_id         INTEGER NOT NULL,
    user_id             TEXT UNIQUE NOT NULL,
    user_displayname    TEXT NOT NULL,
    user_pfp            BLOB NOT NULL,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(user_id),
    PRIMARY KEY (settings_id AUTOINCREMENT)
);

-- ALTER TABLE users
-- ADD FOREIGN KEY (user_id) REFERENCES confirmations(user_id)

INSERT INTO users(user_name, user_email, user_pwd) 
VALUES('Tom', 'test@email.com', '$2b$12$r1XwsYlYdoqf7GC3i256aOajRcJ3AbWlUOPUJuERhJVUExKzH9Hq6');

SELECT * FROM users;
SELECT * from email_validations;

-- SELECT users.user_id, users.user_name, users.user_email, users.user_pwd, email_validations.validation_url, email_validations.validation_code
-- FROM users
-- INNER JOIN email_validations ON email_validations.user_id=users.user_id WHERE validation_url="dd12293c-a47d-4541-bc97-4de2e1e544c6";
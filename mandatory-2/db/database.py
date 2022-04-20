import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def user_get(user):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.row_factory = dict_factory
        user = json.dumps(db.execute('SELECT * FROM users WHERE user_email=:user_email', user).fetchall()[0])
        return user
    finally:
        db.close()

def user_post(user, validation):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.execute('INSERT INTO users(user_name, user_email, user_pwd) VALUES(:user_name, :user_email, :user_pwd)', user)
        db.execute('INSERT INTO email_validations(user_email, validation_url, validation_code) VALUES(:user_email, :validation_url, :validation_code)', dict(user_email=user['user_email'], validation_url=validation['url_snippet'], validation_code=validation['code']))
        db.commit()
    finally:
        db.close()

def validation_get_by_url(url):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.row_factory = dict_factory
        validation = json.dumps(db.execute(
            '''
            SELECT 
                users.user_id, 
                users.user_name,
                users.user_email,
                email_validations.validation_url, 
                email_validations.validation_code
            FROM users
            INNER JOIN email_validations 
            ON email_validations.user_email=users.user_email
            WHERE validation_url=:validation_url;
            ''', dict(validation_url=url)).fetchone())
        return validation
    finally:
        db.close()

def validation_get_by_email(email):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.row_factory = dict_factory
        validation = json.dumps(db.execute(
            '''
            SELECT 
                users.user_id, 
                users.user_name,
                users.user_email,
                email_validations.validation_url, 
                email_validations.validation_code
            FROM users
            INNER JOIN email_validations 
            ON email_validations.user_email=users.user_email 
            WHERE users.user_email=?;
            ''', (email,)).fetchone())
        return validation
    finally:
        db.close()

# TODO less complex SQL query without including the user might be better
def validation_update_code(email, new_code):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.execute(
            '''
            UPDATE email_validations
            SET validation_code=:validation_code
            WHERE user_email IN (
                SELECT e.user_email FROM email_validations e
                INNER JOIN users u 
                ON (e.user_email=u.user_email)
                WHERE u.user_email=:email
            );
            ''', dict(email=email, validation_code=new_code))

        db.commit()
    finally:
        db.close()


def validation_delete(user):
    print(user)
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.execute(
            '''
            DELETE FROM email_validations
            WHERE user_email IN (
                SELECT e.user_email FROM email_validations e
                INNER JOIN users u 
                ON (e.user_email=u.user_email)
                WHERE u.user_email=:user_email
            );
            ''', user)
        db.commit()
    finally:
        db.close()
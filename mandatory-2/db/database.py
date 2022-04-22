import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def user_get_by_email(user_email):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.row_factory = dict_factory
        user = json.dumps(db.execute('SELECT * FROM users WHERE user_email=:user_email', dict(user_email=user_email)).fetchone())
        return json.loads(user)
    finally:
        db.close()

def user_get_by_username(user_name):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.row_factory = dict_factory
        user = json.dumps(db.execute('SELECT * FROM users WHERE user_name=:user_name', dict(user_name=user_name)).fetchone())
        return json.loads(user)
    finally:
        db.close()

def user_post(user, validation, details):
    try:
        db = sqlite3.connect('db/database.sqlite')
        cursor = db.cursor()
        cursor.execute('INSERT INTO users(user_name, user_email, user_pwd) VALUES(:user_name, :user_email, :user_pwd)', user)
        cursor.execute('INSERT INTO email_validations(user_email, validation_url, validation_code) VALUES(:user_email, :validation_url, :validation_code)', dict(user_email=user['user_email'], validation_url=validation['url_snippet'], validation_code=validation['code']))
        cursor.execute('INSERT INTO user_details(user_name, display_name) VALUES(:user_name, :display_name)', dict(user_name=user['user_name'], display_name=details['display_name']))
        last_id = cursor.lastrowid
        print(last_id)
        cursor.execute('INSERT INTO joined_dates(detail_id, joined_month, joined_year) VALUES(:detail_id, :joined_month, :joined_year)', dict(detail_id=cursor.lastrowid, joined_month=details['joined_month'], joined_year=details['joined_year']))
        db.commit()
    finally:
        db.close()

def details_get(user_name):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.row_factory = dict_factory
        details = json.dumps(db.execute('''
            SELECT user_details.user_name, user_details.display_name, user_details.bio, joined_dates.joined_year, joined_dates.joined_month
            FROM user_details
            INNER JOIN joined_dates
            ON joined_dates.detail_id=user_details.detail_id
            WHERE user_details.user_name=:user_name
            ''', dict(user_name=user_name)).fetchone())
        return json.loads(details)
    finally:
        db.close()

def details_get_images(user_name):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.row_factory = dict_factory
        details = db.execute('''
            SELECT user_details.pfp, user_details.banner
            FROM user_details
            INNER JOIN joined_dates
            ON joined_dates.detail_id=user_details.detail_id
            WHERE user_details.user_name=:user_name
            ''', dict(user_name=user_name)).fetchone()
        return details
    finally:
        db.close()

def details_update(user_name, details):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.execute('''
            UPDATE user_details
            SET 
            display_name=:display_name, 
            bio=:bio, 
            pfp=:pfp,
            banner=:banner
            WHERE user_name=:user_name;
            ''', dict(user_name=user_name, **details))
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
        return json.loads(validation)
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
        return json.loads(validation)
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
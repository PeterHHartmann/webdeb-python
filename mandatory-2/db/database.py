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
        user = json.dumps(db.execute('SELECT * FROM users WHERE user_email=:user_email', user).fetchall())
        return user
    finally:
        db.close()

def user_post(user):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.execute('INSERT INTO users VALUES(:user_id, :user_name, :user_email, :user_pwd)', user)
        db.commit()
    finally:
        db.close()
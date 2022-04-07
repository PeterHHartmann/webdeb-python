import sqlite3;

def users_post(user):
    try:
        db = sqlite3.connect('db/database.sqlite')
        db.execute('INSERT INTO users VALUES(:user_id, :user_name, :user_email, :user_pwd)', user)
        db.commit()
    except Exception as ex:
        print(ex)
        raise
    finally:
        db.close()
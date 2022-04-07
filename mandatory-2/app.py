from encodings import utf_8
from uuid import uuid4
from bottle import error, get, post, redirect, request, response, run, static_file, view
import g
import re
import json
import bcrypt

import db.database as db

### static file routes
@get('/app.css')
def _():
    return static_file('app.css', root='style')

@get('/index.js')
def _():
    return static_file('index.js', root='js')

### views
@get('/')
@view('index')
def _():
    return

@post('/signup')
def _():
    user_id = str(uuid4())
    data = json.load(request.body)
    user_name = data.get('username')

    user_email = data.get('email')
    if not re.match(g.REGEX_EMAIL, user_email):
        response.status = 400
        return dict(msg='Please enter a valid email')
    user_pwd = data.get('pwd')
    if len(user_pwd) < 6 or len(user_pwd) > 20:
        response.status = 400
        return dict(msg='Password must be longer than 6 or shorter than 20 characters')

    #TODO hash password
    try:
        db.users_post(
                dict(
                    user_id=user_id,
                    user_name=user_name,
                    user_email=user_email,
                    user_pwd=user_pwd
                )
            )
    except Exception as e:
        print(e)
        response.status = 400
        if str(e) == 'UNIQUE constraint failed: users.user_name':
            return dict(msg='username is taken')
        elif str(e) == 'UNIQUE constraint failed: users.user_email':
            return dict(msg='email is taken')

    return dict(
                    user_name=user_name,
                    user_email=user_email,
                )

@post("/login")
def _():
    # VALIDATE
    # FIRST THING: Always check if the vriable was passed in the form
    if not request.forms.get('user_email'):
        return redirect('/login?error=user_email')    
    if not re.match(g.REGEX_EMAIL, request.forms.get('user_email')):
        return redirect('/login?error=user_email')

    user_email = request.forms.get('user_email')

    # FIRST THING: Always check if the variable was passed in the form
    if not request.forms.get('user_password'):
        return redirect(f'/login?error=user_password&user_email={user_email}')
    if len(request.forms.get("user_password")) < 6:
        return redirect(f'/login?error=user_password&user_email={user_email}')
    if len(request.forms.get("user_password")) > 50:
        return redirect(f'/login?error=user_password&user_email={user_email}')

    password = request.forms.get('user_password')

    for user in g.USERS:
        if user['email'] == user_email:
            if user['password'] == password:
                # do JWT here
                return redirect(f'/login-ok?user-name={user["name"]}')

    return redirect("/login")

@error(404)
@view('404')
def _(error):
    print(error)
    return

### API
@post('/delete-item')
def _():
    item_id = request.forms['item_id']
    for index, item in enumerate(g.ITEMS):
        if item['id'] == item_id:
            g.ITEMS.pop(index)
            return redirect('/items')
    return redirect('/items')


run(host='127.0.0.1', port=3334, debug=True, reloader=True)
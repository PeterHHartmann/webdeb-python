
from uuid import uuid4
from bottle import error, get, post, redirect, request, response, run, static_file, view, TEMPLATE_PATH
import g
import re
import json
import bcrypt
import jwt
import db.database as db

TEMPLATE_PATH.insert(0, 'public/views')

### static file routes
@get('/style/<stylesheet_name>')
def _(stylesheet_name):
    return static_file(stylesheet_name, root='public/style')

@get('/js/<script_name>')
def _(script_name):
    return static_file(script_name, root='public/javascript')

@get('/images/<image_name>')
def _(image_name):
    return static_file(image_name, root='public/image')

### views
@get('/')
@view('index')
def _():
    try:
        cookie = json.loads(request.get_cookie("JWT", secret="secret_info"))
        data = jwt.decode(cookie, key="secret_jwt", algorithms=["HS256"])
        print(data)
        return data
    except:
        return redirect('/login')

@get('/signup')
@view('signup')
def _():
    try:
        cookie = json.loads(request.get_cookie("JWT", secret="secret_info"))
        if cookie:
            return redirect('/')
    except: 
        return

@post('/signup')
def _():
    user_id = str(uuid4())
    data = json.load(request.body)
    user_name = data.get('username')
    if len(user_name.strip()) < 1:
        response.status = 400
        return dict(msg='Please enter a username')

    user_email = data.get('email')
    if not re.match(g.REGEX_EMAIL, user_email):
        response.status = 400
        return dict(msg='Please enter a valid email')
    user_pwd = data.get('pwd')
    if len(user_pwd) < 6 or len(user_pwd) > 20:
        response.status = 400
        return dict(msg='Password must be longer than 6 or shorter than 20 characters')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(user_pwd, 'utf_8'), salt)

    #TODO send confirmation email

    try:
        db.user_post(
                dict(
                    user_id=user_id,
                    user_name=user_name,
                    user_email=user_email,
                    user_pwd=hashed
                )
            )
    except Exception as e:
        print(e)
        response.status = 400
        if str(e) == 'UNIQUE constraint failed: users.user_name':
            return dict(msg='That username is taken')
        elif str(e) == 'UNIQUE constraint failed: users.user_email':
            return dict(msg='That email is already in use')

    return dict(
                    user_name=user_name,
                    user_email=user_email,
                )

@get('/login')
@view('login')
def _():
    try:
        cookie = json.loads(request.get_cookie("JWT", secret="secret_info"))
        if cookie:
            return redirect('/')
    except: 
        return

@post('/login')
def _():
    data = json.load(request.body)
    input_email = data.get('email')
    if not input_email or len(input_email.strip()) < 1:
        response.status = 400
        return dict(msg='Please enter an email')
    if not re.match(g.REGEX_EMAIL, input_email):
        response.status = 400
        return dict(msg='Please enter a valid email')

    input_pwd = data.get('pwd')
    if not input_pwd or len(input_pwd.strip()) < 1:
        response.status = 400
        return dict(msg='Please enter a password')

    # try:
    result = json.loads(db.user_get(dict(user_email=input_email)))
    if result:
        if not bcrypt.checkpw(bytes(input_pwd, 'utf-8'), bytes(result[0].get('user_pwd'), 'utf-8')):
            response.status = 401
            return dict(msg='Invalid email or password')
        else:
            payload = {
                "user_name": result[0].get('user_name'),
                "user_email": result[0].get('user_email')
            }
            encoded_jwt = jwt.encode(payload, "secret_jwt", algorithm="HS256")
            print(encoded_jwt)
            cookie_opts = {'max_age': 3600 * 24 * 3}
            response.set_cookie("JWT", json.dumps(encoded_jwt), "secret_info", **cookie_opts)
            return
    else:
        print("didn't find user")
        response.status = 401
        return dict(msg='Invalid email or password')

@get('/logout')
def _():
    response.delete_cookie("JWT", secret="secret_info")
    return redirect('/login')


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
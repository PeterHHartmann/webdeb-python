from uuid import uuid4
from bottle import error, get, post, redirect, request, response, run, static_file, view
import g
import re

### static file routes
@get('/app.css')
def _():
    return static_file('app.css', root='style')

### views
@get('/')
@view('index')
def _():
    return

@get('/users')
@view('users')
def _():
    return dict(users=g.USERS)

@get('/items')
@view('items')
def _():
    return dict(items=g.ITEMS)

@get('/signup')
@view('signup')
def _():
    return

@post('/signup')
def _():
    user_id = str(uuid4())
    user_email = request.forms.get('user_email')
    if not re.match(g.REGEX_EMAIL, user_email):
        return redirect('/lol')

    user_name = request.forms.get('user_name')
    password = request.forms.get('password')
    user = {'id': user_id, 'email' :user_email, 'name': user_name, 'password': password}
    g.USERS.append(user)
    return redirect(f'/signup-ok?user-email={user_email}&user-name={user_name}')

@get('/signup-ok') 
@view('signup-ok')
def _():
  user_email = request.params.get('user-email')
  user_name = request.params.get('user-name')
  return dict(user_email=user_email, user_name=user_name)

@get('/login')
@view('login')
def _():
    error = request.params.get('error')
    user_email = request.params.get('user_email')
    return dict(error=error, user_email=user_email)

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

@get('/login-ok') 
@view('login-ok')
def _():
  user_name = request.params.get('user-name')
  return dict(user_name=user_name)

@error(404)
@view('404')
def _(error):
    print(error)
    return

### API
@post('/delete-item')
def _():
    item_id = request.forms['item_id']
    for index, item in enumerate(items):
        if item['id'] == item_id:
            items.pop(index)
            return redirect('/items')
    return redirect('/items')


run(host='127.0.0.1', port=3334, debug=True, reloader=True, server='paste')
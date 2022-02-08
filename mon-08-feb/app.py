from uuid import uuid4
from bottle import error, get, post, redirect, request, response, run, static_file, view

items = [
    {
        'id':'362164d0-028c-433e-8e6f-8043524951db', 
        'name':'a', 
        'price':10
    },
    {
        'id':'4b51f6ee-a58f-41d1-b69b-cc2244e6f278', 
        'name':'b', 
        'price':20
    },
    {
        'id':'89a30b7b-24da-4085-852c-ab787de3cfd7', 
        'name':'c', 
        'price':30
    }
]

users = []

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
    return dict(users=users)

@get('/items')
@view('items')
def _():
    return dict(items=items)

@get('/signup')
@view('signup')
def _():
    return

@get('/login')
@view('login')
def _():
    return

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

@post('/signup-user')
def _():
    user_id = str(uuid4())
    user_email = request.forms['user_email']
    users.append({'id': user_id, 'email': user_email})
    return redirect('/users')


run(host='127.0.0.1', port=3333, debug=True, reloader=True, server='paste')
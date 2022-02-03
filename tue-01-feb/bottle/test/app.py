from bottle import get, run, static_file, view

# dictionary
person = {
    'name': 'Peter'
}

###########################
@get('/person')
def _():
    return person

###########################
@get('/app.css')
def _():
    return static_file('app.css', root='.')

###########################
@get('/')
@view('index')
def show_index_page():
    return

###########################
@get('/items')
@view('items')
def show_items_page():
    letters = ['a', 'c', 'x']
    letters.pop()
    return 'yes' if 'x' in letters else 'no'

###########################
@get('/item')
def show_item_page():
    name = 'Peter' # string - text
    year = 2022
    # return str(year) # type-cast or cast
    # return 'Hi ' + name + ' it is ' + str(year)
    return f'Hi {name} it is {year}' # f string

###########################
@get('/my-data/<first_name>/<last_name>')
def _(first_name, last_name):
    return f'Hi {first_name} {last_name}.'

###########################
run(host='127.0.0.1', port=3333, reloader=True, debug=True)
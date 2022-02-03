from bottle import run, get, post, delete, response, request
import json
import uuid;

#####################################
items = [
    {'id': '1', 'name': 'a'},
    {'id': '2', 'name': 'b'},
    {'id': '3', 'name': 'c'}
]

#####################################
@get('/')
def _():
    return 'Hi'

#####################################
@get('/items')
def _():
    # response.status = 500
    # return str(items)
    return json.dumps(items)

#####################################
@get('/test')
def _():
    year = request.params['year']
    school_name = request.params['school-name']
    age = request.params['age']

    # alternatively
    # year = request.query['year']
    # school_name = request.query['school-name']
    # age = request.query['age']

    response_text = f'Hi you are at {school_name}. The year is {year} and you are {age} years old'
    return response_text

#####################################
@get('/friendly/brand/<brand_name>/color/<color>')
def _(brand_name, color):
    return f'You want for brand: {brand_name} and the color is: {color}'

#####################################
@post('/greeting')
def _():
    first_name = request.forms.get('first_name')
    last_name = request.forms.get('last_name')
    return f'Hi {first_name} {last_name}'

#####################################
# @post('/items')
# def _():
#     try:
#         item_id = str(uuid.uuid4())
#         item_name = request.forms['item_name'].trim()
#         item_price = int(request.forms['item_price'])
#         item = {'id': item_id, 'name': item_name, 'price': item_price}
#         items.append(item)
#         return item_id
#     except KeyError as key:
#         response.status = 422
#         return f'Cannot process request'

@post('/items')
def _():
    if not request.forms.get('item_name'):
        response.status = 422
        return 'item_name is missing'
    elif len(request.forms.get('item_name')) < 2:
        response.status = 422
        return 'item_name must be at least 2 character'
    else:
        item_name = request.forms.get('item_name')

    if not request.forms.get('item_price'):
        response.status = 422
        return 'item_price is missing'
    elif int(request.forms.get('item_price')) < 20:
        response.status = 422
        return 'item_price must be at least 20'
    else:
        item_price = int(request.forms.get('item_price'))
    item_id = str(uuid.uuid4())
    item = {'id': item_id, 'name': item_name, 'price': item_price}
    items.append(item)
    return item_id

#####################################
@get('/items/<item_id>')
def _(item_id):
    if not item_id:
        response.status = 400
        return 'item_id is missing'
    for item in items:
        if item["id"] == item_id:
            return json.dumps(item)
    response.status = 400
    return 'item not found'

#####################################
@delete('/items/<item_id>')
def _(item_id):
    if not item_id:
        response.status = 400
        return 'item_id is missing'
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return f'item {item_id} has been deleted'
    response.status = 400
    return 'item not found'

#####################################
run(host='127.0.0.1', port=4444, debug=True, reloader=True)
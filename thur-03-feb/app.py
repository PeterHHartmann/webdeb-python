from bottle import run, get

#####################################

@get('/')
def _():
    return

#####################################

run(host='127.0.0.1', port=4444, debug=True, reloader=True)
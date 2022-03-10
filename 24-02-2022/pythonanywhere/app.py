from email.mime import application
from bottle import default_app, get, run, view, static_file

@get('/static/app.css')
def _():
    return static_file('app.css', root='style')

@get('/')
@view('index')
def _():
    return dict()

@get('/about')
@view('about')
def _():
    return

@get('/contact')
@view('contact')
def _():
    return

try:
    import production
    application = default_app()
except:
    run(host='127.0.0.1', port=3333, debug=True, reloader=True, server='paste')
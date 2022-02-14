from bottle import error, get, post, redirect, request, run, static_file, view

@get('/app.css')
def _():
    return static_file('app.css', root='style')

@error(404)
@view("404")
def _(error):
    print(error)
    return

##############################
run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
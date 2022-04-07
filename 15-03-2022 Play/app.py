from bottle import default_app, get, run


##############################
@get("/")
def _():
  return "x"

##############################



##############################
try:
  import production
  application = default_app()
except Exception as ex:
  print("Server running on development")
  run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
from wsgiref.simple_server import make_server
from APP import application
from app_cors import Http_split


app = Http_split(application.login)
server = make_server('localhost', 8080, app)
server.serve_forever()

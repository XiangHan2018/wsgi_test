from wsgiref.simple_server import make_server


def app(env, start_response):
    body = 'test_2'
    strat = '200 ok'
    print(env['REQUEST_URI'])
    harders = [('Content-Type', 'text/plain'),
               ('Content-Length', str(len(body)))]
    start_response(strat, harders)
    return [body]


server = make_server('localhost', 8080, app)
server.serve_forever()


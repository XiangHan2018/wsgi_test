# -*-coding:utf-8-*-
# application/framework side
from wsgiref.simple_server import make_server
from cgi import parse_qs


def application(environ, start_response):
    print(environ['PATH_INFO'])
    f = open('index.html', 'rb')
    body = f.read()
    f.close()
    # print(body)
    body2 = login_test(environ)
    # print(environ)
    # print(body)
    body3 = 'qing deng lu'
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])
    if 'None' not in body2:
        f = open('index2.html', 'rb')
        body = f.read()
        f.close()
        body3 = 'deng lu cheng gong'

        return body, body3

    # print(body)
    # print(body2)
    return [body, body3]


def login_test(env):
    try:
        login_size = int(env.get('CONTENT_LENGTH', 0))
    except ValueError:
        login_size = 0
    # print('login_size' + str(login_size))
    requests_body = env['wsgi.input'].read(login_size)

    body = parse_qs(requests_body)
    # print('body:' + str(body))
    user = body.get('user', ['None'])[0].encode('utf-8')
    passwd = body.get('password', ['None'])[0].encode('utf-8')

    print(user, passwd)
    return [user, passwd]


def test_1():
    return 'This is a python application!2222'


# server/gateway side
class Http_split():
    def __init__(self, app):
        self.app = app

    def test_1(self, env, start_response):

        body = 'test_1'
        strat = '200 ok'
        harders = [('Content-Type', 'text/plain')]
        start_response(strat, harders)

        return [body]

    def test_2(self, env, start_response):
        body = 'test_2'
        strat = '200 ok'
        harders = [('Content-Type', 'text/plain'),
                   ('Content-Length', str(len(body)))]
        start_response(strat, harders)
        return [body]

    def __call__(self, env, start_response):
        if env['PATH_INFO']:
            if env['PATH_INFO'] == '/1':
                return self.test_1(env, start_response)
            if env['PATH_INFO'] == '/change_data':
                return self.test_2(env, start_response)
            else:
                return self.app(env, start_response)


        else:
            return self.app(env, start_response)


app = Http_split(application)
server = make_server('localhost', 8080, app)
server.serve_forever()

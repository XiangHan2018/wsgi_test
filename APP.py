# -*-coding:utf-8-*-
# application/framework side
from wsgiref.simple_server import make_server
from cgi import parse_qs
import json
import re


def application(environ, start_response):
    print(environ['PATH_INFO'])
    # f = open('index.html', 'rb')
    # body = f.read()
    # f.close()
    json_data = {
        "code": 0,
        "msg": "",
        "resulet":{
            "data": {

            }
        }



    }
    body2 = login_test(environ)

    body4 = 'qing deng lu'

    if 'None' not in body2:
        body3 = 'deng lu cheng gong'
        print()
        json_data['msg'] = body3
        json_data['resulet']['data']['user'] = body2[0]
        json_data['resulet']['data']['passwrd'] = body2[1]
    else:
        json_data['code'] = 1
        json_data['msg'] = body4

    if environ.get('HTTP_ORIGIN'):
        response_headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(str(json_data)))),
            ('Access-Control-Allow-Origin', environ.get('HTTP_ORIGIN')),
            ('Access-Control-Allow-Headers', 'Content-Type')]
        print(environ.get('HTTP_ORIGIN'))
        start_response('200 OK', response_headers)
    else:
        start_response('200 OK', [('Content-Type', 'application/json')])
    # print(type(json_data),json_data)
    # print(type(json_data['msg']))
    json_data = json.dumps(json_data)
    # print(len(json_data))
    print(json_data)
    return [json_data.encode('utf-8')]


def login_test(env):
    try:
        login_size = int(env.get('CONTENT_LENGTH', 0))
    except ValueError:
        login_size = 0
    # print('login_size' + str(login_size))
    requests_body = env['wsgi.input'].read(login_size)
    # print(env)

    body = requests_body.decode('utf-8')
    body = re.sub('\'', '\"', body)
    json_dict = json.loads(body)
    print(json_dict)
    try:
        user = json_dict['data']['user']
        passwd = json_dict['data']['passwrod']
    except KeyError:
        user = 'None'
        passwd = 'None'

    # print(type(user), type(passwd))
    return [user, passwd]


# server/gateway side
class Http_split():
    def __init__(self, app):
        self.app = app

    def test_3(self, env, start_response, ORIGIN):
        response_body = 'oK'
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body))),
            ('Access-Control-Allow-Origin', ORIGIN),
            ('Access-Control-Allow-Headers', 'Content-Type')]
        start_response(status, response_headers)

        return [response_body.encode('utf-8')]

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

    # def test_3(self,env,start_response,ORIGIN):
    #     response_headers.extend([('Access-Control-Allow-Origin', origin)])
    #     return start_response(status, response_headers, exc_info)

    def __call__(self, env, start_response):
        # ORIGIN = env.get('HTTP_ORIGIN')
        # if ORIGIN:
        #     if env.get('REQUEST_METHOD') == 'OPTIONS':
        #         return test_1(env,start_response,ORIGIN)
        #     else:
        #
        #
        # else:

        if env['PATH_INFO']:

            if 'PATH_INFO' in env.keys():
                if env['REQUEST_METHOD'] == 'OPTIONS':
                    return self.test_3(env, start_response,env['HTTP_ORIGIN'])
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

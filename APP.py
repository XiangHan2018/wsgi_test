# -*-coding:utf-8-*-
# application/framework side
from wsgiref.simple_server import make_server
from cgi import parse_qs
import json
import re


class application:
    @classmethod
    def login(cls,environ, start_response):
        print(environ['PATH_INFO'])
        json_data = {
            "code": 0,
            "msg": "",
            "resulet":{
                "data": {

                }
            }
        }
        body2 = cls.login_test(environ)

        json_data['msg'] = '登录失败'

        if 'None' not in body2:
            json_data['msg'] = '登录成功'
            json_data['resulet']['data']['user'] = body2[0]
            json_data['resulet']['data']['passwrd'] = body2[1]
        else:
            json_data['code'] = 1
        json_data = json.dumps(json_data)
        if environ.get('HTTP_ORIGIN'):
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(json_data))),
                ('Access-Control-Allow-Origin', environ.get('HTTP_ORIGIN')),
                ('Access-Control-Allow-Headers', 'Content-Type')]
            print(environ.get('HTTP_ORIGIN'))
            start_response('200 OK', response_headers)
        else:
            start_response('200 OK', [('Content-Type', 'application/json')])
        # print(type(json_data),json_data)
        # print(type(json_data['msg']))

        print(json_data)
        return [json_data.encode('utf-8')]

    @classmethod
    def login_test(cls,env):
        try:
            login_size = int(env.get('CONTENT_LENGTH', 0))
        except ValueError:
            login_size = 0
        requests_body = env['wsgi.input'].read(login_size)
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

    @classmethod
    def OPTIONS(cls, env, start_response, ORIGIN):
        response_body = 'oK'
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body))),
            ('Access-Control-Allow-Origin', ORIGIN),
            ('Access-Control-Allow-Headers', 'Content-Type')]
        start_response(status, response_headers)

        return [response_body.encode('utf-8')]

    @classmethod
    def test_1(cls, env, start_response):

        body = 'test_1'
        strat = '200 ok'
        harders = [('Content-Type', 'text/plain')]
        start_response(strat, harders)

        return [body]

    @classmethod
    def test_2(cls, env, start_response):
        body = 'test_2'
        strat = '200 ok'
        harders = [('Content-Type', 'text/plain'),
                   ('Content-Length', str(len(body)))]
        start_response(strat, harders)
        return [body]


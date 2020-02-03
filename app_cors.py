from APP import application


class Http_split:
    def __init__(self, app):
        self.app = app

    def __call__(self, env, start_response):

        if env['PATH_INFO']:

            if 'PATH_INFO' in env.keys():
                if env['REQUEST_METHOD'] == 'OPTIONS':
                    return application.OPTIONS(env, start_response, env['HTTP_ORIGIN'])
            if env['PATH_INFO'] == '/1':
                return application.test_1(env, start_response)
            if env['PATH_INFO'] == '/change_data':
                return application.test_2(env, start_response)
            else:
                return self.app(env, start_response)

        else:

            return self.app(env, start_response)

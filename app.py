import re
def http404(env, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return ['404 Not Found']

def http405(env, start_response):
    start_response('405 Method Not Allowed', [('Content-type', 'text/plain; charset=utf-8')])
    return ['405 Method Not Allowed']


class Router():
    def __init__(self):
        self.routes = []

    def add(self, method, path, callback):
        self.routes.append({
            'method': method, # GET とか POST
            'path': path, # path 
            'callback': callback # pathへのアクセス時に呼び出したい関数
        })

    def match(self, method, path):
        # pathがroutesに登録されているかを調べる
        for route in self.routes:
            matched = re.compile(route['path']).match(path)
            if matched and route['method'] == method:
                url_vars = matched.groupdict()
                return route['callback'], url_vars
        return http404, {}


class App():

    def __init__(self):
        self.router = Router()

    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    # Appをcallable(呼び出し可能)に
    def __call__(self, env, start_response):
        # リクエストヘッダーからメソッド POST/GETなどを受け取る
        method = env['REQUEST_METHOD'].upper()
        # リクエストヘッダーからパスの情報を受け取る
        path = env['PATH_INFO'] or '/'
        callback, kwargs = self.router.match(method, path)
        return callback(env, start_response, **kwargs)

    
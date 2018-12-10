import re
def http404(env, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return ['404 Not Found']

def http405(env, start_response):
    start_response('405 Method Not Allowed', [('Content-type', 'text/plain; charset=utf-8')])
    return ['405 Method Not Allowed']

class Request():
    def __init__(self,environ):
        self.environ = environ
        self._body = None

    @property
    def path(self):
        return self.environ['PATH_INFO'] or '/'
    
    @property
    def method(self):
        return self.environ['REQUEST_METHOD'].upper()

    @property
    def body(self):
        if self._body is None:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
            self._body = self.environ['wsgi.input'].read(content_length)
            return self._body

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
        error_callback = http404
        # pathがroutesに登録されているかを調べる
        for route in self.routes:
            matched = re.compile(route['path']).match(path)
            if not matched:
                continue
            
            error_callback = http405
            url_vars = matched.groupdict()
            if route['method'] == method:
                return route['callback'], url_vars
        return error_callback, {}


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
        request = Request(env)
        callback, kwargs = self.router.match(request.method, request.path)
        return callback(request, start_response, **kwargs)
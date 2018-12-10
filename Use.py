from app import App
from wsgiref.simple_server import make_server


app = App()


@app.route('^/$', 'GET')
def hello(request, start_response):
    return ['Hello World']


@app.route('^/user/$', 'POST')
def create_user(request, start_response):
    return ['User Created']


@app.route('^/user/(?P<name>\w+)/$', 'GET')
def user_detail(request, start_response, name):
    body = 'Hello {name}'.format(name=name)
    return [body.encode('utf-8')]


@app.route('^/user/(?P<name>\w+)/follow/$', 'POST')
def create_user(request, start_response, name):
    body = 'Followed {name}'.format(name=name)
    return [body.encode('utf-8')]


if __name__ == '__main__':
    httpd = make_server('', 5000, app)
    httpd.serve_forever()
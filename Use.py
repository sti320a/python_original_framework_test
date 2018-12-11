from app import App, Response
from wsgiref.simple_server import make_server


app = App()


@app.route('^/$', 'GET')
def hello(request):
    return Response('Hello World')


@app.route('^/user/$', 'POST')
def create_user(request):
    return Response('User Created', status=201)


@app.route('^/user/(?P<name>\w+)/$', 'GET')
def user_detail(request, name):
    return Response('Hello {name}'.format(name=name))


if __name__ == '__main__':
    httpd = make_server('', 5000, app)
    httpd.serve_forever()
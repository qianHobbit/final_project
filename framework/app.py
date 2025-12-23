from wsgiref.simple_server import make_server

from .request import Request
from .response import Response
from .router import Router


class App:
    def __init__(self):
        self.router = Router()

    def route(self, path, methods=None):
        if methods is None:
            methods = ['GET']

        def decorator(handler):
            self.router.add_route(path, methods, handler)
            return handler

        return decorator

    def __call__(self, environ, start_response):
        request = Request(environ)

        handler = self.router.resolve(request.path, request.method)

        if handler is None:
            response = Response(body='404 Not Found', status=404)
        else:
            try:
                response = handler(request)
                if not isinstance(response, Response):
                    response = Response(body=response)
            except Exception as e:
                error_body = f'500 Internal Server Error: {str(e)}'
                response = Response(body=error_body, status=500)

        status_line = response.status_line()
        headers_list = response.headers_list()
        start_response(status_line, headers_list)

        return [response.body]

    def run(self, host='127.0.0.1', port=8000):
        with make_server(host, port, self) as httpd:
            print(f"Working on http://{host}:{port}/")
            httpd.serve_forever()
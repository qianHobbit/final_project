import unittest
from io import BytesIO

from framework.app import App
from framework.request import Request
from framework.response import Response


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.base_environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'wsgi.input': BytesIO(b''),
            'CONTENT_LENGTH': '0',
        }

    def test_app_initialization(self):
        self.assertIsNotNone(self.app.router)

    def test_route_decorator_get(self):
        @self.app.route('/test', methods=['GET'])
        def test_handler(request):
            return Response(body='Test response')

        handler = self.app.router.resolve('/test', 'GET')
        self.assertIsNotNone(handler)

    def test_route_decorator_default_method(self):
        @self.app.route('/default')
        def default_handler(request):
            return Response(body='Default')

        handler = self.app.router.resolve('/default', 'GET')
        self.assertIsNotNone(handler)

    def test_route_decorator_multiple_methods(self):
        @self.app.route('/api', methods=['GET', 'POST'])
        def api_handler(request):
            return Response(body='API')

        self.assertIsNotNone(self.app.router.resolve('/api', 'GET'))
        self.assertIsNotNone(self.app.router.resolve('/api', 'POST'))

    def test_wsgi_call_with_valid_route(self):
        @self.app.route('/hello')
        def hello_handler(request):
            return Response(body='Hello, World!', status=200)

        environ = self.base_environ.copy()
        environ['PATH_INFO'] = '/hello'

        def start_response(status, headers):
            self.assertEqual(status, '200 OK')
            self.assertIsInstance(headers, list)

        response_body = self.app(environ, start_response)
        self.assertEqual(response_body, [b'Hello, World!'])

    def test_wsgi_call_with_404(self):
        environ = self.base_environ.copy()
        environ['PATH_INFO'] = '/nonexistent'

        def start_response(status, headers):
            self.assertEqual(status, '404 Not Found')

        response_body = self.app(environ, start_response)
        self.assertIn(b'404', b''.join(response_body))

    def test_wsgi_call_handler_exception(self):
        @self.app.route('/error')
        def error_handler(request):
            raise ValueError('Test error')

        environ = self.base_environ.copy()
        environ['PATH_INFO'] = '/error'

        def start_response(status, headers):
            self.assertEqual(status, '500 Internal Server Error')

        response_body = self.app(environ, start_response)
        response_text = b''.join(response_body).decode('utf-8')
        self.assertIn('500', response_text)

    def test_wsgi_call_handler_returns_string(self):
        @self.app.route('/string')
        def string_handler(request):
            return 'Just a string'

        environ = self.base_environ.copy()
        environ['PATH_INFO'] = '/string'

        def start_response(status, headers):
            pass

        response_body = self.app(environ, start_response)
        self.assertIn(b'Just a string', b''.join(response_body))

    def test_request_object_in_handler(self):
        received_request = None

        @self.app.route('/test-request')
        def request_test_handler(request):
            nonlocal received_request
            received_request = request
            return Response(body='OK')

        environ = self.base_environ.copy()
        environ['PATH_INFO'] = '/test-request'
        environ['QUERY_STRING'] = 'key=value'

        def start_response(status, headers):
            pass

        self.app(environ, start_response)
        self.assertIsInstance(received_request, Request)
        self.assertEqual(received_request.query['key'], 'value')


if __name__ == '__main__':
    unittest.main()


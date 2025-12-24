import json
import unittest
from io import BytesIO

from framework.request import Request


class TestRequest(unittest.TestCase):

    def setUp(self):
        self.base_environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/test',
            'QUERY_STRING': '',
            'wsgi.input': BytesIO(b''),
            'CONTENT_LENGTH': '0',
        }

    def test_basic_request(self):
        request = Request(self.base_environ)
        self.assertEqual(request.path, '/test')
        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.body, b'')

    def test_query_parameters(self):
        environ = self.base_environ.copy()
        environ['QUERY_STRING'] = 'name=John&age=30'
        request = Request(environ)
        self.assertEqual(request.query['name'], 'John')
        self.assertEqual(request.query['age'], '30')

    def test_query_parameters_multiple_values(self):
        environ = self.base_environ.copy()
        environ['QUERY_STRING'] = 'tags=python&tags=web'
        request = Request(environ)
        self.assertIsInstance(request.query['tags'], list)
        self.assertIn('python', request.query['tags'])
        self.assertIn('web', request.query['tags'])

    def test_headers_parsing(self):
        environ = self.base_environ.copy()
        environ['HTTP_HOST'] = 'localhost:8000'
        environ['HTTP_USER_AGENT'] = 'TestAgent'
        environ['CONTENT_TYPE'] = 'application/json'
        request = Request(environ)
        self.assertEqual(request.headers['Host'], 'localhost:8000')
        self.assertEqual(request.headers['User-Agent'], 'TestAgent')
        self.assertEqual(request.headers['Content-Type'], 'application/json')

    def test_request_body(self):
        body_content = b'Hello, World!'
        environ = self.base_environ.copy()
        environ['CONTENT_LENGTH'] = str(len(body_content))
        environ['wsgi.input'] = BytesIO(body_content)
        request = Request(environ)
        self.assertEqual(request.body, body_content)

    def test_json_parsing(self):
        json_data = {'name': 'John', 'age': 30}
        body_content = json.dumps(json_data).encode('utf-8')
        environ = self.base_environ.copy()
        environ['CONTENT_LENGTH'] = str(len(body_content))
        environ['wsgi.input'] = BytesIO(body_content)
        request = Request(environ)
        parsed_json = request.json()
        self.assertEqual(parsed_json, json_data)

    def test_json_empty_body(self):
        request = Request(self.base_environ)
        self.assertEqual(request.json(), {})

    def test_json_invalid(self):
        body_content = b'not valid json'
        environ = self.base_environ.copy()
        environ['CONTENT_LENGTH'] = str(len(body_content))
        environ['wsgi.input'] = BytesIO(body_content)
        request = Request(environ)
        with self.assertRaises(json.JSONDecodeError):
            request.json()

    def test_post_request(self):
        environ = self.base_environ.copy()
        environ['REQUEST_METHOD'] = 'POST'
        environ['PATH_INFO'] = '/users'
        request = Request(environ)
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.path, '/users')


if __name__ == '__main__':
    unittest.main()
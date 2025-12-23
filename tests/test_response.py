import unittest
from framework.response import Response



class TestResponse(unittest.TestCase):

    def test_basic_response(self):
        response = Response(body='Hello, World!')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, b'Hello, World!')
        self.assertIn('Content-Type', response.headers)
        self.assertIn('Content-Length', response.headers)

    def test_response_with_bytes(self):
        response = Response(body=b'Binary data')
        self.assertEqual(response.body, b'Binary data')
        self.assertEqual(response.headers['Content-Length'], '11')

    def test_response_status_codes(self):
        response_404 = Response(body='Not Found', status=404)
        self.assertEqual(response_404.status, 404)
        self.assertEqual(response_404.status_line(), '404 Not Found')

        response_500 = Response(body='Error', status=500)
        self.assertEqual(response_500.status, 500)
        self.assertEqual(response_500.status_line(), '500 Internal Server Error')

    def test_status_line(self):
        response = Response(status=200)
        self.assertEqual(response.status_line(), '200 OK')

        response = Response(status=201)
        self.assertEqual(response.status_line(), '201 Created')

        response = Response(status=404)
        self.assertEqual(response.status_line(), '404 Not Found')

    def test_headers_list(self):
        response = Response(body='Test', headers={'X-Custom': 'value'})
        headers_list = response.headers_list()
        self.assertIsInstance(headers_list, list)
        for item in headers_list:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
        header_dict = dict(headers_list)
        self.assertEqual(header_dict['X-Custom'], 'value')

    def test_content_length(self):
        body = 'Hello, World!'
        response = Response(body=body)
        expected_length = str(len(body.encode('utf-8')))
        self.assertEqual(response.headers['Content-Length'], expected_length)

    def test_default_content_type(self):
        response = Response(body='Test')
        self.assertIn('Content-Type', response.headers)
        self.assertIn('text/html', response.headers['Content-Type'])

    def test_custom_content_type(self):
        response = Response(
            body='{"key": "value"}',
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_unicode_body(self):
        body = 'Привет, мир!'
        response = Response(body=body)
        self.assertEqual(response.body, body.encode('utf-8'))

    def test_empty_body(self):
        response = Response(body='')
        self.assertEqual(response.body, b'')
        self.assertEqual(response.headers['Content-Length'], '0')


if __name__ == '__main__':
    unittest.main()
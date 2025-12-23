import json
from urllib.parse import parse_qs


class Request:
    def __init__(self, environ):
        self.environ = environ
        self.path = environ.get('PATH_INFO', '/')
        self.method = environ.get('REQUEST_METHOD', 'GET')
        self.headers = self._parse_headers()
        self.query = self._parse_query()
        self.body = self._read_body()

    def _parse_headers(self):
        headers = {}
        for key, value in self.environ.items():
            if key.startswith('HTTP_'):
                header_name = key[5:].replace('_', '-').title()
                headers[header_name] = value
        if 'CONTENT_TYPE' in self.environ:
            headers['Content-Type'] = self.environ['CONTENT_TYPE']
        if 'CONTENT_LENGTH' in self.environ:
            headers['Content-Length'] = self.environ['CONTENT_LENGTH']
        return headers

    def _parse_query(self):
        query_string = self.environ.get('QUERY_STRING', '')
        if not query_string:
            return {}
        parsed = parse_qs(query_string, keep_blank_values=True)
        query = {}
        for key, value_list in parsed.items():
            if len(value_list) == 1:
                query[key] = value_list[0]
            else:
                query[key] = value_list
        return query

    def _read_body(self):
        try:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            content_length = 0
        if content_length > 0:
            wsgi_input = self.environ.get('wsgi.input')
            if wsgi_input:
                return wsgi_input.read(content_length)
        return b''

    def json(self):
        if not self.body:
            return {}
        try:
            body_str = self.body.decode('utf-8')
            return json.loads(body_str)
        except UnicodeDecodeError:
            raise ValueError("Request body is not UTF-8 encoded")
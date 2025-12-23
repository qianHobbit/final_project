class Response:
    STATUS_CODES = {
        200: 'OK',
        201: 'Created',
        204: 'No Content',
        301: 'Moved Permanently',
        302: 'Found',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        500: 'Internal Server Error',
        501: 'Not Implemented',
    }

    def __init__(self, body='', status=200, headers=None):
        self.status = status
        self.headers = headers or {}

        if 'Content-Type' not in self.headers:
            self.headers['Content-Type'] = 'text/html; charset=utf-8'

        if isinstance(body, str):
            self.body = body.encode('utf-8')
        else:
            self.body = body if isinstance(body, bytes) else str(body).encode('utf-8')

        self.headers['Content-Length'] = str(len(self.body))

    def status_line(self):
        status_text = self.STATUS_CODES.get(self.status, 'Unknown')
        return f"{self.status} {status_text}"

    def headers_list(self):
        return [(key, str(value)) for key, value in self.headers.items()]
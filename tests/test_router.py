import unittest
from framework.router import Router


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = Router()

    def test_add_route_single_method(self):
        def handler(request):
            pass

        self.router.add_route('/users', 'GET', handler)
        resolved = self.router.resolve('/users', 'GET')
        self.assertEqual(resolved, handler)

    def test_add_route_multiple_methods(self):
        def get_handler(request):
            pass

        def post_handler(request):
            pass

        self.router.add_route('/users', ['GET'], get_handler)
        self.router.add_route('/users', ['POST'], post_handler)

        self.assertEqual(self.router.resolve('/users', 'GET'), get_handler)
        self.assertEqual(self.router.resolve('/users', 'POST'), post_handler)

    def test_resolve_nonexistent_route(self):
        resolved = self.router.resolve('/nonexistent', 'GET')
        self.assertIsNone(resolved)

    def test_resolve_wrong_method(self):
        def handler(request):
            pass

        self.router.add_route('/users', 'GET', handler)
        resolved = self.router.resolve('/users', 'POST')
        self.assertIsNone(resolved)

    def test_method_case_insensitive(self):
        def handler(request):
            pass

        self.router.add_route('/test', 'GET', handler)
        resolved = self.router.resolve('/test', 'get')
        self.assertEqual(resolved, handler)

    def test_multiple_routes(self):
        def users_handler(request):
            pass

        def posts_handler(request):
            pass

        self.router.add_route('/users', 'GET', users_handler)
        self.router.add_route('/posts', 'GET', posts_handler)

        self.assertEqual(self.router.resolve('/users', 'GET'), users_handler)
        self.assertEqual(self.router.resolve('/posts', 'GET'), posts_handler)

    def test_same_path_different_methods(self):
        def get_handler(request):
            return 'GET'

        def post_handler(request):
            return 'POST'

        self.router.add_route('/api', 'GET', get_handler)
        self.router.add_route('/api', 'POST', post_handler)

        self.assertEqual(self.router.resolve('/api', 'GET'), get_handler)
        self.assertEqual(self.router.resolve('/api', 'POST'), post_handler)


if __name__ == '__main__':
    unittest.main()
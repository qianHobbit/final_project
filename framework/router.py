class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, methods, handler):
        if isinstance(methods, str):
            methods = [methods]

        for method in methods:
            method_upper = method.upper()
            route_key = (path, method_upper)
            self.routes[route_key] = handler

    def resolve(self, path, method):
        method_upper = method.upper()
        route_key = (path, method_upper)
        return self.routes.get(route_key)
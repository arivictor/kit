import re
from http.server import HTTPServer

from .route_handler import RouteHandler


class App:
    """
    A simple HTTP server application class.
    It allows you to define routes and their corresponding handler functions.
    """
    def route(self, path: str, handler_func):
        if not callable(handler_func):
            raise TypeError("handler_func must be callable")

        method: str = handler_func.__name__.upper()
        if method not in RouteHandler.routes:
            raise ValueError(f"Unsupported method: {method}")

        cls: str = handler_func.__qualname__.split('.')[0]
        cls_obj = handler_func.__globals__.get(cls)
        if cls_obj is None:
            raise RuntimeError(f"Could not locate class for handler")

        bound_func = lambda request, **params: handler_func(cls_obj(), request, **params)
        pattern: str = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', path)
        regex: re.Pattern[str] = re.compile(f"^{pattern}$")
        RouteHandler.routes[method].append((path, regex, bound_func))

    def run(self, host: str = 'localhost', port: int = 8000):
        httpd = HTTPServer((host, port), RouteHandler)
        print(f"Serving on http://{host}:{port}")
        httpd.serve_forever()


def New():
    return App()

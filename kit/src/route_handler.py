import re
import json
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from .request import Request


class RouteHandler(BaseHTTPRequestHandler):
    """
    A simple HTTP request handler that routes requests to the appropriate handler function.
    It supports GET, POST, PUT, DELETE, and OPTIONS methods.
    It also provides a way to define routes with dynamic parameters.
    """
    routes = {"GET": [], "POST": [], "PUT": [], "DELETE": []}  # method -> list of (pattern, regex, handler_func)

    def do_GET(self): self.handle_method('GET')
    def do_POST(self): self.handle_method('POST')
    def do_PUT(self): self.handle_method('PUT')
    def do_DELETE(self): self.handle_method('DELETE')
    def do_OPTIONS(self): self.handle_options()

    def respond(self, status, headers, body):
        """
        Send an HTTP response with the given status code, headers, and body.
        Args:
            status (int): The HTTP status code.
            headers (dict): A dictionary of HTTP headers.
            body (str or bytes): The response body.
        """
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body.encode() if isinstance(body, str) else body)

    def handle_method(self, method):
        """
        Handle the HTTP method (GET, POST, PUT, DELETE) by matching the request path
        against the defined routes and calling the corresponding handler function.
        If no route matches, a 404 Not Found response is returned.
        """
        for pattern, regex, handler_func in self.routes.get(method, []):
            match = regex.match(self.path)
            if match:
                try:
                    request = Request(self)
                    response = handler_func(request, **match.groupdict())

                    if isinstance(response, dict):
                        status = response.get("status", 200)
                        headers = response.get("headers", {})
                        body = response.get("body", "")
                    else:
                        status, headers, body = 200, {}, response

                    self.respond(status, headers, body)
                    return
                except Exception:
                    tb = traceback.format_exc()
                    self.respond(500, {"Content-Type": "text/plain"}, f"Internal Server Error:\n{tb}")
                    return
        self.respond(404, {}, b'404 Not Found')

    def handle_options(self):
        """
        Handle OPTIONS requests by returning the allowed methods for the requested path.
        """
        methods = [method for method, routes in self.routes.items() for (_, regex, _) in routes if regex.match(self.path)]
        if methods:
            self.send_response(204)
            self.send_header("Allow", ", ".join(set(methods)))
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

import re
from http.server import HTTPServer, BaseHTTPRequestHandler

class RouteHandler(BaseHTTPRequestHandler):
    routes = []  # List of (pattern, compiled_regex, handler_class)

    def do_GET(self): self.handle_method('GET')
    def do_POST(self): self.handle_method('POST')
    def do_PUT(self): self.handle_method('PUT')
    def do_DELETE(self): self.handle_method('DELETE')

    def handle_method(self, method):
        for pattern, regex, handler_class in self.routes:
            match = regex.match(self.path)
            if match:
                handler = handler_class()
                if hasattr(handler, method):
                    try:
                        method_func = getattr(handler, method)
                        response = method_func(self, **match.groupdict())

                        if isinstance(response, dict):
                            status = response.get("status", 200)
                            headers = response.get("headers", {})
                            body = response.get("body", "")
                        else:
                            status, headers, body = 200, {}, response

                        self.send_response(status)
                        for k, v in headers.items():
                            self.send_header(k, v)
                        self.end_headers()
                        self.wfile.write(body.encode())
                        return
                    except Exception as e:
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(f"Internal Server Error:\n{e}".encode())
                        return
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'404 Not Found')

class App:
    def route(self, path: str, handler_class: type):
        pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', path)
        regex = re.compile(f"^{pattern}$")
        RouteHandler.routes.append((path, regex, handler_class))

    def run(self, host: str = 'localhost', port: int = 8000):
        httpd = HTTPServer((host, port), RouteHandler)
        print(f"Serving on http://{host}:{port}")
        httpd.serve_forever()

def New():
    return App()
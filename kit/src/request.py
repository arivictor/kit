import re
import json
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class Request:
    """
    A class representing an HTTP request.
    It encapsulates the request path, headers, method, query parameters,
    and the handler that processed the request.
    """
    def __init__(self, handler):
        self.path = handler.path
        self.headers = handler.headers
        self.method = handler.command
        self.query = parse_qs(urlparse(handler.path).query)
        self.handler = handler


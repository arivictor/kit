import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

def json_response(data: dict, status: int = 200):
    return {
        "body": json.dumps(data),
        "status": status,
        "headers": {"Content-Type": "application/json"}
    }
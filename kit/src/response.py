import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

def json_response(data: dict, status: int = 200):
    """
    Create a JSON response.
    Args:
        data (dict): The data to be converted to JSON.
        status (int): The HTTP status code. Defaults to 200.
        Returns:
            dict: A dictionary containing the response body, status, and headers.
    """
    return {
        "body": json.dumps(data),
        "status": status,
        "headers": {"Content-Type": "application/json"}
    }
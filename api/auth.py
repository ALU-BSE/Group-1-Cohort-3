#Adding basic authentication for our main.py file
import base64

USERS = {
    "admin": "pass123",}

def check_auth(handler):
    """Validate Basic auth header on the given handler.

    Returns True when credentials match, False otherwise. Does not send
    HTTP responses; caller (require_auth) will handle the 401 response.
    """
    auth_header = handler.headers.get('Authorization') if handler and getattr(handler, 'headers', None) is not None else None
    if not auth_header or not auth_header.startswith('Basic '):
        return False

    encoded = auth_header.split(" ", 1)[1]
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return USERS.get(username) == password
    except Exception:
        return False
    
def require_auth(handler):
    if not check_auth(handler):
        handler.send_response(401)
        handler.send_header("WWW-Authenticate", 'Basic realm="Access to API"')
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(b'{"error": "Unauthorized"}')
        return False
    return True

